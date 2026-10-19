# American Bankruptcy Dataset: Executed Data Audit

Source: `/home/arkar/projects/datamining_project/bankruptcy_prediction/data/american_bankruptcy.csv`. Loaded as pandas dataframe `df`.

Environment: pandas 3.0.5; NumPy 2.5.3.

All nine checks inspect the original labels and financial values. No records or variables were removed, imputed, clipped, scaled, or relabeled.

## 1. Descriptive statistics

Numerical summaries include the year column; X1–X18 are the 18 financial variables. Standard deviation is the sample standard deviation (ddof=1).

| column | count | mean | std | min | 1% | 25% | 50% | 75% | 99% | max | range |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| year | 78,682 | 2,007.51 | 5.74277 | 1,999 | 1,999 | 2,002 | 2,007 | 2,012 | 2,018 | 2,018 | 19 |
| X1 | 78,682 | 880.362 | 3,928.56 | -7.76 | 0.066 | 18.924 | 100.45 | 431.527 | 13,626.8 | 169,662 | 169,670 |
| X2 | 78,682 | 1,594.53 | 8,930.48 | -366.645 | 0.031 | 17.0383 | 103.661 | 634.548 | 25,674.4 | 374,623 | 374,990 |
| X3 | 78,682 | 121.234 | 652.377 | 0 | 0.002 | 1.192 | 7.9295 | 47.9718 | 1,804.38 | 28,430 | 28,430 |
| X4 | 78,682 | 376.759 | 2,012.02 | -21,913 | -110.217 | -0.811 | 15.0345 | 139.655 | 6,517.19 | 81,730 | 103,643 |
| X5 | 78,682 | 201.606 | 1,060.77 | 0 | 0 | 0 | 7.023 | 74.7473 | 3,421.7 | 62,567 | 62,567 |
| X6 | 78,682 | 129.382 | 1,265.53 | -98,696 | -627.719 | -7.41575 | 1.616 | 40.1442 | 3,047.57 | 104,821 | 203,517 |
| X7 | 78,682 | 286.833 | 1,335.98 | -0.006 | 0 | 3.28125 | 22.82 | 131.581 | 4,848.48 | 65,812 | 65,812 |
| X8 | 78,682 | 3,414.35 | 18,414.1 | 0.0001 | 0.582091 | 34.98 | 227.512 | 1,244.89 | 60,436 | 1.07339e+06 | 1.07339e+06 |
| X9 | 78,682 | 2,364.02 | 11,950.1 | -1,965 | 0.038 | 27.5485 | 186.599 | 1,046.4 | 38,053.1 | 511,729 | 513,694 |
| X10 | 78,682 | 2,867.11 | 12,917.9 | 0.001 | 0.214 | 37.3635 | 213.203 | 1,171.36 | 46,434.3 | 531,864 | 531,864 |
| X11 | 78,682 | 722.484 | 3,242.17 | -0.023 | 0 | 0 | 7.5935 | 248.761 | 12,931.2 | 166,250 | 166,250 |
| X12 | 78,682 | 255.525 | 1,494.64 | -25,913 | -193.404 | -2.787 | 6.518 | 87.599 | 4,746.19 | 71,230 | 97,143 |
| X13 | 78,682 | 769.491 | 3,774.7 | -21,536 | -60.62 | 8.52125 | 63.5815 | 344.074 | 12,568.8 | 137,106 | 158,642 |
| X14 | 78,682 | 610.072 | 2,938.39 | 0.001 | 0.266 | 8.88925 | 43.333 | 222.817 | 10,304.4 | 116,866 | 116,866 |
| X15 | 78,682 | 532.467 | 6,369.16 | -102,362 | -3,133.79 | -68.2827 | -1.131 | 146.07 | 13,321.3 | 402,089 | 504,451 |
| X16 | 78,682 | 2,364.02 | 11,950.1 | -1,965 | 0.038 | 27.5485 | 186.599 | 1,046.4 | 38,053.1 | 511,729 | 513,694 |
| X17 | 78,682 | 1,773.56 | 8,053.68 | 0.001 | 0.34381 | 13.486 | 81.988 | 629.975 | 30,986.9 | 337,980 | 337,980 |
| X18 | 78,682 | 1,987.26 | 10,419.6 | -317.197 | 0.65781 | 32.8725 | 168.912 | 875.522 | 31,905.7 | 481,580 | 481,897 |

Categorical summaries:

| column | count | unique | top | freq |
| --- | --- | --- | --- | --- |
| company_name | 78682 | 8971 | C_7 | 20 |
| status_label | 78682 | 2 | alive | 73462 |

