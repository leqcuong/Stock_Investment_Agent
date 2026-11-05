# R08 — ML Methodology: Labels, Purged Validation, Ranking Metrics, Overfitting Controls

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | ML / research engineer |
| Effort budget | ~8 agent-hours |
| Feeds | P3 |
| Acceptance checks | A07, A08, A20, A21, A26 |

## Why this matters

The handoff sets a strict contract (§9): next-session entry, a 10-session label, date-grouped walk-forward, purging by actual label windows, an untouched holdout, baseline comparison, and no fake probabilities. This track turns that contract into concrete, citable methods and a **promotion rubric frozen before the holdout is examined**.

## Read first

Handoff §8.4, §9 (all), §10.2 (score labeling), §14.

## Research questions

1. **Label design.** Compare the open-to-open 10-session forward return (handoff example), close-to-close with a next-open entry, cross-sectionally demeaned/ranked returns, and triple-barrier labels. Recommend Label spec v1 with exact timing, cost deduction, and handling of suspensions, missing exits and delistings (§9.3).
2. **Validation design.** Purged and embargoed K-fold vs walk-forward expanding/rolling windows vs combinatorial purged CV (CPCV). How do you purge using actual label windows in a ticker-stacked panel? Recommend fold sizes given realistic VN history depth (from R02: roughly 8 years in the free tier?). Specify the final holdout length.
3. **Model setup.** LightGBM regression vs LambdaRank/`rank_xendcg` for cross-sectional ranking. Per-date target normalization. Handling of missing features natively vs imputation inside folds. Hyperparameter search budget appropriate to the sample size.
4. **Metrics.** Rank IC / ICIR (Spearman per date), top-k minus universe spread, hit rate by decile, stability by year/sector/regime. Recommend the primary metric and what "credible value over baseline" means statistically (e.g., a t-stat of mean IC across dates, using a block bootstrap).
5. **Multiple testing.** Deflated Sharpe Ratio, Probability of Backtest Overfitting (PBO), White's Reality Check / Hansen SPA. Which is practical for a solo project? Propose an experiment-tracking rule (log every trial).
6. **Calibration (later).** When, if ever, could a score be shown as a probability? Which methods (isotonic, Platt) apply, on which held-out data, and under what conditions?
7. **Model card.** Recommend a template (e.g., Mitchell et al. *Model Cards*), adapted to trading: data period, universe limits, survivorship, costs, leakage controls, and measured vs assumed results.
8. **Retraining.** Versioned schedule (e.g., quarterly) vs drift-triggered. How do you keep prior forecasts immutable and the inference schema compatible?

## Deliverable

`research/findings/R08_findings.md` with: Label spec v1, a split-design diagram (in text) with dates parameterized, a metric definition sheet, a **draft promotion rubric** (to be frozen by the Tech Lead before any holdout look), a multiple-testing approach, and a model-card template outline.

## Key references to consult

- López de Prado, *Advances in Financial Machine Learning* (purging, embargo, CPCV, triple barrier).
- Bailey and López de Prado on the Deflated Sharpe Ratio.
- Bailey et al. on PBO.
- Gu, Kelly and Xiu, "Empirical Asset Pricing via Machine Learning".
- Studies applying ML cross-sectional ranking to China A-shares or emerging markets.
- The LightGBM ranking documentation.
- Mitchell et al., "Model Cards for Model Reporting".

## Known traps

- Purging by row count instead of label dates.
- Fitting scalers on all data.
- Selecting features on the full sample.
- Calling a percentile a probability.
- Dropping delisted losers from labels.
