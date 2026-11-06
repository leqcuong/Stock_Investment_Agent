# R03 Findings — Vietnam Market Mechanics, Calendar and Trading Costs

**Researcher:** Codex · **Updated:** 2026-11-06 (Asia/Bangkok) · **Review:** BA, Tech Lead and Product Owner review; source verification updated · **Spec:** [R03](../specs/R03_vn_market_mechanics.md)

**Status: REVIEW CORRECTIONS COMPLETE; FULL RULE CERTIFICATION INCOMPLETE.** Section 3 now compares coherent implementation choices rather than treating reference data, calendar libraries and broker reconciliation as interchangeable. Official VSDC 2026 settlement-calendar notices and amendments, official T+2 guidance, and the complete published TCBS tariff have been read. Exchange-level rounding/status rules, current tax-law text, exact account release timing, and corporate-action formulas remain unverified. Those gaps block claiming the entire R03 specification is complete or exporting every row to production. See the readiness matrix in §5.

**Verified scope:** VSDC equity-settlement holiday exceptions for calendar year 2026 as published by 2026-11-06, with the cross-year examples explicitly listed in §4.10; TCBS's retrieved dated public fee statements; and broker-documented trading-rule candidates. Earlier calendar/rule history and all 2027 dates remain outside verified coverage. Do not extrapolate today's rules across a historical backtest.

## 1. Recommendation (read this first)

- **Recommend:** versioned official-source reference tables plus simple local calendar calculations and broker reconciliation. Separate trading calendars, settlement calendars, legal rules, broker terms and simulator assumptions. Accept only verified rows for their explicit scope and effective interval; preserve broker account state as the live sellability bound.
- **Runner-up:** the same verified tables and broker reconciliation, with a custom `exchange_calendars` or `pandas_market_calendars` adapter when scheduling complexity justifies it. This changes the calculation engine, not the source of authority. Neither inspected snapshot supplies a ready Vietnam calendar.
- **Confidence:** high in the observed library-coverage finding; medium in the proposed design; insufficient evidence to certify current Vietnamese market parameters.
- **Would flip the decision:** a maintained Vietnam calendar with source-linked historical holidays, exceptional closures, session changes, settlement coverage, and regression tests matching official notices.
- **Needs user decision / gate:** no architecture or recurring-cost change is proposed. Previously requested network settings are already published; do not reapply them. Historical expansion depends on the R01/R02 data window, not a watchlist or account credentials.

## 2. Answers to the spec's research questions

Evidence labels: **Observed** means inspected source code or a command result; **Documented (official)** means the exchange/depository/regulator itself publishes the cited statement; it does not imply that every referenced attachment or amendment was read. **Documented (broker)** means an external broker page was retrieved and read; this is primary evidence for that broker’s own terms but secondary evidence for exchange rules. **Documented (handoff only)** means the repository makes the claim but its external source was not independently checked here; **Inferred** means a design recommendation or conditional calculation; **Unknown** means evidence is missing. A handoff claim is not promoted to a verified market rule.

| # | Question | Finding / recommended treatment | Status | Evidence |
| --- | --- | --- | --- | --- |
| Q1 | Calendar | VSDC 2026 settlement closures and amendments verified; six real T+2 examples reconciled. Separate exchange-trading notices and earlier history remain open. | Documented (official) / Unknown | S16–S20; §4.10 |
| Q2 | Sessions | SSI supplies the venue/session matrix in §4.9. HNX after-hours wording conflicts within its page; effective dates and exchange confirmation remain open. | Documented (broker) / Unknown | S8, S12 |
| Q3 | Bands/reference prices | SSI corroborates ordinary ±7%/10%/15%, first-day candidates ±20%/30%/40%, and UPCoM round-lot continuous-match weighted average. Exceptional triggers and rounding need primary evidence. | Documented (broker) / Unknown | S8, S12 |
| Q4 | Ticks/lots | SSI supplies equity tick tiers, 100-share round lots, 1–99-share odd lots and a HOSE 500,000-share maximum. ETF/CW broker candidates added in §4.12; primary instrument rules and historical applicability remain open. | Documented (broker) / Unknown | S8–S9, S12, S23–S24 |
| Q5 | Settlement | VSDC confirms T+2 and DVP, referencing Decision 39/QĐ-HĐTV of 29 April 2025. Exact intraday statutory/account-release deadlines remain open; future rule transition identified. | Documented (official) / Unknown | S21–S22 |
| Q6 | Order types | SSI describes HOSE MP→MTL, MTL/MOK/MAK residual behavior, auction priority, amendment priority and odd-lot LO restriction. | Documented (broker) | S8–S9; see §4.9 |
| Q7 | Costs | Published TCBS total tariff, included collections, cash advance and margin terms retrieved; double-counting risk resolved. Current sale/dividend tax law remains unverified. | Documented (broker) / Unknown | S13–S15, S25; §4.11 |
| Q8 | Corporate actions | Separate entitlement, reference-price adjustment, cash payment, share delivery and tradability. Official formulas, rounding and tax triggers remain open. | Inferred / Unknown | S4, S5–S7, S10 |
| Q9 | Special statuses | SSI describes HOSE restricted-stock 15-minute periodic auctions and final-five-minute amendment restrictions; full legal status taxonomy remains unverified. | Documented (broker) / Unknown | S8–S9 |

## 3. Options compared — corrected decision

**Decision (Inferred):** use official versioned tables for historical market rules, a small local calculation layer, and broker-reported state for live sellability and actual account terms. Calendar libraries are optional calculation helpers. Broker reconciliation cannot replace historical official rules, and an official settlement calendar is not automatically an exchange trading calendar.

| Coherent choice | Free-first gate | What it supplies | Remaining obligation | Decision |
| --- | --- | --- | --- | --- |
| Official tables + simple local calendar arithmetic + broker reconciliation | No mandatory recurring software charge; provider entitlement checked by R01 | Explicit history/provenance, reproducible date arithmetic, live account bounds | Maintain notices/amendments; verify all date coverage and account semantics | Recommended baseline |
| Same tables/reconciliation + custom calendar-library adapter | No mandatory recurring software charge | Library scheduling interfaces for more complex session calculations | Custom VN rules, pinned library version and tests against the same official fixtures | Optional alternative engine, not a different authority |
| Generic weekdays/national holidays as the calendar | No mandatory recurring software charge | Fast synthetic scaffolding | Cannot establish exchange closures, settlement exceptions or special workdays | Synthetic fixtures only |
| Broker state as sole authority for all history | R01 must verify entitlement | Current operational observations | Cannot establish past regulations, holiday amendments or missing historical states | Reject as sole historical source; retain for live reconciliation |

