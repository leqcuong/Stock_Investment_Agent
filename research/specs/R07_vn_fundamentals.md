# R07 — Vietnamese Financial Statements, Banks and Publication Lags

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | Quant engineer with accounting knowledge |
| Effort budget | ~6 agent-hours |
| Feeds | P2 (financial summaries), P3 (whether financial features can enter training) |
| Acceptance checks | A06, A07, A26 |

## Why this matters

Financial analysis is in Phase 1 scope, but historical ML financial features are **conditional** on knowing when each figure became public (§8.2). Vietnamese statements follow VAS, which has its own structure (and IFRS adoption is in transition). Banks need different metrics. This track defines what can be shown honestly and how availability dates are assigned.

## Read first

Handoff §7.1 (Financial observation), §7.2, §8.2, §9.4, §14 (A06, A07).

Also read `research/notes/Graham_Intelligent_Investor_fit.md`: a reference screening catalog (Graham, *The Intelligent Investor*, Ch. 14–15) with an initial data-availability table. It is a US 1970s reference for formulas, not Vietnam-calibrated thresholds, and its availability column is untested. Probe `Fundamental.equity.*` on sample tickers, including whether `filing` carries publication dates, and settle each row.

## Research questions

1. **Disclosure deadlines.** The regulation in force (historically Circular 96/2020/TT-BTC; check for replacements or amendments up to 2026). Deadlines for quarterly, semi-annual (reviewed) and annual (audited) reports, and extension conditions. Are these deadlines a safe **conservative availability proxy** when the actual publication date is unknown? Quantify how often companies file late, if any data exists.
2. **Statement structure (VAS).** Standard templates (B01/B02/B03 for corporates; separate templates for banks, securities firms and insurers). Consolidated vs parent-only. Cumulative (YTD) vs standalone quarterly cash flows. The IFRS transition status and its impact on comparability.
3. **Metric catalog.** For non-financial companies: revenue and profit growth, margins, ROE/ROA, operating cash flow vs profit, leverage, and valuation (P/E, P/B, EV/EBITDA). For each, give: required line items, the formula, and invalid cases (negative base, non-comparable period). Return "N/A" with a reason code instead of a number in those cases.
4. **Banks and securities firms.** Which metrics (NIM, NPL ratio, CAR, LDR, CASA, credit cost) are computable from **public statements** vs requiring notes or other disclosures? Recommend a bank-specific summary that never invents NPL/NIM/CAR (§8.2).
5. **Restatements.** How often do VN companies restate (e.g., audited vs self-prepared annual differences)? How should revisions be stored and labelled?
6. **Sector-aware scoring.** Is any simple, published, sector-relative quality/value scoring appropriate for a *display summary*, or should Phase 1 show raw metrics only? Evidence of fundamental factors (value, quality, profitability) in the Vietnamese cross-section.
7. **Source fit.** Cross-check with R02: which sources supply line items and dates for which statement types?

## Deliverable

`research/findings/R07_findings.md` with: a disclosure-deadline table (with legal citations), a metric catalog (formula, inputs, validity rules, reason codes), a bank/securities-firm metric table (computable / not computable), an availability-date policy for training, and a short evidence review of fundamental factors in VN.

## Out of scope

Building a full valuation model (DCF), analyst forecasts, and paid fundamental datasets (note them as `PAID/OPTIONAL` only).

## Known traps

- The quarter-end date is not the publication date.
- Q4 standalone ≠ annual minus Q1–Q3 when the audit adjusts figures.
- Parent-only vs consolidated reports mixed in one series.
- Growth rates computed from a negative base.
