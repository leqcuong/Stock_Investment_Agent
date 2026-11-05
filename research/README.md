# AI_Stock_Scanner — Research Phase (Literature Review)

**Source requirement:** [../requirement/AI_Stock_Scanner_Agent_Handoff.md](../requirement/AI_Stock_Scanner_Agent_Handoff.md) (v1.0, 5 Nov 2026) — referred to below as *the handoff*; `§n` = handoff section n.
**Purpose:** Before any P0–P6 code is written, research agents find the best-supported way to meet each part of the handoff, using primary documentation, academic/practitioner literature, and existing open-source work.
**Status:** Specs ready. No findings yet.

## 1. Where this fits in the delivery pipeline

```text
Handoff (requirement/)  ──►  RESEARCH (this folder)  ──►  ADRs / spec updates  ──►  P0 … P6 build (§13)
                              R01–R11 findings            Tech Lead synthesis        coding agents
```

The handoff goes straight from specification to build. This phase is inserted because several handoff decisions depend on facts nobody has checked yet: whether TCBS access can run unattended, how deep the free history is, whether point-in-time financials exist, and whether to build or adopt a framework. Building P1–P4 before those facts are known risks rework.

## 2. Research tracks

| ID | Track | Wave | Feeds | Unblocks decision |
| --- | --- | --- | --- | --- |
| [R01](specs/R01_tcbs_openapi.md) | TCBS OpenAPI capability, auth and terms | 1 | P1, P4, P6 | Can TCBS be the primary price/holdings source, and can it run unattended? |
| [R02](specs/R02_free_data_sources.md) | Free complementary data sources (Vnstock and others) | 1 | P1, P2, P3 | Which source provides history, universe, financials and corporate actions? |
| [R03](specs/R03_vn_market_mechanics.md) | Vietnam market mechanics, calendar, costs reference data | 1 | P1, P4 | Exact rules/tables the calendar, simulator and sizing must encode |
| [R04](specs/R04_build_vs_adopt.md) | Build vs adopt: quant frameworks and prior art | 1 | P0, P3, P4 | Custom code vs Qlib/vectorbt/etc.; what to reuse |
| [R05](specs/R05_local_stack_storage.md) | Local stack: point-in-time storage, UI, scheduler, config/secrets | 2 | P0, P1, P5, P6 | Concrete libraries and schema pattern for §6–§7 |
| [R06](specs/R06_technical_market_context.md) | Technical features, baseline rule, market/sector context — VN evidence | 2 | P2, P3 | Feature set v1 and the frozen research baseline |
| [R07](specs/R07_vn_fundamentals.md) | Vietnamese financial statements, banks, publication lags | 2 | P2, P3 | Which financial metrics are shown/trained and how availability dates are set |
| [R08](specs/R08_ml_methodology.md) | ML methodology: labels, purged CV, ranking metrics, overfitting controls | 2 | P3 | Label spec v1, split design, metrics and promotion rubric |
| [R09](specs/R09_execution_simulation.md) | Execution simulation and backtest realism on daily bars | 2 | P3, P4 | Fill conventions, limit-lock and T+2 handling in the simulator |
| [R10](specs/R10_risk_sizing_accounting.md) | Risk sizing, portfolio constraints, performance accounting | 2 | P4, P5 | Sizing/stress formulas and cash-flow-adjusted drawdown method |
| [R11](specs/R11_alerts_scheduling.md) | Alert reliability, free notification channels, local scheduling | 2 | P5, P6 | Event/outbox design, channel options to offer the user, missed-run handling |

**Coverage:** every acceptance check A01–A28 (§14) is owned by at least one track, except **A19** (an unowned favorite weakens → warning, not a sell quantity). A19 is pure product logic already fully specified in §3.1/§10.1, so it needs no research.

**Wave 1** tracks are on the critical path; start them first and in parallel. **Wave 2** tracks can also start immediately. They mostly depend on documentation and literature, but should re-check their conclusions once R01/R02/R04 findings land.

