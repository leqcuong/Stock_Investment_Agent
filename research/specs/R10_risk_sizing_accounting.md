# R10 — Risk Sizing, Portfolio Constraints and Performance Accounting

| Field | Value |
| --- | --- |
| Wave / priority | 2 (smaller track — the handoff already specifies most of it) |
| Owner role | Financial risk specialist |
| Effort budget | ~4 agent-hours |
| Feeds | P4, P5 (Holdings/Research screens), P6 (pilot report) |
| Acceptance checks | A16, A18, A23, A24 |

## Why this matters

Handoff §11 gives proposed limits and a sizing formula. This track checks them against established practice, defines the stress scenarios and theme-overlap method precisely, and picks a performance-accounting method that handles deposits and withdrawals (A23). It does **not** choose the user's limits; those stay editable research defaults.

## Read first

Handoff §11, §18.2, §20.2–§20.4, §14 (A16, A18, A23, A24).

## Research questions

1. **Fixed-fractional sizing.** Review practitioner and academic treatment of fixed-fractional risk-per-trade, ATR-based stops, and why Kelly is excluded. Confirm that the §11 formula (`min` of planned-risk, stress, cash, name, sector, liquidity, heat, and joint-stress quantities, floored to lot) has no gaps. For example: does pending-order exposure count, and how are odd lots handled?
2. **Stress scenarios.** Define the "selected adverse scenario" concretely for VN: consecutive limit-down days (−7% ×3 ≈ −19.6% for HOSE), historical worst sector drawdowns (e.g., 2022 Real Estate/Securities), and gap risk. Recommend per-position and joint (correlated/sector) scenarios with sources.
3. **Overlapping themes.** Methods to measure concentration when a stock belongs to multiple themes: count full exposure in each theme vs fractional weights. Recommend one and justify why it does not understate concentration (§7.1).
4. **Portfolio heat and joint stress.** Standard definitions, and how to include unsettled and pending positions.
5. **Performance accounting.** Time-weighted return (daily valuation) vs Modified Dietz vs money-weighted IRR for a retail account with irregular deposits. A drawdown series based on cash-flow-adjusted equity. Recommend one method, with formulas. (A23)
6. **Drawdown response.** Evidence for or against drawdown-based risk scaling (the handoff halves risk at 4% and pauses at 6%). Present this as a behavioral guardrail, not an edge.
7. **Margin (reporting only).** Which debt/collateral fields are needed before labeling risk "complete" when existing margin exists.

## Deliverable

`research/findings/R10_findings.md` with: a verified sizing algorithm (pseudo-code with all inputs and their unknown-handling), a stress-scenario table, a theme-overlap method, a performance-accounting method with formulas, and a list of risk-completeness preconditions.

## Out of scope

Choosing the user's actual limits, broker-specific margin call simulation, and optimization-based portfolio construction.

## Known traps

- Treating a missing equity value as zero.
- Rounding up to a lot.
- Ignoring costs in risk per share.
- Counting a deposit as performance.
