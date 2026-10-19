# Bankruptcy Prediction: Main Ideas and Project Plan

## Main idea

Study whether a company's financial condition and changes over time help identify approaching bankruptcy. Keep the prediction horizon at **one year**, while using up to three consecutive financial years to build predictors.

The data audit is complete. Data preparation, predictive modeling, association rules, and clustering are planned; their effectiveness has not yet been demonstrated.

## Our three questions

1. **Classification:** Can current financial ratios and historical changes predict bankruptcy in the following fiscal year?
2. **Association rules:** Which financial warning signs occur together before bankruptcy, and how do their frequencies compare with non-bankruptcy observations?
3. **Clustering:** Do financial profiles form groups with different bankruptcy proportions, or do outcome groups overlap?

**Non-bankrupt does not automatically mean financially healthy.** A company can report losses without entering bankruptcy. Financial warnings are predictors; bankruptcy remains the outcome.

## Why we chose the US dataset

- **Company histories:** company IDs and fiscal years let us follow the same business over time. The attached Polish and Taiwanese files lack the identifiers and dates needed to reconstruct comparable histories reliably.
- **Useful feature engineering:** accounting variables allow us to calculate ratios, changes, and repeated warning signs, following the professor's recommendation to investigate financial deterioration.
- **Chronological evaluation:** we can train on earlier years and test on later years.
- **One dataset for all three questions:** financial measures can support classification, warning-pattern discovery, and clustering.

This choice reflects the dataset's fit for studying change over time. It does not guarantee better predictions than the alternatives.

## What we have verified

- **78,682 company-year records**, **8,971 companies**, and **18 financial variables**, covering **1999–2018**.
- **609 failed companies** have **5,220 failed-labeled historical rows**. Those rows are not separate bankruptcy events.
- No missing cells, infinite financial values, duplicate rows, or duplicate company-year records.
- **710 companies have internal year gaps**; complete cells do not imply complete histories.
- **X9 and X16 are identical.**
- Losses, extreme values, and very small denominators require careful handling.

These findings come from the [executed audit report](results/data_audit/report.md).

## Main limitations

- **Bankruptcy timing is inferred:** the original label stays constant throughout each company's history, and individual filing dates are absent. We assume a failed company's final observed financial year immediately precedes bankruptcy. Agreement with published annual bankruptcy counts supports this interpretation but does not verify individual dates.
- **Follow-up is uncertain:** disappearance does not establish bankruptcy, and continued reporting does not independently prove its absence.
- **Events are rare:** the 609 failed companies provide at most 609 assumed events before eligibility restrictions. Annual prediction is more imbalanced than the original row labels suggest.
- **Records are related:** repeated observations belong to the same companies. Filtering endpoints or requiring longer histories can introduce selection bias.
- **Context is limited:** industry information and financial-statement release dates are absent. Historical public-company results may not generalize to current or private businesses.
- **Patterns are associations:** warning combinations and clusters cannot establish causes of bankruptcy.

## Agreed data preparation workflow

1. **Preserve the source data and original labels.** Keep separate working tables and document inclusion, exclusion, and transformations.
2. **Build a separate annual target.** Mark only the final observed year of a failed company positive under our timing assumption. Earlier years are negative only under the assumption that no earlier bankruptcy occurred. Keep target-construction metadata out of predictor inputs.
3. **Apply the documented continuity rule.** Retain assumed positives and candidate negatives with an observation in the immediately following calendar year; exclude other uncertain endpoints. This remains an assumption-based sample, not independently verified follow-up.
4. **Keep one final record per company for exploration.** Use it for initial financial-profile comparisons, while keeping the annual experiment as the main prediction task.
5. **Engineer interpretable ratios.** Start with current assets/current liabilities, liabilities/assets, net income/assets, EBIT/assets, retained earnings/assets, and market value/liabilities. Check derived values for numerical problems.
6. **Make historical features central.** Compare current-year ratios with changes and summaries from two and three consecutive years: rising leverage, falling liquidity or profitability, repeated losses, and declining sales. Use current and past information only; do not fill missing years using future records. Current assets are not a direct measure of cash reserves.
7. **Compare feature sets fairly.** Use the same three-year-history-eligible records for the direct one-, two-, and three-year feature comparison. Separately report coverage on the larger samples.
8. **Handle quality without erasing distress.** Preserve valid losses and zeros, investigate questionable values, and omit duplicate predictor X16 from model inputs.
9. **Compare outlier treatments and scale appropriately.** Compare unchanged ratios with training-fitted 1st–99th percentile clipping. Use scaling for KNN, K-means, and the neural network; decision trees do not require it. Select preparation settings using validation data.
10. **Create warning flags before clipping or scaling.** Examples include negative net income, negative retained earnings, negative EBITDA, liabilities/assets above 0.8, and current ratio below 1. These thresholds are working definitions, not universal danger boundaries.
11. **Split chronologically.** Use 1999–2011 for training, 2012–2014 for validation, and 2015–2017 for testing. Under our continuity rule, 2018 retains 36 assumed positives and no negatives, so report it separately. This deliberately differs from the paper's test period.
12. **Prevent information leakage and address imbalance.** Learn transformations on training data only. Compare class weighting where supported, preserve evaluation class proportions, and keep the test outcomes for final evaluation. Do not rebalance the main association or clustering samples.

Before additional history restrictions, the conservative 1999–2017 sample contains **69,474 records and 573 assumed events**. Continued reporting and endpoint filtering do not remove outcome uncertainty or selection bias.

## Modeling and evaluation plan

| Question | Planned method | What we will assess |
|---|---|---|
| Next-year bankruptcy | Decision tree, KNN with different k values, Naive Bayes, and neural network | Whether financial histories improve prediction over current-year features and an always-negative baseline |
| Warning combinations | Apriori on warning flags | Support, confidence, lift, and actual case counts; check patterns on separate records |
| Financial groups | K-means on selected, prepared financial features | Financial profiles, bankruptcy proportions, silhouette, and agreement with outcomes |

For classification, report confusion matrices, accuracy, precision, recall, F1, ROC-AUC, and precision–recall curves/average precision. Accuracy alone is insufficient for rare events. Add a separate evaluation holding out entire companies to assess performance on unfamiliar businesses.

For clustering, exclude labels and identifiers when forming groups; examine outcomes afterward. Mixed clusters are a possible finding. For annual rules and clusters, interpret outcomes using the reconstructed annual target and report distinct company counts alongside row counts.

## Expected contribution and scope

Our contribution is to test whether **financial deterioration adds useful information beyond a single-year snapshot**, then explain warning combinations and overlapping financial profiles. We will report results honestly even if trends do not improve prediction or bankruptcy cases do not form separate clusters.

Longer forecast horizons, advanced trajectory methods, and an Altman Z-score benchmark remain optional future work. The final presentation will distinguish audited facts, assumptions, and experimental results, and document AI assistance.

See the [assignment requirements](project.md) and [detailed preparation decisions](data_preparation_decisions.md) for supporting detail.
