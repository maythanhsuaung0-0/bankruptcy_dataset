# American Bankruptcy Dataset: Findings and Data Preparation Decisions

Updated: October 14, 2026.

This document summarizes our discussion, findings from `data/american_bankruptcy.csv`, and preparation decisions. It accompanies the assignment instructions in [project.md](project.md). The calculations below are exploratory audits; no classifiers, association-rule models, or clustering models have been trained yet.

The nine data-understanding checks are implemented in [test.py](test.py) and were run against the original CSV. The [executed audit report](results/data_audit/report.md) contains descriptive statistics, column datatypes, company and status counts, data-quality checks, year-gap findings, financial-value flags, and correlation results. Complete company lists and supporting tables are saved alongside the report. Reproduce the results from the project directory with `venv/bin/python test.py`. The audit preserves all original rows, labels, and financial variables.

## 1. Our three questions

1. **Classification:** Can we predict whether a company will go bankrupt in the next fiscal year using its financial data?
2. **Association rules:** Which financial warning signs commonly occur together before bankruptcy, and are these combinations more common than among non-bankrupt companies?
3. **Clustering:** Do companies form distinct financial groups, or do bankrupt and non-bankrupt companies mix within the same clusters?

The next-year interpretation depends on the target-construction assumptions below. In this project, a financial warning is an indicator, while bankruptcy is the outcome. A company can report losses without filing bankruptcy. We will not replace the bankruptcy target with a subjective healthy/unhealthy score.

## 2. Verified findings from our CSV

- **78,682 company-year records**, **21 columns**, and **18 financial variables**, covering **1999–2018**.
- **8,971 distinct company IDs** in the actual file.
- **73,462 alive-labeled rows** and **5,220 failed-labeled rows**. Failed rows account for **6.63%** of all rows.
- **8,362 alive-labeled companies** and **609 failed-labeled companies**. Failed companies account for **6.79%** of companies.
- **No missing cells, infinite financial values, duplicate rows, or duplicate company-year records**.
- Every company has the same original status label throughout its recorded history.
- Company histories contain **1–20 observations**, with a median of **7**. There are **755 companies with one record** and **710 companies with year gaps**.
- **X9 and X16 are exactly identical** throughout the file.
- Negative financial results are common: **34,001 rows have negative net income**, **40,277 have negative retained earnings**, and **23,012 have negative EBITDA**.
- Assets, current liabilities, and total liabilities are positive throughout the file, but each reaches a minimum of **0.001**. Very small denominators can create extreme ratios.
- **5,675 alive-labeled companies stop appearing before 2018**. The CSV does not explain each disappearance.

### Descriptive differences in final observed records

These calculations use one final record per company. They are full-sample descriptions, not held-out predictive results.

| Measure | Alive label | Failed label |
|---|---:|---:|
| Percentage reporting a net loss | 52.74% | 85.22% |
| Median current ratio | 1.67 | 0.93 |
| Median liabilities/assets | 0.56 | 0.91 |

The groups differ financially, but they overlap. An alive label does not establish financial strength, and a warning does not establish bankruptcy.

### What the documentation supports