**Team discussion and resolution:** BA requires each acceptance check to distinguish evidence from assumptions. Tech Lead keeps authority, calculation and reconciliation separate so one broker outage does not redefine rules. Product Owner keeps the existing free-first, analysis-only scope and requires visible coverage limits. The resulting pipeline is `retrieve notice → record publication/effective dates → reconcile amendments/conflicts → validate reference rows → calculate dates/costs → reconcile broker state`. No new service, framework adoption, or architecture migration is required by this decision.

**Decision boundary:** adopt a library adapter only if documented scheduling requirements exceed the simple calculation layer and it reproduces the official fixtures. Do not accept a library merely because it supports other exchanges. Any later large framework adoption remains subject to G2 approval.

## 4. Details and evidence

### 4.1 Calendar-library probe

Access date for all observations: **2026-11-05**. Public repositories were cloned to `/tmp/r03-research/`; no application dependencies were installed.

| Library snapshot | Inspection | Result | Limit |
| --- | --- | --- | --- |
| `exchange_calendars` commit `bbda29fed902374bdb75acab008f421fbd567823` | Parsed the default factory/alias dictionaries in `calendar_utils.py`; inspected calendar modules | 72 default factories and 31 aliases; no `XSTC`, `HOSE`, `HNX`, `UPCOM`, `UPCoM`, or `XHNX` entry | Static source inspection, not a runtime import or a claim about every release/fork |
| `pandas_market_calendars` commit `f511a67c0826065a1e880e4e32dd4f86be6840e7`, manifest version `5.6.0` | Inspected `calendar_registry.py`, native calendars, and `calendars/mirror.py`; searched source/docs/tests for Vietnam identifiers | No native Vietnam calendar found; mirror module imports calendars from `exchange_calendars` | Coverage of an installed combination depends on its dependency version and any custom registrations |

**Inferred recommendation:** store each calendar's verified coverage interval explicitly. An unknown future date must not silently become a business day. For each year, obtain both exchange closure notices and the applicable settlement schedule. Treat missing provider bars as missing data until a closure notice establishes otherwise. Do not assume public-sector compensatory workdays imply exchange trading.

### 4.2 Proposed common reference-row contract

All fields and behavior below are **Inferred design proposals**, not requirements extracted from an exchange regulation.

| Field | Meaning / validation |
| --- | --- |
| `rule_id`, `version` | Stable identity plus immutable revision |
| `venue`, `board`, `instrument_type` | Scope; use separate rows where rules differ |
| `investor_scope` | E.g. domestic retail individual; do not generalize institutional exemptions |
| `valid_from`, `valid_to` | Effective interval; define end as exclusive; null end is allowed only for a verified open-ended rule |
| `known_at`, `retrieved_at` | Publication/availability time and research retrieval time; do not substitute one for the other |
| `value` / `formula_id`, `units` | Explicit decimal value or versioned formula; prices in VND/share and quantities in shares |
| `timezone` | `Asia/Ho_Chi_Minh` for Vietnamese session/availability timestamps |
| `conditions`, `exceptions` | First trading day, resumption, corporate action, instrument differences, special notices |
| `source_url`, `document_id`, `article`, `published_on` | Provenance; tariff/notice identifiers are valid where no circular number exists |
| `evidence_status`, `verification_status` | Separate observation/documentation from whether a rule is approved for use |
| `coverage_start`, `coverage_end` | Independently verified historical coverage; not inferred from publication date |
| `supersedes`, `content_hash` | Amendment chain and checksum of archived evidence when accessible |

Proposed export behavior: retain pending rows in the research register; reject them from runnable configurations. Reject overlapping effective rules for the same scope unless precedence is explicit. A null effective date on a pending row means **unknown**, never “all history.”

```yaml
# Proposed schema example; deliberately non-runnable pending verification.
rule_id: VN.HOSE.EQUITY.NORMAL_PRICE_BAND
version: research-2026-11-05
venue: HOSE
instrument_type: equity
investor_scope: domestic_retail_individual
value: null
candidate_from_handoff: 0.07
units: fraction_of_reference_price
valid_from: null
valid_to: null
timezone: Asia/Ho_Chi_Minh
evidence_status: documented_handoff_only
verification_status: pending_primary_source
source_url: null
```

### 4.3 Reference tables to populate after source access

| Table | Required columns beyond common provenance | Effective date / source state |
| --- | --- | --- |
| Trading calendar | Venue, date, open/closed/unknown, session override, closure reason, notice ID | 2026 settlement exceptions verified in §4.10; exchange-trading and earlier notices pending |
| Settlement calendar | Settlement system/asset scope, date, processing status, cutoff exceptions | S16–S20 verified for 2026 equity settlement; preserve scope and amendments |
| Sessions | Session kind, start/end, boundary inclusion, allowed instruments/orders, matching method | Pending post-KRX and applicable earlier exchange regulations |
| Price bands | Ordinary/exceptional band, trigger, reference source, upper/lower rounding algorithms, exceptional fallback | Broker candidates in S8/S12; effective dates unknown |
| Reference prices | Venue, ordinary calculation, component trades, prior-session fallback, CA override | S8/S12 identify eligible UPCoM trades; detailed fallback/rounding pending |
| Ticks/lots | Price-tier bounds/inclusivity, tick, lot, minimum/maximum quantity, odd-lot method/session | Broker equity ticks/lots in §4.9; primary verification pending |
| Settlement timing | Lag, calendar ID, process completion, earliest broker release rule, cash/stock distinction | VSDC T+2 verified; exact intraday deadlines pending |
| Order types | Venue/session, type, matching priority, residual treatment, cancellation/amendment constraints | Pending; do not enable an order merely because its name appears in R03 |
| Fees/taxes | Payer, taxable/fee base, rate, min/max, rounding, collection event, channel/tier, inclusion in commission | TCBS S15 populated in §4.11; current tax law and full history pending |
| Corporate actions | Action type, calculation formula, ex-date, record/payment/credit/trading dates, entitlement rounding | Pending exchange/VSDC/issuer evidence |
| Special statuses | Original status, translated label, legal trading effect, effective interval, instrument notice, local policy | Pending exchange rules and dated security notices |

