# R03 — Vietnam Market Mechanics, Calendar and Trading Costs (Reference Data)

| Field | Value |
| --- | --- |
| Wave / priority | 1 |
| Owner role | Vietnam market specialist / risk engineer |
| Effort budget | ~6 agent-hours |
| Feeds | P1 (calendar), P4 (settlement, simulator, sizing) |
| Acceptance checks | A09, A10, A12, A13, A15, A17, A18, A28 |

## Why this matters

The simulator, settlement logic and sizing must encode current rules exactly, each with an effective date. The handoff summarizes them (§5) and asks to verify. This track produces **versioned reference tables** that P1/P4 can turn into config without further research.

## Read first

Handoff §5, §9.5, §11, §20.3, §21 (S9–S13).

## Research questions (each answer = a table with an effective date and a source)

1. **Trading calendar.** Official holiday schedule source for 2026 (and how future years are announced); a historical holiday list back as far as history is used; ad-hoc closures. Recommend how to maintain the calendar (manual versioned file vs library — check e.g. `exchange_calendars`/`pandas_market_calendars` coverage of XSTC/HOSE).
2. **Sessions.** Current session times per board (ATO, continuous, lunch break, ATC, put-through, post-close) on HOSE (post-KRX), HNX, UPCoM.
3. **Price bands and reference prices.** HOSE ±7%, HNX ±10%, UPCoM ±15%. First-day listing and post-suspension bands. Ex-rights reference-price adjustment formula. The UPCoM reference definition (weighted average). Rounding rules for ceiling/floor.
4. **Tick sizes and lots.** Tick-size schedule by board and price tier (stocks vs ETFs/CW), board lot (100), odd-lot trading rules, and maximum order size.
5. **Settlement.** T+2 mechanics; when purchased shares become sellable (the time of day on T+2), and when sale proceeds become usable or can be advanced. How holidays shift this. Any 2025–2026 changes (e.g., the non-pre-funding scheme for institutional investors and its relevance to retail). (A09, A10)
6. **Order types and priority.** LO, ATO, ATC, MP/MTL/MOK/MAK per board after KRX. Behavior when there is no opposite liquidity (A12).
7. **Costs.** Personal income tax on sales (0.1% of sale value — confirm the current rate and any 2026 law change). Tax on cash and stock dividends. TCBS commission schedule (zero-commission conditions?), exchange/depository fees (VSDC fees per share/month), and margin interest (for reporting only). Express each as an effective-dated, parameterized formula. (A17)
8. **Corporate-action mechanics.** How the exchange adjusts the reference price on ex-date for cash dividends, stock dividends and rights. When new shares become tradable. (A15)
9. **Special statuses.** Warning/control/restricted/suspended status categories (cảnh báo, kiểm soát, hạn chế giao dịch) and their trading effects, for eligibility filters. (A28)

## Deliverable

`research/findings/R03_findings.md` with machine-ready tables (markdown, and optionally CSV/YAML snippets) for: calendar source, sessions, bands, ticks, lots, settlement timing, fees/taxes, CA adjustment formulas, special statuses. Also include a short list of rules daily OHLCV **cannot** reveal, so the simulator must treat them conservatively.

## Out of scope

Derivatives, covered warrants (except tick tables if shared), bonds, margin simulation details.

## Method and starting sources

hsx.vn and hnx.vn trading regulations, vsd.vn (settlement, fees), SSC (ssc.gov.vn) decisions, the Ministry of Finance circulars on trading and fees, the tax law (current Personal Income Tax law and implementing guidance), broker rule pages (SSI S10–S12, VNDirect S9, the TCBS fee page). Prefer the regulator/exchange over broker summaries. Give the circular/decision number for every rule.

## Known traps

- "T+2.5" is colloquial.
- Rules changed with the KRX go-live. Check that each source is dated after the change.
- Ceiling and floor are rounded to a tick in a specific direction.
- Odd-lot holdings must not be rounded away.
