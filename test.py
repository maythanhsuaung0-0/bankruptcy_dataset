"""Run the nine requested exploratory checks without changing the source data.

Run from the project directory: venv/bin/python test.py
The report and complete supporting tables are saved in results/data_audit/.
"""

import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
FINANCIAL_COLUMNS = [f"X{i}" for i in range(1, 19)]
HIGH_CORRELATION_THRESHOLD = 0.95
SMALL_VALUE_THRESHOLD = 1.0


def markdown_table(frame):
    """Render a small table without requiring the optional tabulate package."""
    def cell(value):
        if pd.isna(value):
            return ""
        if isinstance(value, (float, np.floating)):
            return f"{value:,.6g}"
        return str(value).replace("|", "\\|").replace("\n", " ")

    rows = [list(frame.columns), ["---"] * len(frame.columns)]
    rows.extend(frame.itertuples(index=False, name=None))
    return "\n".join("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)


def audit_dataframe(df, output_dir, source):
    """Inspect df and write a report plus CSV tables; do not alter df."""
    required = ["company_name", "status_label", "year", *FINANCIAL_COLUMNS]
    absent = sorted(set(required) - set(df.columns))
    if absent:
        raise ValueError(f"Required columns are missing: {absent}")
    if df.empty:
        raise ValueError("The dataset contains no observations.")
    if not all(pd.api.types.is_numeric_dtype(df[c]) for c in ["year", *FINANCIAL_COLUMNS]):
        raise ValueError("Year and financial columns must be numeric; inspect the input dtypes.")
    if df["company_name"].isna().any() or df["year"].isna().any():
        raise ValueError("Missing company/year keys prevent a reliable company-history audit.")
    if not np.isfinite(df["year"]).all() or df["year"].mod(1).ne(0).any():
        raise ValueError("Years must be finite integers for the consecutive-year checks.")

    output_dir.mkdir(parents=True, exist_ok=True)

    def save(name, table, index=False):
        table.to_csv(output_dir / f"{name}.csv", index=index)

    # 1. Descriptive statistics: all columns, plus detailed numerical summaries.
    descriptive = df.describe(include="all").T.rename_axis("column").reset_index()
    numeric = df.select_dtypes(include="number")
    numeric_summary = numeric.describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99]).T
    numeric_summary["range"] = numeric_summary["max"] - numeric_summary["min"]
    numeric_summary = numeric_summary.rename_axis("column").reset_index()
    categorical = df[["company_name", "status_label"]].describe().T
    categorical = categorical.rename_axis("column").reset_index()
    save("descriptive_statistics", descriptive)
    save("numeric_statistics", numeric_summary)
    save("categorical_statistics", categorical)

    # 2. Dataset shape and inferred datatypes; check infinity in every numeric column.
    schema = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_null": df.notna().sum().to_numpy(),
        "missing": df.isna().sum().to_numpy(),
        "positive_infinity": [int(np.isposinf(df[c]).sum()) if c in numeric else 0 for c in df],
        "negative_infinity": [int(np.isneginf(df[c]).sum()) if c in numeric else 0 for c in df],
    })
    save("column_quality", schema)

    # 3 and 5. Observation counts and status consistency for every company.
    grouped = df.groupby("company_name", sort=True)
    companies = grouped.agg(
        observations=("year", "size"),
        unique_years=("year", "nunique"),
        first_year=("year", "min"),
        last_year=("year", "max"),
        distinct_statuses=("status_label", lambda s: s.nunique(dropna=False)),
        missing_statuses=("status_label", lambda s: s.isna().sum()),
        status_labels=("status_label", lambda s: ", ".join(sorted(s.dropna().unique()))),
    )
    companies["status_is_constant"] = (
        companies["distinct_statuses"].eq(1) & companies["missing_statuses"].eq(0)
    )

    # 7. Compare sorted unique years; duplicates do not count as missing years.
    gap_records = []
    missing_years_by_company = {}
    for company, history in grouped:
        years = np.sort(history["year"].unique().astype(int))
        missing_years = []
        for previous, following in zip(years[:-1], years[1:]):
            if following - previous > 1:
                missing = list(range(int(previous) + 1, int(following)))
                missing_years.extend(missing)
                gap_records.append({
                    "company_name": company,
                    "previous_observed_year": previous,
                    "next_observed_year": following,
                    "missing_year_count": len(missing),
                    "missing_years": ", ".join(map(str, missing)),
                })
        missing_years_by_company[company] = missing_years
    companies["missing_year_count"] = [len(missing_years_by_company[c]) for c in companies.index]
    companies["missing_years"] = [", ".join(map(str, missing_years_by_company[c])) for c in companies.index]
    companies["consecutive_years"] = companies["missing_year_count"].eq(0)
    companies = companies.reset_index()
    inconsistent = companies.loc[~companies["status_is_constant"]]
    gapped = companies.loc[~companies["consecutive_years"]]
    gaps = pd.DataFrame(gap_records, columns=[
        "company_name", "previous_observed_year", "next_observed_year", "missing_year_count", "missing_years",
    ])
    observation_distribution = companies["observations"].value_counts().sort_index()
    observation_distribution = observation_distribution.rename_axis("observations_per_company").reset_index(name="companies")
    save("company_observation_counts", companies)
    save("observations_per_company_distribution", observation_distribution)
    save("inconsistent_company_status", inconsistent)
    save("companies_with_year_gaps", gapped)
    save("year_gap_intervals", gaps)

    # 4. Report original labels at both observation and company level.
    row_status = df["status_label"].value_counts(dropna=False).rename_axis("status_label").reset_index(name="observations")
    row_status["percent"] = row_status["observations"] / len(df) * 100
    company_labels = companies["status_labels"].where(companies["status_is_constant"], "mixed_or_missing")
    company_status = company_labels.value_counts(dropna=False).rename_axis("status_label").reset_index(name="companies")
    company_status["percent"] = company_status["companies"] / len(companies) * 100
    save("status_distribution_rows", row_status)
    save("status_distribution_companies", company_status)

    # 6. Count both excess duplicates and all rows participating in duplicate groups.
    duplicate_rows = df.duplicated(keep=False)
    duplicate_keys = df.duplicated(["company_name", "year"], keep=False)
    infinite_rows = np.isinf(numeric).any(axis=1)
    quality = pd.DataFrame([
        ("missing_cells", int(df.isna().sum().sum())),
        ("rows_with_missing_values", int(df.isna().any(axis=1).sum())),
        ("infinite_numeric_cells", int(np.isinf(numeric).sum().sum())),
        ("rows_with_infinite_values", int(infinite_rows.sum())),
        ("duplicate_rows_excluding_first", int(df.duplicated().sum())),
        ("all_rows_in_duplicate_groups", int(duplicate_rows.sum())),
        ("duplicate_company_years_excluding_first", int(df.duplicated(["company_name", "year"]).sum())),
        ("all_rows_in_duplicate_company_year_groups", int(duplicate_keys.sum())),
    ], columns=["check", "count"])
    save("quality_checks", quality)
    save("duplicate_rows", df.loc[duplicate_rows])
    save("duplicate_company_year_rows", df.loc[duplicate_keys])
    save("rows_with_missing_or_infinite_values", df.loc[df.isna().any(axis=1) | infinite_rows])

    # 8. Flag financial values; thresholds identify review candidates, not errors.
    financial = df[FINANCIAL_COLUMNS]
    finite_financial = financial.where(np.isfinite(financial))
    q1 = finite_financial.quantile(0.25)
    q3 = finite_financial.quantile(0.75)
    iqr = q3 - q1
    lower_fence, upper_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    value_summary = pd.DataFrame({
        "min": finite_financial.min(),
        "p01": finite_financial.quantile(0.01),
        "median": finite_financial.median(),
        "p99": finite_financial.quantile(0.99),
        "max": finite_financial.max(),
        "negative_count": financial.lt(0).sum(),
        "zero_count": financial.eq(0).sum(),
        "small_nonzero_count": (financial.abs().lt(SMALL_VALUE_THRESHOLD) & financial.ne(0)).sum(),
        "iqr_lower_fence": lower_fence,
        "iqr_upper_fence": upper_fence,
        "below_iqr_fence_count": financial.lt(lower_fence).sum(),
        "above_iqr_fence_count": financial.gt(upper_fence).sum(),
    }).rename_axis("variable").reset_index()
    examples = []
    for variable in FINANCIAL_COLUMNS:
        for tail, indices in [
            ("smallest", finite_financial[variable].nsmallest(5).index),
            ("largest", finite_financial[variable].nlargest(5).index),
        ]:
            for idx in indices:
                value = df.at[idx, variable]
                examples.append({
                    "variable": variable,
                    "tail": tail,
                    "dataframe_index": idx,
                    "company_name": df.at[idx, "company_name"],
                    "year": df.at[idx, "year"],
                    "status_label": df.at[idx, "status_label"],
                    "value": value,
                    "negative": value < 0,
                    "zero": value == 0,
                    "small_nonzero": 0 < abs(value) < SMALL_VALUE_THRESHOLD,
                    "outside_iqr_fences": value < lower_fence[variable] or value > upper_fence[variable],
                })
    save("financial_value_flags", value_summary)
    save("financial_extreme_examples", pd.DataFrame(examples))

    # 9. Pearson and rank correlations; test exact equality independently.
    pearson = finite_financial.corr(method="pearson")
    spearman = finite_financial.corr(method="spearman")
    pair_records = []
    for left, right in combinations(FINANCIAL_COLUMNS, 2):
        equal = financial[left].eq(financial[right]) | (financial[left].isna() & financial[right].isna())
        pair_records.append({
            "variable_1": left,
            "variable_2": right,
            "pearson": pearson.at[left, right],
            "spearman": spearman.at[left, right],
            "identical_values": bool(equal.all()),
            "mismatching_rows": int((~equal).sum()),
        })
    pairs = pd.DataFrame(pair_records)
    high_pairs = pairs.loc[
        pairs[["pearson", "spearman"]].abs().ge(HIGH_CORRELATION_THRESHOLD).any(axis=1)
    ]
    exact_pairs = pairs.loc[pairs["identical_values"]]
    x9_x16 = pairs.loc[pairs["variable_1"].eq("X9") & pairs["variable_2"].eq("X16")].iloc[0]
    x9_x16_equal = df["X9"].eq(df["X16"]) | (df["X9"].isna() & df["X16"].isna())
    save("pearson_correlations", pearson.rename_axis("variable"), index=True)
    save("spearman_correlations", spearman.rename_axis("variable"), index=True)
    save("financial_variable_pairs", pairs)
    save("highly_correlated_pairs", high_pairs)
    save("identical_financial_variables", exact_pairs)
    save("x9_x16_mismatches", df.loc[~x9_x16_equal, ["company_name", "year", "X9", "X16"]])

    # The Markdown report previews long company lists; CSV files contain every row.
    report = [
        "# American Bankruptcy Dataset: Executed Data Audit",
        f"Source: `{source}`. Loaded as pandas dataframe `df`.",
        f"Environment: pandas {pd.__version__}; NumPy {np.__version__}.",
        "All nine checks inspect the original labels and financial values. No records or variables were removed, imputed, clipped, scaled, or relabeled.",
        "## 1. Descriptive statistics",
        "Numerical summaries include the year column; X1–X18 are the 18 financial variables. Standard deviation is the sample standard deviation (ddof=1).",
        markdown_table(numeric_summary),
        "Categorical summaries:",
        markdown_table(categorical),
        "Complete all-column output: [descriptive_statistics.csv](descriptive_statistics.csv).",
        "## 2. Shape and datatypes",
        f"Shape: **{df.shape[0]:,} rows × {df.shape[1]} columns**. Financial years: **{int(df.year.min())}–{int(df.year.max())}**.",
        markdown_table(schema),
        "## 3. Companies and observations per company",
        f"Unique companies: **{len(companies):,}**. Observations per company: **{int(companies.observations.min())}–{int(companies.observations.max())}**, median **{companies.observations.median():g}**, mean **{companies.observations.mean():.2f}**.",
        markdown_table(observation_distribution),
        "First 15 companies (the complete list is in [company_observation_counts.csv](company_observation_counts.csv)):",
        markdown_table(companies[["company_name", "observations", "first_year", "last_year"]].head(15)),
        "## 4. Original status_label distribution",
        "Company-year observations:",
        markdown_table(row_status),
        "Distinct companies (mixed/missing statuses are kept separate if present):",
        markdown_table(company_status),
        "These are the original company labels, not independently observed annual bankruptcy events. Repeated years of a failed company must not be counted as separate bankruptcies.",
        "## 5. Within-company status consistency",
        f"Companies with a constant, nonmissing status: **{int(companies.status_is_constant.sum()):,}/{len(companies):,}**. Companies with mixed/missing statuses: **{len(inconsistent):,}**.",
        "Complete results: [inconsistent_company_status.csv](inconsistent_company_status.csv).",
        "## 6. Missing values, infinite values, and duplicates",
        markdown_table(quality),
        "Duplicate counts excluding the first record measure excess rows. The companion counts include all members of a duplicate group. Missingness and infinity counts per column appear in Section 2. Detailed exception CSVs are saved even when empty.",
        "## 7. Consecutive yearly observations",
        f"Companies with internal year gaps: **{len(gapped):,}**. Companies without internal gaps: **{len(companies) - len(gapped):,}**. Missing internal company-years: **{int(companies.missing_year_count.sum()):,}** across **{len(gaps):,}** gap intervals.",
        f"Single-record companies: **{int(companies.observations.eq(1).sum()):,}**; they have no internal gaps but cannot establish a multi-year history. This check covers each company's first through last observed year, not the full dataset calendar span.",
        "First 15 companies with gaps:",
        markdown_table(gapped[["company_name", "observations", "first_year", "last_year", "missing_years"]].head(15)),
        "Complete company list: [companies_with_year_gaps.csv](companies_with_year_gaps.csv). Individual intervals: [year_gap_intervals.csv](year_gap_intervals.csv).",
        "## 8. Large, small, negative, and zero financial values",
        f"Small nonzero values use **0 < abs(value) < {SMALL_VALUE_THRESHOLD:g} in the stored units**. Unusually low/high values use **Q1 − 1.5×IQR / Q3 + 1.5×IQR**, computed separately for each financial variable. Negative, zero, small, and IQR flags may overlap. These are review flags rather than evidence of errors; skewed financial distributions can produce many IQR flags.",
        markdown_table(value_summary[["variable", "min", "median", "max", "negative_count", "zero_count", "small_nonzero_count"]]),
        "Statistical tail flags:",
        markdown_table(value_summary[["variable", "p01", "p99", "iqr_lower_fence", "iqr_upper_fence", "below_iqr_fence_count", "above_iqr_fence_count"]]),
        "The five smallest and five largest observations for every financial variable, with company/year identifiers and flags, are in [financial_extreme_examples.csv](financial_extreme_examples.csv). Complete thresholds and counts: [financial_value_flags.csv](financial_value_flags.csv).",
        "Negative earnings and retained earnings may represent real distress. Negative values in X1 (current assets) and X11 (long-term debt) deserve review. Small denominators in X10 (total assets), X14 (current liabilities), and X17 (total liabilities) could produce extreme ratios; their observed minima appear above. No flagged values were automatically removed.",
        "## 9. Identical and highly correlated financial variables",
        f"High correlation means **abs(Pearson r) ≥ {HIGH_CORRELATION_THRESHOLD} or abs(Spearman rho) ≥ {HIGH_CORRELATION_THRESHOLD}**. Only financial variables enter these calculations; no company IDs, year, or status encoding are included.",
        markdown_table(high_pairs),
        f"**X9 and X16 identical values: {bool(x9_x16.identical_values)}. Mismatching rows: {int(x9_x16.mismatching_rows):,}/{len(df):,}.** Equality is checked directly, without numerical tolerance; matching missing cells would be treated as equal. Each column has {int(df.X9.notna().sum()):,} / {int(df.X16.notna().sum()):,} nonmissing values respectively.",
        "Exact duplicate financial pairs:",
        markdown_table(exact_pairs),
        "Full matrices: [pearson_correlations.csv](pearson_correlations.csv) and [spearman_correlations.csv](spearman_correlations.csv). All 153 financial-variable pairs, exact-equality checks, and mismatch counts: [financial_variable_pairs.csv](financial_variable_pairs.csv).",
        "Correlation can reflect company size, skew, and repeated company observations. It does not by itself justify removing a variable. Exact duplicates can be excluded from later model inputs; all variables remain in this audit.",
        "## Reproduce",
        "Run from the project directory:",
        "```bash\nvenv/bin/python test.py\n```",
        "Optional arguments: `--data /path/to/american_bankruptcy.csv --output /path/to/report_directory`.",
    ]
    report_text = "\n\n".join(report) + "\n"
    (output_dir / "report.md").write_text(report_text, encoding="utf-8")
    return report_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=PROJECT_DIR / "data" / "american_bankruptcy.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_DIR / "results" / "data_audit")
    args = parser.parse_args()
    df = pd.read_csv(args.data, encoding="utf-8-sig")
    report = audit_dataframe(df, args.output, args.data)
    print(report)
    print(f"Saved report and complete CSV tables to {args.output.resolve()}")


if __name__ == "__main__":
    main()
