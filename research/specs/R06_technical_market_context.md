# R06 — Technical Features, Research Baseline and Market/Sector Context: Vietnam Evidence

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | Quant engineer |
| Effort budget | ~8 agent-hours |
| Feeds | P2 (features, market view), P3 (baseline, model inputs) |
| Acceptance checks | A20, A25, A28 |

## Why this matters

The handoff asks for a small, documented feature set and a transparent baseline: a 20-session relative-strength rank plus one trend/setup filter, **frozen before evaluation** (§9.2). This track grounds those choices in published evidence on Vietnamese (and comparable frontier/emerging, price-limited) markets, so the baseline isn't picked by tuning many variants.

## Read first

Handoff §8.1, §8.3, §8.4, §9.1–§9.2, §11 (liquidity screen), §18.2.

## Research questions

1. **Momentum and reversal evidence in Vietnam.** Academic studies on cross-sectional momentum, short-term reversal, 52-week-high effects, and industry momentum on HOSE/HNX. What horizons, holding periods and liquidity filters do they use, and how do they handle costs? Does the evidence support a 5–20 session horizon or argue against it?
2. **Price limits and their effects.** Literature on daily price limits (magnet effect, delayed price discovery, volatility spillover) in Vietnam, China and Taiwan. What does it imply for features measured around limit-hit days and for labels?
3. **Liquidity and size.** Evidence on illiquidity premia and implementability in VN. Is the handoff's VND 10 billion median 20-session matched-turnover screen reasonable? Roughly how many tickers pass it (from any public statistic)?
4. **Feature set v1.** Propose ≤ 20 features, each with: definition, lookback/warm-up, adjustment basis (raw vs adjusted), missing-data behavior, and the literature support. Cover returns/momentum, MA distance, volatility/ATR, relative volume/turnover, relative strength vs index and sector, breakout/pullback distance.
5. **Baseline rule.** Recommend one precise baseline: the formula, universe filter, rebalance/entry convention, and exit. Give the reasons for choosing it over two alternatives. It must be fully specified before any data is seen.
6. **Market and sector context.** Evidence for breadth/regime indicators (index vs 50-session MA, % of stocks above their 20-session MA) in VN. Sector classification options and how to represent overlapping themes (Banks, Securities, Real Estate, Steel, Public Investment). Should the regime feed the model as a feature only (the handoff's default)?
7. **Explanations.** Deterministic templates for reasons ("RS rank top 10% of covered universe over 20 sessions…"). Can SHAP-style attributions on LightGBM be shown without implying causation?

## Deliverable

`research/findings/R06_findings.md` with: an annotated bibliography (≥ 8 relevant papers or reports, each summarized in 2–3 lines with market, period, method and finding), Feature set v1 table, a frozen baseline spec, and a market-context panel spec.

## Out of scope

Running backtests on real data, intraday features, sentiment/news/social features (excluded in §3.3), and opaque "smart money" scores.

## Method and starting sources

Google Scholar / SSRN / RePEc searches ("Vietnam stock momentum", "HOSE price limit", "Vietnam liquidity premium"), Vietnamese university journals (e.g., Journal of Asian Business and Economic Studies, Journal of Economics and Development), and IMF/World Bank frontier-market notes.

## Known traps

- A paper's in-sample alpha is not evidence for this project.
- Studies that ignore the transaction tax, price limits or survivorship.
- Tuning the baseline after looking at results.