Complete all-column output: [descriptive_statistics.csv](descriptive_statistics.csv).

## 2. Shape and datatypes

Shape: **78,682 rows × 21 columns**. Financial years: **1999–2018**.

| column | dtype | non_null | missing | positive_infinity | negative_infinity |
| --- | --- | --- | --- | --- | --- |
| company_name | str | 78682 | 0 | 0 | 0 |
| status_label | str | 78682 | 0 | 0 | 0 |
| year | int64 | 78682 | 0 | 0 | 0 |
| X1 | float64 | 78682 | 0 | 0 | 0 |
| X2 | float64 | 78682 | 0 | 0 | 0 |
| X3 | float64 | 78682 | 0 | 0 | 0 |
| X4 | float64 | 78682 | 0 | 0 | 0 |
| X5 | float64 | 78682 | 0 | 0 | 0 |
| X6 | float64 | 78682 | 0 | 0 | 0 |
| X7 | float64 | 78682 | 0 | 0 | 0 |
| X8 | float64 | 78682 | 0 | 0 | 0 |
| X9 | float64 | 78682 | 0 | 0 | 0 |
| X10 | float64 | 78682 | 0 | 0 | 0 |
| X11 | float64 | 78682 | 0 | 0 | 0 |
| X12 | float64 | 78682 | 0 | 0 | 0 |
| X13 | float64 | 78682 | 0 | 0 | 0 |
| X14 | float64 | 78682 | 0 | 0 | 0 |
| X15 | float64 | 78682 | 0 | 0 | 0 |
| X16 | float64 | 78682 | 0 | 0 | 0 |
| X17 | float64 | 78682 | 0 | 0 | 0 |
| X18 | float64 | 78682 | 0 | 0 | 0 |

## 3. Companies and observations per company

Unique companies: **8,971**. Observations per company: **1–20**, median **7**, mean **8.77**.

| observations_per_company | companies |
| --- | --- |
| 1 | 755 |
| 2 | 906 |
| 3 | 756 |
| 4 | 681 |
| 5 | 616 |
| 6 | 573 |
| 7 | 497 |
| 8 | 427 |
| 9 | 402 |
| 10 | 265 |
| 11 | 290 |
| 12 | 295 |
| 13 | 240 |
| 14 | 194 |
| 15 | 186 |
| 16 | 168 |
| 17 | 148 |
| 18 | 158 |
| 19 | 242 |
| 20 | 1172 |

First 15 companies (the complete list is in [company_observation_counts.csv](company_observation_counts.csv)):

| company_name | observations | first_year | last_year |
| --- | --- | --- | --- |
| C_1 | 19 | 1999 | 2017 |
| C_10 | 20 | 1999 | 2018 |
| C_100 | 15 | 1999 | 2013 |
| C_1000 | 20 | 1999 | 2018 |
| C_1001 | 20 | 1999 | 2018 |
| C_1002 | 20 | 1999 | 2018 |
| C_1003 | 20 | 1999 | 2018 |
| C_1004 | 19 | 2000 | 2018 |
| C_1005 | 9 | 2003 | 2011 |
| C_1006 | 13 | 1999 | 2011 |
| C_1007 | 15 | 1999 | 2013 |
| C_1008 | 7 | 1999 | 2005 |
| C_1009 | 20 | 1999 | 2018 |
| C_101 | 20 | 1999 | 2018 |
| C_1010 | 20 | 1999 | 2018 |

## 4. Original status_label distribution

Company-year observations:

| status_label | observations | percent |
| --- | --- | --- |
| alive | 73462 | 93.3657 |
| failed | 5220 | 6.6343 |

Distinct companies (mixed/missing statuses are kept separate if present):

| status_label | companies | percent |
| --- | --- | --- |
| alive | 8362 | 93.2115 |
| failed | 609 | 6.78854 |

These are the original company labels, not independently observed annual bankruptcy events. Repeated years of a failed company must not be counted as separate bankruptcies.

## 5. Within-company status consistency

Companies with a constant, nonmissing status: **8,971/8,971**. Companies with mixed/missing statuses: **0**.

Complete results: [inconsistent_company_status.csv](inconsistent_company_status.csv).

## 6. Missing values, infinite values, and duplicates

| check | count |
| --- | --- |
| missing_cells | 0 |
| rows_with_missing_values | 0 |
| infinite_numeric_cells | 0 |
| rows_with_infinite_values | 0 |
| duplicate_rows_excluding_first | 0 |
| all_rows_in_duplicate_groups | 0 |
| duplicate_company_years_excluding_first | 0 |
| all_rows_in_duplicate_company_year_groups | 0 |