The authors describe financial information from the year before bankruptcy as the input for a next-year target. They report 8,262 companies, which differs from our 8,971 IDs. We will report our actual count and acknowledge this discrepancy. [Authors' documentation](https://github.com/sowide/bankruptcy_dataset)

In our CSV, counting failed companies by their final observed year and shifting that year forward by one reproduces all 20 annual bankruptcy counts in Table 1 of the paper. For example:

| Final financial year | Inferred bankruptcy year | Our count | Published count |
|---|---:|---:|---:|
| 1999 | 2000 | 3 | 3 |
| 2007 | 2008 | 59 | 59 |
| 2010 | 2011 | 35 | 35 |
| 2018 | 2019 | 36 | 36 |

This supports the inference that failed-company histories end in their pre-bankruptcy year. Agreement in aggregate does not independently verify individual filing dates. [Original paper, Table 1](https://air.unipr.it/bitstream/11381/2933563/5/futureinternet-14-00244-v2.pdf)

## 3. Limitations we must carry into the analysis

- **Event dates are inferred.** The CSV has a company-wide status label rather than an explicit filing date or a year-specific bankruptcy target.
- **Follow-up is uncertain.** A missing next-year record does not establish bankruptcy. A next-year record establishes continued reporting, but does not independently prove absence of bankruptcy; Chapter 11 businesses may continue operating.
- **The annual target is much more imbalanced.** Marking only the final failed record positive gives 609 assumed events, not 5,220 separate events. Across all original rows, that is about **0.77%**.
- **Rows are dependent.** Multiple records belong to the same company. The effective number of distinct failed businesses is 609.
- **Final-record selection is retrospective.** Choosing an endpoint uses knowledge of where a history ends, and the reasons for ending may differ across outcome groups.
- **Missing years are different from missing cells.** The absence of blank values does not make the histories complete.
- **Extreme values can be errors or real distress.** Blanket removal risks deleting useful bankruptcy information.
- **Industry and release-date context are absent.** We cannot fully adjust thresholds for industry or establish the exact date each financial statement became available.
- **Coverage is historical and limited to the documented US public-company population.** Results do not automatically transfer to current or private companies.
- **Association does not establish causation.** Financial patterns may be associated with bankruptcy without explaining why it happened.

## 4. Final data preparation decisions and why they help

- **Keep the original data unchanged and preserve its labels.** Create working tables and record each transformation. **Why:** this makes the analysis reproducible and lets us distinguish supplied information from assumptions we introduced.

- **Use reconstructed company-year observations for the main next-year experiment.** Add a separate `bankruptcy_next_year` target. For a failed company, assume its final observed year immediately precedes its bankruptcy year; mark only that financial year positive. Earlier observations are negative under the assumption that no earlier bankruptcy occurred. **Why:** this aligns observations with the one-year question instead of labeling every historical year as a next-year event. The target remains inferred.

- **Keep final records as an exploratory baseline.** Preserve a separate table with 8,971 companies and 609 failed labels. **Why:** it provides a manageable comparison without repeated-company weighting, and is useful for initial warning-pattern and cluster exploration. It does not replace the main annual experiment or remove selection bias. The main predictive baseline uses single-year features on the same eligible company-year records as the historical-feature models.

- **Mark uncertain outcomes rather than silently labeling them negative.** Keep an eligibility indicator and the reason a record is included or excluded. **Why:** disappearing companies and dataset endpoints should not automatically become confirmed non-bankruptcy cases. The conservative continuity rule and its limits are described in Section 5.

- **Use current financial ratios and consecutive-year changes as the main numerical feature comparison.** Start with the six ratios below, then engineer changes and summaries from two and three consecutive past financial years, including the prediction record's year. **Why:** levels express current condition, while historical changes let us test whether deterioration or persistent losses add predictive information. Ratios do not eliminate industry effects or tiny-denominator problems.

- **Compare feature sets on the same eligible prediction records.** Evaluate single-year ratios versus ratios plus historical features on a common history-eligible sample. Separately report the broader single-year sample as a coverage benchmark. **Why:** changing both the features and the companies at the same time would make it unclear whether any improvement comes from better predictors or a different sample.

- **Remove exact duplication and inspect correlated features.** Drop X16 from model inputs if raw financial columns are retained, because it duplicates X9. Compare correlations among engineered features before adding more variables. **Why:** duplicated and closely related inputs can overemphasize a financial characteristic, especially in distance calculations and Naive Bayes.

- **Preserve valid negative and zero values; flag questionable records.** Keep losses, negative retained earnings, and legitimate zero inventory or debt. Investigate unusual negatives in fields such as current assets. Do not replace values without evidence. **Why:** the conditions we are investigating can look unusual, so automatic cleaning could erase distress signals.

- **Compare unchanged ratios with controlled outlier treatment.** Test an uncapped preparation against clipping at training-data 1st and 99th percentiles. Record how many values and bankruptcy cases are affected. **Why:** this controls extreme numerical influence while showing whether conclusions depend on compressing genuine distress. Select the preparation using validation data.

- **Scale numerical inputs for distance-based methods and the neural network.** Start with clipping plus `StandardScaler`; compare an uncapped `RobustScaler` preparation where useful. Decision trees do not require scaling. **Why:** KNN and K-means should not be dominated by a feature's numerical range. Robust scaling protects its fitting statistics but does not remove extreme observations.

- **Create warning flags from original financial values before clipping or scaling.** Use the flags below for Apriori. **Why:** categories such as a net loss retain their financial meaning and can be explained in ordinary language. Fixed thresholds are chosen definitions, not universal danger boundaries.

- **Split chronologically before learning transformations.** Use earlier financial years for training and later years for validation and testing. Keep company ID, original label, final-history year, inferred event year, and eligibility metadata out of predictor inputs. Year defines the split but is excluded from the initial feature set. **Why:** neither future financial information nor metadata used to construct the target should reveal the answer. [Preprocessing guidance](https://scikit-learn.org/stable/common_pitfalls.html)

- **Add company-disjoint evaluation as a separate check.** In the annual experiment, an existing company may legitimately have earlier training records and later test records. Separately hold out whole companies to assess transfer to unfamiliar businesses. **Why:** future-period prediction and unseen-company prediction are different evaluation questions; a random row split does not address either reliably.

- **Start with original class proportions and compare class weighting where supported.** Keep validation and test proportions unchanged. Postpone oversampling or SMOTE until a baseline exists; any resampling belongs inside training data or training folds. **Why:** this addresses rare events without changing the evaluation population. Do not rebalance the main association-rule or clustering samples, since that changes prevalence and rule confidence. [Resampling guidance](https://imbalanced-learn.org/stable/common_pitfalls.html)

- **Keep a one-year forecast horizon and make historical feature engineering central.** Build one feature row per company and prediction year using current and past measurements only. Calculate changes from actual consecutive years; do not fill missing years with zeros or interpolate using future records. Record the cases lost by history requirements. **Why:** this follows the professor's advice to focus on stronger predictors for next-year bankruptcy rather than adding multi-year forecast horizons. Improvement must still be tested.

- **Exclude post-entry records from a first-bankruptcy prediction population.** Historical feature windows must precede the assumed event. If verified dates later identify records at or after bankruptcy entry, exclude them from the first-entry task rather than automatically assigning zero or continuing a positive label. **Why:** predicting entry and describing an existing bankruptcy are different tasks. Under our inferred-endpoint convention, no records follow the inferred event; this does not independently verify the absence of actual post-filing records.

### Initial numerical features

| Feature | Formula | Financial interpretation |
|---|---|---|
| Current ratio | X1 / X14 | Short-term assets relative to short-term obligations |
| Liabilities/assets | X17 / X10 | Obligations relative to assets |
| Net income/assets | X6 / X10 | Profit or loss relative to company size |
| EBIT/assets | X12 / X10 | Earnings before interest and taxes relative to assets |
| Retained earnings/assets | X15 / X10 | Accumulated retained earnings or deficit relative to assets |
| Market value/liabilities | X8 / X17 | Market valuation relative to obligations |

Check that all derived values are finite. Scaling does not make a distribution normal. Ordinary logarithms cannot be applied directly to negative earnings.

### Initial association-rule flags

| Flag | Definition |
|---|---|
| Net loss | X6 < 0 |
| Negative retained earnings | X15 < 0 |
| Negative EBITDA | X4 < 0 |
| High leverage | X17 / X10 > 0.8 |
| Low current ratio | X1 / X14 < 1 |

**Correction to the classmate's suggestion:** X5/X14 measures inventory/current liabilities. A low value alone does not establish poor liquidity. Use X1/X14 for the initial current-liquidity flag.

### Professor's feedback: history length versus prediction horizon

The prediction horizon stays at **one year**. The input history can cover **one, two, or three consecutive financial years**. For example, information from 2008–2010 can be combined into one prediction row for bankruptcy in 2011. Historical measurements and summaries are features; future outcomes and reconstructed event dates are not features.

The main comparisons are:

- **Single-year model baseline:** the current financial ratios.
- **Two-year history:** current ratios plus changes from the previous financial year.
- **Three-year history:** selected changes, averages, and persistent-warning patterns across three consecutive years.

Candidate features include change in liabilities/assets, change in long-term debt/assets (X11/X10), change in current ratio, change in net income/assets, number of loss-making years, and sales declining in two consecutive years. Compute them within each company using past data. Warning patterns for Apriori come from original measurements before clipping or scaling.

Adapt the professor's examples to the available columns:

- **Cash reserves are not supplied directly.** X1 is current assets, not cash. Use liquidity features without claiming that they measure actual cash reserves.
- **Liabilities and debt are different.** X17 is total liabilities; X11 is long-term debt. Use precise names when interpreting their changes.
- **Equity is not supplied directly.** X10 minus X17 is a book-equity proxy, but is nonpositive in 7,794 original rows. Do not naively divide by it. Start with liabilities/assets and long-term debt/assets; any equity-based extension needs an explicit rule for undefined or misleading ratios.

Under the conservative annual-sample rule in Section 5, ending in 2017, history requirements retain:

| History required, including current year | Eligible prediction records | Assumed bankruptcy events |
|---|---:|---:|
| One financial year | 69,474 | 573 |
| Two consecutive financial years | 60,805 | 558 |
| Three consecutive financial years | 53,220 | 529 |

Fewer usable events reflect sample eligibility, not a reduction in actual bankruptcies. Longer-history samples may favor companies with longer or more complete reporting histories. For a direct three-way feature comparison, use the three-year-eligible records for all three versions; separately show coverage on the larger samples. All model settings and preparation choices are selected on training/validation data, leaving the test outcomes for final evaluation.

The professor's concern is addressed in the **revised study design**, not yet demonstrated by model results. The original emphasis on optional trends has been replaced with this central feature-engineering comparison.

## 5. Conservative annual-sample rule and the final-year boundary

This is an implementation default that makes our treatment of uncertain endpoints explicit. It does not independently validate outcomes.

- **Positive:** the final observed record of a company labeled failed, using the inferred event timing.
- **Candidate negative:** a record with another observation for the same company in the immediately following calendar year, combined with the reconstructed event timing and original company status.
- **Unknown/excluded:** other records without sufficient continuity under this rule, including alive-company final records.

The negative interpretation assumes the supplied status and reconstructed timing correctly describe the bankruptcy outcome. Continued reporting alone is insufficient. Keep this assumption and selection bias visible in the report.

This rule produces **69,510 candidate records**, with **609 positives**, **68,901 negatives**, and **9,172 excluded records**. It contains **8,187 companies**. These counts describe a proposed sample, not verified event labels.

### Boundary handling

The authors use financial years 2015–2018 for testing. Under our continuity rule, however, 2018 retains **36 positives and zero negatives**, because the file has no 2019 financial records.

For this conservative version, before the additional history-window eligibility restrictions in Section 4, use:

| Group | Financial years | Records | Assumed positives | Candidate negatives |
|---|---|---:|---:|---:|
| Training | 1999–2011 | 51,244 | 403 | 50,841 |
| Validation | 2012–2014 | 9,603 | 87 | 9,516 |
| Testing | 2015–2017 | 8,627 | 83 | 8,544 |

- This gives **69,474 records**, including **573 assumed events**, for the primary conservative experiment.
- Report the 36 assumed events associated with 2018 separately. Do not include a positive-only year as though it were a comparable complete annual population.
- Extend the test through 2018 only if the negative-case horizon is supported by additional outcome documentation or follow-up; identify that as a different sample policy.
- This is a deliberate difference from the paper's test period. Do not claim exact reproduction of its experiment or benchmark scores.
- This filtering also excludes companies that stop reporting for other reasons. It reduces endpoint ambiguity but can introduce reporting/survival selection bias.

## 6. Preparation products for the three questions

| Product | Contents | Use |
|---|---|---|
| Audit and reference table | Original fields, company/year keys, anomaly flags, inferred timing, and eligibility reasons | Traceability and limitation reporting |
| Final-record baseline | One record per company, original outcome, and financial features | Initial bankruptcy-profile comparison |
| Annual numerical table | Eligible company-years, numerical ratios, and a separate inferred target | Main classification experiment |
| Annual warning table | Original-value Boolean flags and a separate inferred target | Warning combinations and association with assumed events |
| Clustering input | Numerical ratios without status, inferred target, IDs, or target-construction metadata | Financial groups; examine outcomes after clustering |

Keep the observation unit visible. A company-level rule describes companies; an annual rule describes company-year observations. Their support, confidence, and outcome proportions are not directly interchangeable. If using annual clusters or rules, report distinct company counts as well as row counts so repeated histories are visible.

For annual comparisons, a negative target means no event in the following year under our assumptions. It can include earlier observations of a company that eventually fails. Use the reconstructed annual target to interpret annual rules and clusters; use the original company status to interpret the final-record baseline. Do not mix these two outcome definitions.

## 7. How this fits the assignment

The assignment requires feature selection, target definition, normalization, and quality control. The decisions above cover these preparation requirements.

- **Classification:** compare decision tree, KNN with different k values, Naive Bayes, and a neural network, as required by the final assignment.
- **Association rules:** discover warning combinations on training data, then check support, confidence, lift, and counts on separate records.
- **Clustering:** form clusters without bankruptcy labels; examine financial profiles and bankruptcy proportions afterward. Use silhouette, ARI, and a PCA illustration as supporting evidence. Purity alone is misleading: one cluster containing the entire baseline would already have 93.21% purity.
- **Evaluation:** report confusion matrices, accuracy, precision, recall, F1, ROC and precision-recall curves, and average precision. Include an always-negative baseline. Accuracy alone is especially weak for the reconstructed annual target.
- **AI appendix:** describe how AI assisted exploration, preparation planning, and writing. Distinguish audited observations from proposed or untested methods.

## 8. Other ideas discussed

- **Altman Z-score:** retain as an optional benchmark. Check the chosen version's applicability; industry labels are absent. Do not promise that machine learning will outperform it.
- **More advanced financial trajectories:** extend beyond the central two-/three-year feature comparison only if time permits. For the separate final-record exploratory sample, requiring three consecutive years retains 7,101 companies, including 564 failed companies. These counts differ from annual prediction-record counts.
- **Different forecast horizons:** keep outside the main project, following the professor's advice. They require separate outcome definitions and follow-up decisions. Marking two years positive changes the horizon and should not be presented as the same one-year task.
- **Financial archetypes:** interpret clusters from measured profiles, such as high leverage and low profitability; do not assume distressed companies will separate cleanly.
- **Florida–UCLA–LoPucki alternative:** the previously inspected file has actual filing dates but is a bankruptcy-case database without a non-bankrupt comparison sample. It does not directly replace our dataset for all three questions, and anonymous company IDs prevent a direct reliable join. [Official coverage](https://www.lopucki.law.ufl.edu/contents_of_the_webbrd.php)

## 9. Suggested wording for the preparation section

> We will preserve the original dataset and prepare a final-record exploratory sample alongside a reconstructed company-year dataset for the main next-year experiment. We will interpret failed companies' final financial years as pre-bankruptcy years, document uncertain follow-up, and apply an explicit sample-eligibility rule. We will compare current financial ratios with features engineered from two and three consecutive past years, while keeping a one-year prediction horizon and evaluating feature sets on the same eligible records. We will also create warning flags, retain meaningful negative and zero values, compare outlier treatments, and learn numerical transformations from training data only. Evaluation will use later periods, with an additional company-disjoint check. Conclusions will acknowledge inferred outcomes, reporting selection, history requirements, historical coverage, and missing industry context.

The final decision is to keep bankruptcy as the outcome, reconstruct an annual target with explicit assumptions, and make consecutive-year feature engineering a central experiment following the professor's feedback. Final records support exploration; single-year features on matching annual records provide the predictive baseline. We have selected a defensible workflow; predictive accuracy and useful patterns remain to be established by modeling and evaluation.
