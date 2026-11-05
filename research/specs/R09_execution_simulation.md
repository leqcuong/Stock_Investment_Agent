# R09 — Execution Simulation and Backtest Realism on Daily Bars

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | Risk engineer / quant engineer |
| Effort budget | ~6 agent-hours |
| Feeds | P3 (policy evaluation), P4 (simulator) |
| Acceptance checks | A10, A11, A12, A13, A14, A15, A17, A18, A24 |
| Depends on | R03 (rules tables); re-check against R04 (framework choice) |

## Why this matters

Model ranking quality and executable-policy performance are evaluated separately (§9.3). With daily OHLCV only, the simulator must not invent fills: no favorable intrabar ordering, no sales during floor locks, and no selling of unsettled shares. This track finds established conservative conventions and slippage/impact models suited to a thin, price-limited market.

## Read first

Handoff §5, §9.5, §10.1, §11, §14 (A10–A18, A24), and R03 findings when available.

## Research questions

1. **Fill conventions.** Literature and framework defaults for daily-bar fills: next-open, VWAP proxy, limit-order touch rules ("touch ≠ fill"; require trade-through by one tick?). Recommend a primary convention plus sensitivity variants.
2. **Ambiguous bars.** Conventions when the stop and target are both inside the high-low range (worst-case first, open-proximity heuristics, or marking indeterminate). (A14)
3. **Limit-locked days.** How to detect probable floor-/ceiling-locked sessions from daily data (close = floor, low = high, volume patterns), and how studies treat unfillable exits and entries. (A11, A12)
4. **Gap handling.** Entry when the open gaps outside the planned interval: skip, reassess, or wait. (A13)
5. **Slippage and impact.** Simple, defensible models for VN mid/small caps: a fixed-bps spread proxy, a square-root impact model with an ADV/turnover participation cap (handoff: ≤ 0.1% of median turnover). Any VN or emerging-market estimates of effective spreads?
6. **Settlement and cash in simulation.** Lot-level T+2 sellability, unsettled sale proceeds, and sequential capital reservation when signals compete (A24). How do existing frameworks (from R04) handle T+N, or what must be custom?
7. **Corporate actions in backtests.** Raw prices with explicit CA events vs adjusted prices. Which avoids double counting dividends while keeping lot/tick/band logic on raw prices? (A15)
8. **Reporting.** Which execution-realism metrics to report (unfilled/partial/delayed exits, indeterminate bars, stale marks) and how to present liquidation uncertainty.

## Deliverable

`research/findings/R09_findings.md` with: a simulator rule-book (each rule: condition → action → rationale → source), a list of sensitivity scenarios, a slippage model with parameters as explicit assumptions, and the CA price-basis recommendation.

## Out of scope

Intraday/tick simulation, order-book modeling, and market-making.

## Known traps

- Filling at the signal bar's close.
- Treating a locked position as cash.
- Assuming the stop price equals the exit price.
- Applying adjusted prices to tick/band checks.