Duplicate counts excluding the first record measure excess rows. The companion counts include all members of a duplicate group. Missingness and infinity counts per column appear in Section 2. Detailed exception CSVs are saved even when empty.

## 7. Consecutive yearly observations

Companies with internal year gaps: **710**. Companies without internal gaps: **8,261**. Missing internal company-years: **1,851** across **810** gap intervals.

Single-record companies: **755**; they have no internal gaps but cannot establish a multi-year history. This check covers each company's first through last observed year, not the full dataset calendar span.

First 15 companies with gaps:

| company_name | observations | first_year | last_year | missing_years |
| --- | --- | --- | --- | --- |
| C_1028 | 12 | 1999 | 2018 | 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013 |
| C_1046 | 13 | 1999 | 2017 | 2003, 2004, 2005, 2014, 2015, 2016 |
| C_107 | 18 | 1999 | 2018 | 2005, 2012 |
| C_1083 | 15 | 1999 | 2014 | 2000 |
| C_1087 | 7 | 1999 | 2006 | 2000 |
| C_1114 | 5 | 2001 | 2007 | 2002, 2003 |
| C_1129 | 6 | 1999 | 2012 | 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007 |
| C_1171 | 6 | 1999 | 2005 | 2004 |
| C_1181 | 10 | 1999 | 2018 | 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014 |
| C_1191 | 19 | 1999 | 2018 | 2010 |
| C_122 | 4 | 1999 | 2003 | 2001 |
| C_1225 | 7 | 1999 | 2008 | 2002, 2003, 2004 |
| C_1236 | 9 | 1999 | 2009 | 2007, 2008 |
| C_1239 | 5 | 1999 | 2004 | 2001 |
| C_1277 | 3 | 1999 | 2002 | 2001 |

Complete company list: [companies_with_year_gaps.csv](companies_with_year_gaps.csv). Individual intervals: [year_gap_intervals.csv](year_gap_intervals.csv).

## 8. Large, small, negative, and zero financial values

Small nonzero values use **0 < abs(value) < 1 in the stored units**. Unusually low/high values use **Q1 − 1.5×IQR / Q3 + 1.5×IQR**, computed separately for each financial variable. Negative, zero, small, and IQR flags may overlap. These are review flags rather than evidence of errors; skewed financial distributions can produce many IQR flags.

| variable | min | median | max | negative_count | zero_count | small_nonzero_count |
| --- | --- | --- | --- | --- | --- | --- |
| X1 | -7.76 | 100.45 | 169,662 | 6 | 0 | 3857 |
| X2 | -366.645 | 103.661 | 374,623 | 6 | 306 | 4221 |
| X3 | 0 | 7.9295 | 28,430 | 0 | 633 | 17515 |
| X4 | -21,913 | 15.0345 | 81,730 | 23012 | 3 | 6873 |
| X5 | 0 | 7.023 | 62,567 | 0 | 19701 | 7680 |
| X6 | -98,696 | 1.616 | 104,821 | 34001 | 7 | 7597 |
| X7 | -0.006 | 22.82 | 65,812 | 1 | 2205 | 9903 |
| X8 | 0.0001 | 227.512 | 1.07339e+06 | 0 | 0 | 1378 |
| X9 | -1,965 | 186.599 | 511,729 | 13 | 0 | 4572 |
| X10 | 0.001 | 213.203 | 531,864 | 0 | 0 | 2225 |
| X11 | -0.023 | 7.5935 | 166,250 | 1 | 20884 | 8853 |
| X12 | -25,913 | 6.518 | 71,230 | 28498 | 0 | 7374 |
| X13 | -21,536 | 63.5815 | 137,106 | 6603 | 25 | 5290 |
| X14 | 0.001 | 43.333 | 116,866 | 0 | 0 | 3567 |
| X15 | -102,362 | -1.131 | 402,089 | 40277 | 0 | 1496 |
| X16 | -1,965 | 186.599 | 511,729 | 13 | 0 | 4572 |
| X17 | 0.001 | 81.988 | 337,980 | 0 | 0 | 2634 |
| X18 | -317.197 | 168.912 | 481,580 | 3 | 1 | 1259 |

Statistical tail flags:

| variable | p01 | p99 | iqr_lower_fence | iqr_upper_fence | below_iqr_fence_count | above_iqr_fence_count |
| --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.066 | 13,626.8 | -599.98 | 1,050.43 | 0 | 10975 |
| X2 | 0.031 | 25,674.4 | -909.226 | 1,560.81 | 0 | 11594 |
| X3 | 0.002 | 1,804.38 | -68.9776 | 118.141 | 0 | 11475 |
| X4 | -110.217 | 6,517.19 | -211.51 | 350.355 | 346 | 11872 |
| X5 | 0 | 3,421.7 | -112.121 | 186.868 | 0 | 12435 |
| X6 | -627.719 | 3,047.57 | -78.7558 | 111.484 | 4835 | 12169 |
| X7 | 0 | 4,848.48 | -189.168 | 324.029 | 0 | 11237 |
| X8 | 0.582091 | 60,436 | -1,779.88 | 3,059.75 | 0 | 11409 |
| X9 | 0.038 | 38,053.1 | -1,500.73 | 2,574.68 | 1 | 11224 |
| X10 | 0.214 | 46,434.3 | -1,663.64 | 2,872.37 | 0 | 11521 |
| X11 | 0 | 12,931.2 | -373.141 | 621.902 | 0 | 12641 |
| X12 | -193.404 | 4,746.19 | -138.366 | 223.178 | 1144 | 12107 |
| X13 | -60.62 | 12,568.8 | -494.808 | 847.404 | 74 | 11232 |
| X14 | 0.266 | 10,304.4 | -312.002 | 543.709 | 0 | 11781 |
| X15 | -3,133.79 | 13,321.3 | -389.812 | 467.599 | 5819 | 12048 |
| X16 | 0.038 | 38,053.1 | -1,500.73 | 2,574.68 | 1 | 11224 |
| X17 | 0.34381 | 30,986.9 | -911.248 | 1,554.71 | 0 | 12366 |
| X18 | 0.65781 | 31,905.7 | -1,231.1 | 2,139.5 | 0 | 11214 |

The five smallest and five largest observations for every financial variable, with company/year identifiers and flags, are in [financial_extreme_examples.csv](financial_extreme_examples.csv). Complete thresholds and counts: [financial_value_flags.csv](financial_value_flags.csv).

Negative earnings and retained earnings may represent real distress. Negative values in X1 (current assets) and X11 (long-term debt) deserve review. Small denominators in X10 (total assets), X14 (current liabilities), and X17 (total liabilities) could produce extreme ratios; their observed minima appear above. No flagged values were automatically removed.

## 9. Identical and highly correlated financial variables

High correlation means **abs(Pearson r) ≥ 0.95 or abs(Spearman rho) ≥ 0.95**. Only financial variables enter these calculations; no company IDs, year, or status encoding are included.

| variable_1 | variable_2 | pearson | spearman | identical_values | mismatching_rows |
| --- | --- | --- | --- | --- | --- |
| X1 | X10 | 0.824172 | 0.959776 | False | 78319 |
| X2 | X9 | 0.975963 | 0.966225 | False | 78657 |
| X2 | X16 | 0.975963 | 0.966225 | False | 78657 |
| X2 | X18 | 0.988994 | 0.977995 | False | 69741 |
| X4 | X12 | 0.973745 | 0.941066 | False | 78049 |
| X9 | X16 | 1 | 1 | True | 0 |
| X9 | X18 | 0.993149 | 0.984331 | False | 78679 |
| X10 | X17 | 0.967443 | 0.960302 | False | 78680 |
| X14 | X17 | 0.897105 | 0.968604 | False | 71666 |
| X14 | X18 | 0.823712 | 0.951635 | False | 78680 |
| X16 | X18 | 0.993149 | 0.984331 | False | 78679 |

**X9 and X16 identical values: True. Mismatching rows: 0/78,682.** Equality is checked directly, without numerical tolerance; matching missing cells would be treated as equal. Each column has 78,682 / 78,682 nonmissing values respectively.

Exact duplicate financial pairs:

| variable_1 | variable_2 | pearson | spearman | identical_values | mismatching_rows |
| --- | --- | --- | --- | --- | --- |
| X9 | X16 | 1 | 1 | True | 0 |

Full matrices: [pearson_correlations.csv](pearson_correlations.csv) and [spearman_correlations.csv](spearman_correlations.csv). All 153 financial-variable pairs, exact-equality checks, and mismatch counts: [financial_variable_pairs.csv](financial_variable_pairs.csv).

Correlation can reflect company size, skew, and repeated company observations. It does not by itself justify removing a variable. Exact duplicates can be excluded from later model inputs; all variables remain in this audit.

## Reproduce

Run from the project directory:

```bash
venv/bin/python test.py
```

Optional arguments: `--data /path/to/american_bankruptcy.csv --output /path/to/report_directory`.