## 3. Rules for every research agent

1. **Read first:** the handoff sections listed in your spec, plus this README. Do not re-litigate confirmed decisions in handoff §2 (TCBS broker, free-first, ML direction, analysis-only Phase 1).
2. **Output:** one file `research/findings/<ID>_findings.md` using [_TEMPLATE_findings.md](_TEMPLATE_findings.md). Do not edit other tracks' files or the handoff.
3. **No application code.** Small throwaway probes (e.g., inspecting a public library's API) are allowed in a scratch location; do not commit them to `src/`.
4. **Source hierarchy:** official/primary docs (exchange, regulator, broker, library maintainers) > peer-reviewed papers > reputable practitioner sources > blogs/forums. Vietnamese-language sources are expected and welcome; quote the original term and translate it.
5. **Date and version every claim** (access date, doc/library version). Mark each claim **Documented** (a source says so), **Observed** (you saw it in a public, permitted response or code), or **Inferred**.
6. **Never:** request or store credentials, iOTP or account numbers; call authenticated endpoints; recommend undocumented/scraped endpoints as a dependency (you may *report* that they exist and their risk); present a backtest number from a paper as evidence for this project.
7. **Free-first gate:** any option that needs paid data, a paid LLM, a GPU, or hosting must be marked `PAID/OPTIONAL` and cannot be the primary recommendation.
8. **Recommend, don't survey.** Each finding ends with one recommendation, its runner-up, and what evidence would flip the choice.
9. **Map to the handoff:** list affected acceptance checks (§14 A01–A28) and any handoff text you propose to change (as a proposal, not an edit).
10. **Time-box:** follow the effort budget in your spec. If a question cannot be answered from public sources, record it under *Open questions → needs user/credentials* and move on.

## 4. After the findings: synthesis and decision gates

1. **Tech Lead synthesis:** read all findings and write `docs/adr/ADR-00x-*.md` (one per decision), plus a consolidated list of proposed handoff changes.
2. **BA check:** every acceptance check A01–A28 is still covered, and every open decision in §16 still has a safe default.
3. **PO review with the user.** These need explicit user approval before build:
   - **G1 — Data source:** if R01 shows TCBS cannot run unattended, or lacks usable history, choose the primary history source.
   - **G2 — Architecture:** if R04 recommends adopting a framework (e.g., Qlib) as the core rather than a library, that is a large architecture change and needs user sign-off.
   - **G3 — Any recurring cost:** any option that breaks the VND 0 recurring target.
4. Then P0 starts using the kickoff prompt in handoff §17, plus the approved ADRs.

## 5. Team discussion (BA · Tech Lead · Product Owner)

- **Tech Lead:** Data access is the critical path. If TCBS needs an iOTP every 8 hours, the "unattended end-of-day scan" in §15 does not work as written, and P1, P5 and P6 all change. R01 and R02 go first, and their capability tables must be concrete enough to fill `docs/data_capabilities.md` (§4.3) directly.
- **Product Owner:** R04 has the largest effect on schedule. A mature framework could replace weeks of P3/P4 work, but it might fight the Vietnam-specific rules (T+2, ±7/10/15% bands, lot-aware settlement). I want a reasoned recommendation backed by a small fit test, not a feature list. Adopting a framework as the core goes to the user (gate G2).
- **BA:** Each finding has to trace back to acceptance checks and §16 open decisions. Otherwise research turns into reading for its own sake. R07 and R08 matter most for honesty: if point-in-time financials or survivorship-free history can't be recovered, the model card's claims shrink, and the user should hear that early.
- **Agreed:** wave 1 = R01–R04 in parallel. Wave 2 runs alongside but re-checks against wave-1 findings. Nothing is coded until synthesis is done and gates G1–G3 are cleared.

## 6. Status

| ID | Assigned to | Status | Findings |
| --- | --- | --- | --- |
| R01–R11 | — | Not started | — |