**Historical pass:** R01/R02 must supply the earliest usable price date and coverage by venue. Build amendment chains back to that date for settlement timing, sessions/order priority, bands/ticks/lots, fees/taxes, and exceptional closures. Record unsupported intervals explicitly. A current page's access date does not establish the effective date of its content. Pre-KRX rules may remain applicable if not amended; a post-KRX publication date alone does not prove accuracy or applicability.

### 4.4 Settlement and cash: model separate states

**Inferred design:** retain trade timestamp, expected settlement date, actual credit/release time where available, broker-reported sellable quantity, unsettled sale proceeds, available cash, advance balance, and advance charges separately. Institutional non-pre-funding provisions must not change retail cash checks without evidence that they apply to the configured investor.

For simulation, calculate settlement using the applicable verified settlement calendar and rule version. For live reconciliation, broker-confirmed sellability bounds quantity. An expected T+2 date does not establish a specific account's release time. Availability of sale proceeds for another purchase, withdrawal, or a paid advance are different capabilities.

### 4.5 Costs: parameterized contract, not verified rates

All formulas below are **Inferred generic accounting templates**. Parameters and applicability must come from the relevant tariff or law. Retrieved TCBS parameter values and inclusion rules are recorded in §4.11; statutory tax parameters remain unresolved.

| Cost | Candidate formula / fields | Required verification |
| --- | --- | --- |
| Broker commission | `tariff(trade_value, side, channel, tier, effective_date)`; percentage/minimum/cap only if specified | TCBS eligibility, promotion dates, excluded channels, billing granularity |
| Sale tax | `taxable_sale_value × applicable_rate`, with legal rounding | Current law, investor category, taxable base; 0.001 is only the handoff candidate |
| Cash-dividend tax | `taxable_cash_distribution × applicable_rate` | Exemptions, withholding agent/date, gross vs net data |
| Stock-dividend tax | Separate event-based liability; formula intentionally unspecified | Basis, trigger, valuation and collection timing; do not copy cash-dividend handling |
| Custody/depository charge | `tariff(quantity_history, billing_period, instrument_type)` | Payer, billable days/quantity, minimum/cap and TCBS pass-through |
| Exchange-related charge | Explicit separate charge only where borne by the investor outside commission | Whether included in broker pricing; avoid charging the same cost twice |
| Cash advance | `advance_tariff(amount, duration, minimum, day_count_basis)` | Optional activation, usable time, actual tariff and collection event |
| Existing margin interest | `interest_tariff(balance_history, rate_schedule, day_count_basis)` | Reporting only; does not authorize new borrowing |
| Slippage | R09 model assumption | Economic execution cost, not a statutory fee |

Do not equate zero commission with zero transaction cost. Do not treat fees charged to a broker or market member as automatic extra retail charges.

### 4.6 Corporate actions and status semantics

**Inferred design:** store announcement, ex-date, record date, cash payment, share credit, and first tradable date separately. Preserve rights, cash, pending shares, and tradable shares as distinct accounting states. Link each event to its source and availability time. Use raw-price units for exchange tick/band checks; document any adjusted-price series and avoid mixing it with explicit dividends in return accounting.

An illustrative economic identity, **not an exchange formula**, is `P_after = (P_before - D + r*K) / (1 + s + r)` for simultaneous cash distribution `D`, free shares `s` per old share, and subscribed new shares `r` per old share at subscription price `K`. It assumes compatible entitlement bases and participation. Sequential actions, alternative rights treatment, taxes, caps, and official rounding can invalidate its direct use. Actual reference-price formulas remain pending; prefer a verified published reference when available and reconcile the calculated value.

Retain Vietnamese labels such as **cảnh báo** (warning), **kiểm soát** (control), **hạn chế giao dịch** (restricted trading), and **đình chỉ giao dịch** (suspension). These translations are research labels, not a verified legal taxonomy. Separate exchange-imposed constraints from the scanner's proposed choice to exclude new entries. Continue reporting existing holdings and unresolved exits even when new entries are disabled.

### 4.7 Worked validation scenarios

The holiday row below uses published VSDC dates; other rows are **synthetic, conditional examples**, not market observations. Arithmetic was checked locally; no application or exchange simulator exists yet.

| Scenario | Synthetic inputs | Expected result / acceptance mapping |
| --- | --- | --- |
| Holiday settlement | Published VSDC example: trade 2026-02-12; settlement closure 16–20 February and weekends | Settlement 2026-02-23, matching S19. Exact account sellable time remains separate. A09 |
| Mixed lots | 200 settled shares, 100 unsettled shares, broker sellable quantity 150 | At most 150 shares can be considered sellable; neither 300 nor automatically 200. A10 |
| Lot constraint | Configured lot 100; unrounded risk cap 99 shares | Zero permitted new round-lot purchase; existing odd lots retained. A18 |
| Fee accounting | Sale 1,000 shares at VND 30,000; assumed sale-tax rate 0.001; commission zero | Conditional tax VND 30,000 and proceeds VND 29,970,000 before other charges. This does not verify the tax rate. A17 |
| Combined action | Assume P=30,000, D=1,000, s=0.1, r=0.2, K=10,000 | Illustrative identity gives about VND 23,846.153846 before official rounding. Must not become an exchange reference without verified rules. A15 |
| Tick boundary | Two synthetic tiers: prices below 10,000 use tick 10; prices at/above 10,000 use tick 50 | Exercise 9,990, 10,000, 10,010, 10,050; algorithm must use verified tier boundaries. These are invented tiers, not a VN schedule. |
| Locked exit | Daily bar at a candidate floor; opposing liquidity and queue unknown | No guaranteed sale. Retain position and pending-exit state; R09 chooses conservative fill convention. A12 |
| Gap outside plan | Planned acceptable entry 29,000–30,000; next open 31,000 | Saved policy skips/reassesses; cannot fill at 30,000 because it was yesterday's desired price. A13 |
| Unsupported restriction | Dated status indicates restrictions; effective sessions cannot be verified | Visible coverage/eligibility limitation, no presumed execution; preserve holdings. A28 |

### 4.8 What daily OHLCV cannot establish

