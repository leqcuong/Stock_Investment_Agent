# R01 — TCBS OpenAPI: Capability, Authentication and Terms

| Field | Value |
| --- | --- |
| Wave / priority | 1 — critical path |
| Owner role | Data engineer |
| Effort budget | ~6 agent-hours |
| Feeds | P1 (adapters), P4 (holdings/sellability), P6 (scheduling) |
| Acceptance checks | A02, A04, A05, A09, A10, A16, A27 |
| Possible gate | **G1** (primary data source) |

## Why this matters

The handoff makes TCBS the broker and the preferred adapter. Whether its OpenAPI can deliver reliable daily history and holdings **without a human entering iOTP every session** decides how the end-of-day pipeline (§15) and scheduler (P6) are designed, and whether a second history source is required.

## Read first

Handoff §2, §4.1–§4.3, §5, §7.2, §12.2, §21 (S1–S5, S13).

## Research questions

1. **Authentication lifecycle.** Exact steps for API key + iOTP → access token. Token lifetime (handoff says ≤ 8 h). Is there a refresh token, long-lived key, or "trusted device" mode? Can an unattended daily job work, and if not, what is the minimum human action per day/week? *Done when:* there is a sequence diagram (in text) and a yes/no/partial verdict on unattended operation, with citations.
2. **Eligibility and terms.** Who can register (any TCBS retail account? any conditions)? Current fees. Rate limits/quotas. Terms on personal automated use, data storage/caching, and redistribution. Is an OTP device or app required?
3. **Market-data endpoints.** Inventory the documented endpoints that are relevant: long-term bars (`/nyx/v2/stock/bars-long-term`), intraday, quotes/snapshot (reference/ceiling/floor, trading status), securities list/universe, indices, corporate actions, financials (if any). For each: parameters, max history depth, pagination, price units (VND vs thousand-VND), adjusted vs raw, volume definition (matched vs including negotiated), timestamp semantics.
4. **Account endpoints (read-only).** Stock assets `/aion/v1/accounts/{accountNo}/se` and any cash/margin/debt endpoints. What does each quantity field mean (total, sellable, T+ pending, blocked, odd-lot)? Can the response support lot-aware sellability (A10), or only aggregates?
5. **Mutation risk.** Which endpoints place/modify orders or transfers? Can API keys be scoped read-only? The design must guarantee no order mutations (§3.3).
6. **Errors and limits.** Documented error codes for expired token, quota, maintenance. Map them to adapter states `AUTH_REQUIRED`, `QUOTA_EXCEEDED`, `PROVIDER_ERROR`.
7. **Ecosystem.** Is there an official SDK (Python?) and what is its license and maintenance status? Note community wrappers and **classify** any that use undocumented public endpoints (e.g., older `apipubaws`-style hosts used by some libraries) as *undocumented — not a dependency*.
8. **Fixture plan.** Which sample responses appear in the docs that could serve as sanitized fixtures before real access exists?

## Options to compare

- A. TCBS OpenAPI for both market history and holdings.
- B. TCBS for holdings and snapshots only; another source (R02) for history and financials.
- C. TCBS unavailable or too manual → CSV import for holdings plus R02 for data.

## Evaluation criteria

Gates: documented and permitted, free for this use, read-only use possible. Then: unattended feasibility, history depth and quality, field semantics clarity, stability/versioning, operational burden for a solo user.

## Out of scope

Calling authenticated endpoints, registering an account, order placement design.

## Method and starting sources

developers.tcbs.com.vn (portal, workflow, auth/token, stock/bars-long-term, stock/asset); TCBS support/FAQ pages about iFlash OpenAPI; TCBS fee schedule; GitHub search for "tcbs openapi". Record the doc version and access date for every page.

## Deliverable

`research/findings/R01_findings.md` (template), including:
- An endpoint capability table that can go straight into `docs/data_capabilities.md` (§4.3).
- An auth-state machine proposal: `OK → EXPIRING → AUTH_REQUIRED`.
- A recommendation among options A/B/C.

## Known traps

- Free registration does not mean free use at any volume.
- A daily-bar timestamp can label the session rather than the time the data became available (§7.2).
- "Sellable" in a broker UI may already net out pending sell orders. Describe what the docs actually say.