**Inferred from information content:** daily aggregates alone do not identify queue priority, opposing depth at order arrival, the investor's partial fill, intraday stop/target ordering, whether the high/low occurred before settlement release, broker sellability, paid cash-advance eligibility, or actual corporate-action credit dates. A daily price touch is not fill evidence. A close at the floor does not establish that the entire day was untradeable. Missing bars do not distinguish a market holiday, a security suspension, and a provider outage.

R03 owns rule/reference-data verification; only rows meeting their verification criteria are eligible for implementation. R09 owns fill assumptions and sensitivity tests. Do not encode an R09 conservative policy as an exchange rule.

### 4.9 Retrieved market and broker tables — 6 November 2026

All rows in this subsection are **Documented (broker)**. S8/S9/S12 were retrieved on 2026-11-06 without a verified rule-effective date. Their values are research candidates with `verification_status=broker_documented_pending_exchange`; do not use retrieval time as `valid_from`. TCBS rows explicitly distinguish its own dated terms from undated current-page claims. Venue sessions use `Asia/Ho_Chi_Minh`; precise boundary inclusivity remains to be checked.

#### Sessions and permitted orders — ordinary equity round lots

| Venue | Local time | Session | Orders in source | Source / effective-date evidence |
| --- | --- | --- | --- | --- |
| HOSE | 09:00–09:15 | Opening auction | ATO, LO; no amendment/cancellation | S8 §2; effective date unknown |
| HOSE | 09:15–11:30; 13:00–14:30 | Continuous | LO, MTL | S8 §2; effective date unknown |
| HOSE | 14:30–14:45 | Closing auction | ATC, LO; no amendment/cancellation | S8 §2; effective date unknown |
| HNX | 09:00–11:30; 13:00–14:30 | Continuous | LO, MTL, MOK, MAK | S8 §2; effective date unknown |
| HNX | 14:30–14:45 | Closing auction | ATC, LO | S8 §2; effective date unknown |
| HNX | 14:45–14:55; 14:55–15:00 | Source distinguishes periodic then continuous after-hours round-lot matching | Source labels “lệnh giới hạn không có giá” (limit order without a price); exact order semantics unresolved | S8 §2 conflicts with its generic PLO text in §3; block implementation pending exchange rules |
| UPCoM | 09:00–11:30; 13:00–15:00 | Continuous | LO | S12 “Thời gian giao dịch”; effective date unknown |
| All three | 11:30–13:00 | Lunch break | SSI can queue instructions locally; this is not exchange execution | S8 §1–2; SSI-specific queue capability |
| All three | 09:00–11:30; 13:00–15:00 | Negotiated / put-through | Negotiated instructions | S8 §2, S12; effective date unknown |

#### Prices, quantities and exceptional cases

| Rule | HOSE equities | HNX equities | UPCoM equities | Source / unresolved boundary |
| --- | --- | --- | --- | --- |
| Ordinary band | ±7% | ±10% | ±15% | S8 §6, S12; effective dates unknown |
| Ordinary reference | Previous relevant closing price | Previous relevant closing price | Weighted average of **round-lot continuous-matching** trades of previous relevant trading day | S8 §6, S12; no-trade/CA fallback and rounding pending |
| New-listing first-day candidate band | ±20% | ±30% | ±40% | S8 §6; source also describes resumption but inconsistently uses “over 25” vs “25 consecutive” days; exact triggers not verified |
| Matched-trade equity tick | Below VND 10,000: 10; quoted tier VND 10,000–49,950: 50; ≥50,000: 100 | VND 100 | VND 100 | S8 §6, S12; these are equity ticks, not verified ETF/CW schedules |
| Round lot | Multiples of 100 | Multiples of 100 | 100-share lot | S8 §6, S12 |
| Maximum matched round-lot order | 500,000 shares | Not established | Not established | S8 §6; do not generalize HOSE limit |
| Odd lot | 1–99 shares | 1–99 shares | 1–99 shares | S8 §6; S12 |
| Negotiated minimum candidate | 20,000 shares | 5,000 shares | No minimum established here | S8 §6; primary verification pending |
| Negotiated price step | Source states VND 1 | Source states VND 1 | S12 says not prescribed | Source distinctions must be retained; does not change matched-trade tick |

Do not round candidate ceiling/floor values until the exact exchange rounding and exceptional fallback rules are sourced. S8 contains an obvious label conflict: the UPCoM formula using `(100% - 15%)` is labeled “Giá trần” (ceiling), while S12 labels the minus formula “Giá tối thiểu (Giá sàn)” (minimum/floor). Prefer S12's internally consistent wording for the research explanation; do not silently copy S8's label into configuration.

#### Order behavior and restricted securities

| Rule | Retrieved statement | Source / effective-date evidence |
| --- | --- | --- |
| HOSE market order | MP replaced by MTL under KRX | S9 Q2; KRX regime described, exact commencement not independently verified |
| MTL residual | Unfilled balance becomes LO; buy at last matched price + one tick, sell at last matched price − one tick | S9 Q2; S23 supplies broker-described band-boundary cases in §4.12; primary rule pending |
| No opposite limit order | Market-type order rejected/cancelled at entry rather than guaranteeing a fill | S8 §3 for MTL/MOK/MAK |
| MOK / MAK | MOK: whole order cancelled if not fully executable; MAK: cancel unfilled remainder | S8 §3 |
| Auction priority | ATO/ATC do not outrank earlier ceiling-price buys/floor-price sells | S8 §3, S9 Q6: “không được ưu tiên trước” — “not given priority ahead of” |
| Amendments | Change price **or** quantity in one amendment; price change or quantity increase loses time priority; quantity decrease retains it | S9 Q4 |
| Odd-lot auctions | HOSE opening/closing and HNX closing auctions available; **LO only**, not ATO/ATC | S9 Q1/Q3; primary effective date pending |
| HOSE restricted-stock matching | Repeated 15-minute periodic auctions; no amendment/cancellation in each auction's final five minutes | S9 Q7; full status eligibility and session schedule pending |
| Settlement statement | SSI says money/securities settle before 13:00 on T+2 | S8 §6, S12 settlement table; does not establish broker-independent statutory or TCBS availability |

S8's later PLO description says immediate matching when an opposite order exists, while its session table splits HNX after-hours into periodic and continuous periods. This inconsistency requires primary-source resolution. Do not infer a fully specified HNX after-hours matching algorithm from this page.

#### TCBS program statements and eligibility (reconciled with full tariff in §4.11)

| Rule ID | Scope and value/formula | Effective date evidence | Source / status |
| --- | --- | --- | --- |
| `TCBS.COMMISSION.ZERO_FEE` | TCBS commission component 0 VND for covered equities, warrants and listed fund certificates; excludes iWealth Partner-referred clients and clients with other agreements | Page says program from **2023-01-01**, no fixed end. The page does not prove every currently stated exclusion existed unchanged since that date. | S13, issuer of the tariff/program; Documented |
| `TCBS.EXCHANGE_CHARGE` | Separately collected **0.03% × transaction value**; not waived by zero commission | Current page retrieved 2026-11-06; separate charge's historical effective interval not established | S13; Documented; reconciled with the included total trading fee in S15/§4.11 |
| `TCBS.CUSTODY.EQUITY` | **VND 0.3 per share/fund certificate/covered warrant per month** | Dated notice effective **2025-07-31**; no later amendment chain verified | S14; Documented; quantity averaging/proration and full tariff billing terms pending |
| `TCBS.CUSTODY.VAT` | Notice changes the listed service treatment from 10% VAT to **“Không chịu thuế GTGT” (not subject to VAT)** | **2025-07-31** in notice | S14 cites Circular **77/2025/TT-BTC**, issued **2025-07-30**, and Decree **181/2025/NĐ-CP**, dated **2025-07-01**; legal texts not independently retrieved |
| `VN.INDIVIDUAL.SALE_TAX` | Candidate 0.1% × sale value from handoff; **still unverified against current tax law** | Unknown | S4 only; pending S10 |
| `TCBS.ADVANCE`, `TCBS.MARGIN` | Published rates now recorded in §4.11; account-specific terms still required | See S15/S25 | Documented; margin reporting only |

“Not subject to VAT” must not be encoded as a statutory 0% VAT category: preserve the legal category as well as the computed invoice amount. The 2025 notice is primary evidence of TCBS's announced change, not independent verification of the cited laws or proof the tariff is unchanged today.

Conditional A17 example using the newly retrieved exchange-charge rate: on a VND 30,000,000 sale, an eligible zero-commission customer has a VND **9,000** exchange charge. If the separately unverified sale-tax assumption of 0.1% is used in a labeled scenario, tax is VND **30,000**, and proceeds are VND **29,961,000** before any other charges. Both rate provenance and the tax assumption must remain visible. S15 confirms that the published 0.03% total fee for customers without iWealth Partner already includes the collection described in S13; do not add a second exchange charge. The earlier §4.7 example excludes other charges by design and is not a complete TCBS proceeds calculation.

#### Evidence capture

Retrieved HTML and extracted text are in `/tmp/r03-research/` on this instance; they are scratch evidence, not committed source archives. SHA-256 hashes identify the retrieved HTML, not legal authenticity or permanent availability:

| Source | Snapshot | SHA-256 |
| --- | --- | --- |
| S8 | `ssi-rules.html` | `056ddf413863da95495e1642634f71ff0786622e264aa9992d417abc9fc7e70d` |
| S12 | `ssi-upcom.html` | `f7624cbe30e39f31a391d10bbc8c8c4ef6ec49c2c85f38de16b387ff8b1d87a7` |
| S9 | `ssi-krx.html` | `b553576e1e4b47c26990ddc77a74717a026e7c3c1782e46b137adf6f56473f7e` |
| S13 | `tcbs-zero.html` | `997567b43cd50585f182cd27e118b95569bef026815ef5be2c161a5af3ae194c` |
| S14 | `tcbs-vat.html` | `3b6de3ebbb1f055d8e7ea82f37a23ccbb2b4c7f4fe1c21749670420fe296f236` |

### 4.10 Official settlement calendar, amendment chain and transition boundary

**Documented (official), retrieved 2026-11-06.** S16 is the VSDC settlement calendar, not a substitute for separate HOSE/HNX trading notices. The baseline references **4228/TB-VSDC dated 20 November 2025**. S17 amends it for New Year; S18 adds a November holiday. S20 confirms the amendment identifiers **4690/TB-VSDC dated 25 December 2025** and **3043/TB-VSDC dated 21 July 2026**. Keep publication dates as knowledge-time evidence; do not backdate an amendment into decisions before it was announced.

| Rule ID | First closed date | Last closed date (inclusive) | Equity-settlement event | Evidence / knowledge time |
| --- | --- | --- | --- | --- |
| `VSDC.2026.NEW_YEAR` | 2026-01-01 | 2026-01-02 | New Year, including exchanged working day | S16 plus S17 published 2025-12-26; amendment dated 2025-12-25 |
| `VSDC.2026.TET` | 2026-02-16 | 2026-02-20 | Lunar New Year | S16 published 2025-11-21; confirmed S19 published 2026-02-06 |
| `VSDC.2026.HUNG_KINGS` | 2026-04-27 | 2026-04-27 | Compensatory Hung Kings holiday | S16; baseline known 2025-11-21 |
| `VSDC.2026.APRIL_MAY` | 2026-04-30 | 2026-05-01 | Reunification Day / Labour Day | S16; baseline known 2025-11-21 |
| `VSDC.2026.NATIONAL_DAY` | 2026-08-31 | 2026-09-02 | National Day plus exchanged working day | S16; confirmed S20 published 2026-08-06 |
| `VSDC.2026.CULTURE_DAY` | 2026-11-24 | 2026-11-24 | Vietnam Culture Day | S18 published 2026-07-21; cites Resolution 28/2026/QH16 of 2026-04-24, effective 2026-07-01 |

These are **14 weekday closure dates**, in addition to weekends, within the published 2026 equity-settlement schedule as observed on 2026-11-06. Check later exceptional notices before extending an operational calendar. S17/S18/S20 explicitly say makeup Saturdays **2026-01-10** and **2026-08-22** are not equity clearing/settlement sessions. Exceptions for certain debt principal/interest and central-bank transactions do not turn these Saturdays into equity settlement days.

| Trade date | Published T+2 settlement date | Source |
| --- | --- | --- |
| 2025-12-30 | 2026-01-05 | S17, superseding earlier New Year schedule |
| 2025-12-31 | 2026-01-06 | S17 |
| 2026-02-12 | 2026-02-23 | S19 |
| 2026-02-13 | 2026-02-24 | S19 |
| 2026-08-27 | 2026-09-03 | S20 |
| 2026-08-28 | 2026-09-04 | S20 |

**Settlement rule:** S21 states `T+2` for equities, fund certificates and covered warrants and describes delivery versus payment (DVP). It cites **Decision 39/QĐ-HĐTV of 29 April 2025** for detailed clearing/settlement procedures. This establishes the public rule and document identity, not the full attachment's intraday deadlines. SSI's “before 13:00” statement remains a broker statement; do not relabel it as a verified VSDC deadline or TCBS release guarantee.

**Upcoming transition:** S22, published **2 November 2026**, says Circular **145/2026/TT-BTC**, issued **30 September 2026**, takes effect **16 November 2026**. VSDC invites comments by **6 November** on nine draft implementing rulebooks. At this report's as-of date, those drafts are not adopted rule versions. Revalidate the applicable final instruments for runs on/after 16 November; this finding does not assert that T+2 itself changes.

### 4.11 Full TCBS tariff: inclusion rules and cost parameters

**Documented (broker's own terms):** S15 displays 14 October 2026 and says the tariff applies from **1 July 2025**, with row-specific dates and negotiated exceptions. The current page is not proof that its full contents were available unchanged on 1 July 2025. Preserve explicit row dates and retrieve historical versions before backtesting earlier terms.

| Rule ID | Published parameter / formula | Effective-date evidence | Inclusion / limit |
| --- | --- | --- | --- |
| `TCBS.TRADE.NO_IWEALTH` | `trade_value × 0.0003` on all channels for clients without iWealth Partner | S15 general tariff date 2025-07-01 | **Total listed trading fee**; includes the 0.03% exchange collection described by S13. Do not charge it twice. |
| `TCBS.TRADE.IWEALTH` | Agreed rate from **0.03% to 0.3%** of transaction value, except clients under other policies | S15 general tariff date 2025-07-01 | Use actual agreement; do not select the minimum or add another exchange charge without a documented separate charge. |
| `TCBS.CUSTODY.EQUITY` | **VND 0.3/share/month** (also listed fund certificates/CW) | S15; VAT change separately dated in S14 | Includes **VND 0.27/share/month** collected for VSD. Do not add 0.27 again. Quantity averaging/proration still not stated here. |
| `TCBS.CASH_ADVANCE` | `advanced_principal × 0.00042 × chargeable_days` | S15 explicitly says **2023-07-27** | 0.042%/day. Formula is a parameterized interpretation; minimum, partial-day billing and exact eligible-day counting need terms. Optional service, not settled cash. |
| `TCBS.MARGIN.REPORTING` | Annual ordinary-customer rate **from 13.5%**, based on security/rate at disbursement and agreements; `sum(daily_principal × applicable_annual_rate / 365)` | S25 page dated 2026-04-08; rate section effective **2025-02-07** | Reporting template, not a universal rate or authorization for new borrowing. S25 says a year is 365 days. |
| `TCBS.MARGIN.OVERDUE` | Page rate section says 150% of in-term rate; older policy table says 150% capped at 20%/year | S25 mixes a 2025 rate section and 2022 policy section | Resolve current contract/precedence before computing overdue interest; 13.5% × 150% = 20.25% exposes the conflict. |
| `TCBS.NPF.INSTITUTIONAL` | 0.042%/day support for blocking obligation; 15.33%/year settlement support | S15 general tariff date | **Foreign institutional NPF only**. These are not retail margin rates and do not relax retail funding checks. |

S14's non-VAT treatment must remain service-specific; the full tariff also labels some other rows as VAT-exclusive. Never apply one blanket VAT assumption to every fee.

**Checked arithmetic:** for a VND 30,000,000 trade at the no-iWealth tariff, total listed trading fee is **VND 9,000**, not VND 18,000. For 1,000 shares billable for a full month under the published custody rate, charge is **VND 300**, of which **VND 270** is the included VSD collection, not VND 570. A hypothetical VND 10,000,000 advance for two chargeable days is **VND 8,400**, subject to unverified billing conventions. Current transfer/dividend tax-law verification is still separate; the 0.1% sale-tax examples remain labeled assumptions.

### 4.12 Additional broker cross-checks and unresolved conflicts

S23 (TCBS HOSE KRX page, displayed 6 May 2025) and S24 (HNX KRX page, displayed 5 May 2025) corroborate ordinary sessions and stock ticks. They are secondary exchange-rule sources, not independent legal certification.

| Topic | Retrieved evidence | Treatment |
| --- | --- | --- |
| HOSE ETF/CW tick | S23 lists VND 10 across all shown price tiers; matched round lot 100 and maximum 500,000 | Record instrument-specific candidate; do not use equity price tiers for ETFs/CW. Primary effective date pending. |
| HNX ETF tick | S24 lists VND 1; equity matched tick VND 100 | Broker-documented candidate; primary confirmation pending. |
| MTL boundary | S23 says residual buy LO stays at ceiling when last fill is ceiling; residual sell stays at floor when last fill is floor | Resolves missing broker-description edge case; full exchange precedence still pending. |
| Tiny reference-price fallback | S23/S24 describe ±one tick when calculated bounds equal reference; S24 says at reference VND 100 floor remains reference | Candidate exception only; exact general rounding algorithm is still not sourced. |
| HNX after-hours | S24 says 14:45–15:00 PLO, while S8 distinguishes periodic then continuous after-hours matching | Keep conflict open; do not invent an intraday execution engine from inconsistent summaries. |
| Odd-lot auctions | S9 permits specified auctions with LO only; S23's odd-lot paragraph describes only continuous/negotiated windows | Do not silently treat the newer-looking KRX page as internally complete. Primary exchange text needed. |
| UPCoM negotiated tick | S12 says not prescribed; S24's table says VND 100 | Conflicting broker statements; no verified configuration value. |
| Corporate-action pricing | S23/S24 describe adjusting reference for rights/dividends; S26 gives an economic explanation | Insufficient for a verified combined-action formula, rounding or delivery date. Keep §4.6 formula illustrative only. |
| Stock-dividend tax | S27's article exists but its substantive content is an external Canva embed; fetched HTML contains no tax formula | Do not infer tax from the article title or claim the content was read. Current law and collection trigger remain open. |

**Status policy (Inferred, not a legal taxonomy):** keep original warning/control/restricted/suspended/delisted labels and the dated security notice. Warning/control alone does not establish suspension. HOSE PCA is only the broker-documented restricted-stock case in S9/S23. Unknown HNX/UPCoM restrictions block new-entry eligibility with an explicit reason; continue valuing and monitoring existing holdings. A suspension blocks modeled execution until a verified resumption, but does not delete the position. Legal definitions, venue-specific effects and effective dates still need exchange documents.

## 5. Impact on the handoff

| Acceptance check | Evidence now available | Remaining dependency | Readiness |
| --- | --- | --- | --- |
| A09 | Official 2026 VSDC closures/amendments; six sourced settlement-date examples | Separate trading calendar, earlier history, exact release time | Settlement-date reference ready within stated scope; application test not run |
| A10 | VSDC T+2/DVP; lot/broker-bound scenario | Actual TCBS release and reconciliation semantics | Partial |
| A12 | Broker descriptions of order/no-liquidity behavior | Primary matching rules; R09 fill policy | Partial; no guaranteed fill |
| A13 | Broker session/band candidates; conditional gap example | Primary band/rounding rules; saved entry policy | Partial |
| A15 | Event-state design, illustrative arithmetic, broker adjustment descriptions | Official formulas/rounding, issuer delivery/tradability dates and tax triggers | Blocked for verified CA configuration |
| A17 | TCBS published fees, inclusion rules, advance and margin parameters | Current sale/dividend tax law; actual account agreement; unresolved billing conventions | Fee reference improved; complete net-cost verification blocked |
| A18 | Broker lot/tick candidates; round-down arithmetic | Primary venue/instrument limits | Partial |
| A28 | Broker HOSE PCA description; explicit unknown-status policy | Full official status-effect matrix | Partial; unsupported cases visible |

**These are research readiness assessments, not passed application acceptance tests.** The repository has no application/test suite. Document/source checks and conditional arithmetic do not certify live execution, tax compliance or backtest validity.

Proposed changes only; the handoff and R03 spec are unchanged:

1. §5: attach effective dates and source/article IDs to each rule and distinguish legal, exchange, broker, and model layers.
2. §7: retain both effective time and knowledge time for rules and notices; preserve historical versions.
3. §9.5: restrict backtest claims to verified rule/calendar coverage; state unsupported historical intervals.
4. §11: distinguish investor-paid fees from charges already included in commission.
5. §21: preserve older sources that remain legally effective; trace amendments rather than filtering only by post-KRX publication date.

Input for R01/R02: earliest history date, historical status/CA fields, provider price units and reference-price availability. Input for R09/R10: pending rule register, settlement/cost contracts, conditional examples. Proposed ADR: **versioned local market-reference tables with explicit verification and coverage boundaries**.

## 6. Risks and traps found

- A library's international exchange coverage does not establish Vietnam coverage.
- Broker sources now corroborate several handoff claims, but current legal applicability and complete historical coverage are still unverified.
- A 2026 access date cannot make a historical rule applicable to all 2026 sessions.
- “Machine-ready” syntax does not make unknown parameters safe to execute.
- Generic national holidays, present-day broker state, and adjusted prices each answer different questions from historical trading/settlement rules.
- Exact taxes, rounding, first-day/resumption bands, and institutional exemptions must not be reconstructed from memory.

## 7. Open questions and continuation

### Source access and publication state — final review on 6 November 2026

The prior domain additions are published and enforced. VSDC and TCBS full tariff are now accessible and read; no previous configuration changes need reapplying. This review changes no environment settings and publishes nothing.

| Source | Observed outcome | Remaining limit |
| --- | --- | --- |
| VSDC | Official calendar, amendments, settlement overview and forthcoming-rule notice retrieved | Detailed legal-search POST returned HTTP 400 with an empty body; full Decision 39 attachment/intraday deadline not retrieved |
| TCBS | Detailed tariff and margin policy retrieved | Contract-specific eligibility/proration; stock-dividend article embeds Canva content not retrieved |
| Government search | Public search endpoint reachable, returns JSON `error: Unable to connect to the remote server`, `data: null` | A backend failure, not evidence of zero matching laws |
| HNX | Root and public vi-vn routes returned HTTP 503 | Primary exchange regulations unavailable through tested routes |
| HOSE | Public HTML/JavaScript reachable; official app uses `api.hsx.vn` and `staticfile.hsx.vn` | These additional hosts are outside the current allowlist; exchange regulation text not retrieved. No undocumented endpoint is proposed as an application dependency. |
| VBPL | Public search request returned HTTP 403 | Legal texts not verified from that route |

### Remaining evidence required before the whole R03 can be declared complete

1. Retrieve authoritative HOSE/HNX/UPCoM regulations with effective dates/article IDs for price rounding, exceptional bands, instrument/order limits, after-hours and odd-lot conflicts, and status effects.
2. Retrieve current individual securities-sale and cash/stock-dividend tax legislation, amendments and collection-trigger rules. Existing 0.1% examples remain assumptions until this is done.
3. Read the full applicable VSDC procedure and public TCBS release terms for intraday sellability/cash deadlines. Recheck adopted instruments for the 16 November transition; do not promote drafts.
4. Verify official CA formulas/rounding and issuer-specific credit/trading schedules. The illustrative economic identity is not a substitute.
5. Retrieve independent exchange-trading calendars and earlier settlement/rule amendments once R01/R02 fix the history window. Do not claim historical completeness from a 2026 calendar.

**No credentials are needed to research these public rules.** Account-specific fee eligibility, actual holdings and broker release observations are later integration inputs. The exact current public-source failures above remain external limitations; changing a status label to COMPLETE would not resolve them.

## 8. Sources

S1–S4 were inspected on **2026-11-05**. External pages were retrieved or retried on **2026-11-06**; dates use the client Asia/Bangkok context. Pending URLs identify retrieval targets, not documents read or proof of a rule.

| ID | Title / URL | Type | Version / access result |
| --- | --- | --- | --- |
| S1 | [exchange_calendars default registry](https://github.com/gerrymanoim/exchange_calendars/blob/bbda29fed902374bdb75acab008f421fbd567823/exchange_calendars/calendar_utils.py) | Primary library source | Commit `bbda29f…`; inspected locally, static AST probe |
| S2 | [pandas_market_calendars registry](https://github.com/rsheftel/pandas_market_calendars/blob/f511a67c0826065a1e880e4e32dd4f86be6840e7/pandas_market_calendars/calendar_registry.py) | Primary library source | Commit `f511a67…`; inspected; manifest reports 5.6.0 |
| S3 | [pandas_market_calendars mirrored calendars](https://github.com/rsheftel/pandas_market_calendars/blob/f511a67c0826065a1e880e4e32dd4f86be6840e7/pandas_market_calendars/calendars/mirror.py) | Primary library source | Same commit; inspected |
| S4 | [Project handoff](../../requirement/AI_Stock_Scanner_Agent_Handoff.md) | Internal specification, not primary legal evidence | Version 1.0, 2026-11-05; inspected at project commit `41b109b8100dfaf781d718d656dde7583bb8d641` |
| S5 | [HOSE](https://www.hsx.vn/) | Official exchange discovery target | 2026-11-06: HTTP 200 application shell; document/decision IDs pending |
| S6 | [HNX](https://hnx.vn/) | Official exchange discovery target | 2026-11-06: HTTP 503; rule and notice IDs pending |
| S7 | [VSDC](https://vsd.vn/) | Official settlement/depository discovery target | 2026-11-06: redirect followed; official evidence retrieved as S16–S22 |
| S8 | [SSI equity trading rules](https://www.ssi.com.vn/khach-hang-ca-nhan/quy-dinh-giao-dich/quy-dinh-giao-dich-co-phieu) | Broker summary of exchange rules | Retrieved/read 2026-11-06; no verified publication/effective date |
| S9 | [SSI KRX FAQ](https://www.ssi.com.vn/khach-hang-ca-nhan/krx-thi-truong-co-so-faq) | Broker summary of KRX changes | Retrieved/read 2026-11-06; no verified commencement date |
| S10 | [Government legal documents](https://vanban.chinhphu.vn/), [legal database](https://vbpl.vn/), [Ministry of Finance](https://mof.gov.vn/) | Official legal discovery targets | Government search backend error despite HTTP access; VBPL 403; current legal texts pending |
| S11 | [TCBS](https://www.tcbs.com.vn/) | Broker's own tariff discovery target | Main site retrieved; program/notice S13/S14 and full tariff S15 read |
| S12 | [SSI UPCoM rules](https://www.ssi.com.vn/khach-hang-ca-nhan/quy-dinh-giao-dich-tai-upcom) | Broker summary of exchange rules | Retrieved/read 2026-11-06; effective date unknown |
| S13 | [TCBS Zero Fee program](https://www.tcbs.com.vn/ca-nhan/zero-fee-mien-phi-giao-dich/) | Primary broker program statement | Retrieved/read 2026-11-06; states program starts 2023-01-01; amendment history unavailable |
| S14 | [TCBS VAT and fee notice effective 31 July 2025](https://www.tcbs.com.vn/tin-tuc/thong-bao-tu-tcbs/thong-bao-cap-nhat-thue-gtgt-bieu-phi-mot-so-dich-vu-chung-khoan-tu-ngay-31-07-2025/) | Primary broker notice | Published 2025-07-31; retrieved/read 2026-11-06 |
| S15 | [TCBS detailed securities tariff](https://help.tcbs.com.vn/bieu-phi-dich-vu-chung-khoan/) | Official broker tariff linked by S13 | Retrieved/read 2026-11-06; page displays 2026-10-14; states tariff from 2025-07-01 with row-specific exceptions |
| S16 | [VSDC settlement calendar 2026](https://vsdc.vn/lich-giao-dich?tab=LICH_NGHI_GIAODICH&date=06/11/2026) | Official depository calendar | Published 2025-11-21; baseline 4228/TB-VSDC; read 2026-11-06 |
| S17 | [VSDC New Year amendment](https://vsdc.vn/vi/ad/190545) | Official notice | Published 2025-12-26; amendment 4690/TB-VSDC dated 2025-12-25 identified by S18/S20; read 2026-11-06 |
| S18 | [VSDC July calendar amendment](https://vsdc.vn/vi/ad/198399) | Official notice | Published 2026-07-21; 3043/TB-VSDC identified by S20; read 2026-11-06 |
| S19 | [VSDC Lunar New Year settlement](https://vsdc.vn/vi/ad/191685) | Official notice | Published 2026-02-06; explicit T+2 examples; read 2026-11-06 |
| S20 | [VSDC National Day settlement](https://vsdc.vn/vi/ad/198931) | Official notice | Published 2026-08-06; amendment references and T+2 examples; read 2026-11-06 |
| S21 | [VSDC clearing and settlement](https://vsdc.vn/sd/XAz40d2Q-9j569TvBgLQaQ) | Official service description | T+2/DVP; cites Decision 39/QĐ-HĐTV dated 2025-04-29; read 2026-11-06; attachment not read |
| S22 | [VSDC consultation on implementing rules](https://vsdc.vn/vi/ad/202086) | Official consultation notice, not adopted rulebook | Published 2026-11-02; states Circular 145/2026/TT-BTC effective 2026-11-16; read 2026-11-06 |
| S23 | [TCBS HOSE KRX rules](https://help.tcbs.com.vn/quy-dinh-giao-dich-tai-hsx-krx/) | Broker rule summary | Displays 2025-05-06; retrieved/read 2026-11-06; effective rule date not established |
| S24 | [TCBS HNX KRX rules](https://help.tcbs.com.vn/quy-dinh-giao-dich-chung-khoan-tai-hnx-krx/) | Broker rule summary | Displays 2025-05-05; retrieved/read 2026-11-06; effective rule date not established |
| S25 | [TCBS margin policy](https://help.tcbs.com.vn/chinh-sach-margin/) | Primary broker policy | Displays 2026-04-08; rate section effective 2025-02-07; older policy section dated 2022-11-07; read 2026-11-06 |
| S26 | [TCBS ex-rights price explanation](https://help.tcbs.com.vn/ufaq/tai-sao-thi-gia-lai-dieu-chinh-giam-tai-ngay-giao-dich-khong-huong-quyen/) | Broker explanation | Read 2026-11-06; no verified effective date or exact formula |
| S27 | [TCBS stock-dividend tax article](https://help.tcbs.com.vn/thue-co-tuc/) | Broker article containing an external embed | Displays 2025-11-24; HTML read 2026-11-06, substantive Canva content not retrieved |

**Recommendation remains:** official versioned tables, simple calculation and broker reconciliation form the baseline. A custom library adapter is an optional engine over the same verified data. Section 3 and the identified report defects have been corrected; unresolved primary-rule evidence keeps full R03 certification open. No application acceptance check is claimed as passed.
