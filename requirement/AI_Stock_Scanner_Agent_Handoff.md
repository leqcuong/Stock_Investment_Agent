# AI_Stock_Scanner — Product Decisions and Agent Implementation Handoff

**Version:** 1.0  
**Prepared:** 5 November 2026 (Asia/Bangkok)  
**Purpose:** Consolidate the discussion, preserve the user's decisions, and give coding agents a concrete starting specification.  
**Status:** Planning and implementation handoff. No application, trained model, broker connection, or alert service has been implemented or validated by this document.

## 1. Read this first

Build a **free-first, ML-assisted Vietnamese stock scanner** for a solo retail trader using **TCBS**. It must automatically analyze financial information, technical conditions, and market context to:

1. Evaluate the user's favorite stocks and identify conditional entry and exit-review setups.
2. Monitor actual holdings separately from favorites.
3. Scan the wider Vietnamese market for potential opportunities.
4. Produce understandable alerts and retain signals for later evaluation.

The user has chosen the ML scanner direction. The earlier panel preferred starting with a risk co-pilot, but that recommendation does **not** replace the user's choice. Keep risk, settlement, and data-quality checks inside the scanner.

**Do not wait for a watchlist to start implementation.** Build an empty-state workflow, clearly labeled synthetic fixtures, and import/configuration support. Do not invent the user's stocks, holdings, account size, or margin exposure.

This is a consolidated specification rather than a verbatim conversation transcript. Sections 2–17 describe the proposed build; sections 18–20 preserve the panel's diagnosis, debate, alternatives, and illustrative calculations. Proposed settings are research hypotheses, not proven trading edges or personalized investment allocations.

**Quick navigation:** [Decisions](#2-confirmed-decisions-and-pending-inputs) · [Data/TCBS](#4-data-strategy-including-the-tcbs-decision) · [ML contract](#9-ml-training-and-evaluation-contract) · [Agent work packages](#13-agent-work-packages-and-dependency-order) · [Acceptance checks](#14-acceptance-checks-and-failure-scenarios) · [Kickoff prompt](#17-copyable-kickoff-prompt-for-coding-agents) · [Panel debate](#19-earlier-panel-independent-assessments-and-cross-examination)

## 2. Confirmed decisions and pending inputs

| Item | Status | Instruction for agents |
| --- | --- | --- |
| Project name | Confirmed | `AI_Stock_Scanner` |
| Market | Confirmed | Vietnamese equities: HOSE, HNX, UPCoM |
| Core product | Confirmed | ML-assisted analysis, watchlist alerts, and market discovery |
| Analysis requested | Confirmed | Financial/fundamental analysis, technical analysis, and supporting market context |
| Broker | **Confirmed: TCBS** | Prioritize supported TCBS integration; do not require another broker account |
| Budget | **Free preferred** | Target VND 0 recurring software/data charges on existing hardware; no mandatory paid data, LLM, GPU, or hosting |
| Favorite tickers | **Later** | Leave empty and editable; this is not a development blocker |
| Current holdings | Pending | Keep separate from favorites; support manual input and import |
| Holding period | Pending | Proposed research default: 5–20 sessions, with a 10-session model horizon |
| Analysis frequency | Proposed | End-of-day first, after required inputs are complete |
| Alert destination | Pending | In-app inbox and local digest initially; external channel disabled until configured |
| Account equity/cash | Pending | Do not issue personalized quantities until supplied and reconciled |
| Margin use | Pending | Do not assume no existing debt; proposed strategy uses no new borrowing |
| Operating system and machine availability | Pending | Keep local setup portable; scheduling requires an awake machine |
| TCBS API credentials/eligibility | Pending | Build adapters and fixtures now; validate real access later |
| Vnstock Community credentials | Pending | Optional complementary data access; verify current entitlements |
| Automatic trading | Outside Phase 1 | Analysis and alerts only; execution remains manual |

No answer has been supplied for alert channel or holding period. Telegram was an example in the discussion, not a user selection.

## 3. Product outcomes and scope

### 3.1 Four workflows

| Workflow | Required behavior | Output |
| --- | --- | --- |
| Analyze favorites | Analyze every configured stock, including weak or incomplete setups | Entry setup, wait, weakening setup, or insufficient data |
| Monitor holdings | Use actual lots, acquisition dates, quantity, sellable shares, and saved plan | Exit-review, profit-taking review, invalidation, and settlement information |
| Discover opportunities | Enumerate the market, check eligibility, rank the successfully covered universe | A short candidate list with reasons and risks; zero candidates is valid |
| Track outcomes | Save decisions before outcomes become known | Net results, drawdown, failed exits, false signals, missed opportunities, and operational quality |

Favorites are not evidence of ownership. An unowned stock can receive a weakening/setup-invalidated message, but not an instruction to sell a fictional holding.

### 3.2 Phase 1 includes

- A local dashboard and a reusable command-line analysis pipeline.
- Market data ingestion with persistent caching, incremental updates, and clear coverage reporting.
- Watchlist management and optional holdings/transaction imports.
- Technical analysis and available financial summaries.
- A transparent baseline plus an actual trained ML model and chronological evaluation.
- Conditional entry/exit plans, risk checks, alert deduplication, and a signal journal.
- A paper-operation mode before any claim that model alerts are suitable for trading decisions.

### 3.3 Phase 1 excludes

- Broker order placement, order modification/cancellation, transfers, or account mutations.
- Deep learning, reinforcement learning, high-frequency trading, derivatives, and short selling.
- Guaranteed returns, guaranteed stop execution, or unvalidated probability-of-profit labels.
- Paid-only data as a required dependency, paid LLM calls, or a GPU requirement.
- Social-room scraping, trading from Zalo/Telegram hype, and opaque “smart money” scores.
- Multiple broker integrations, a public SaaS product, and a complex distributed deployment.
- A comprehensive broker margin simulator or dozens of untested indicators.

## 4. Data strategy, including the TCBS decision

### 4.1 Current source findings

The following provider and market-rule references were checked on 5 November 2026. Documentation establishes advertised capabilities, not successful access to this user's account. Check terms, permissions, schemas, and actual responses during integration.

**TCBS has an official OpenAPI.** Its developer portal documents market data and portfolio access across HOSE, HNX, and UPCoM. The workflow page advertises free iFlash OpenAPI registration. Authentication uses an API key plus iOTP, and access tokens last at most eight hours. Free registration is not a promise that all data usage, execution, or future service charges are zero. [S1–S3]

The official long-term OHLCV endpoint is documented as `GET /nyx/v2/stock/bars-long-term`, with daily/weekly/monthly bars. The stock-assets endpoint is `GET /aion/v1/accounts/{accountNo}/se`. These are implementation starting points; validate history depth, price adjustments, pagination, data units, and holdings-field semantics before relying on them. [S4–S5]

**Design implication:** prioritize an official TCBS adapter for broker-related data and evaluate it for price history. Token renewal can interrupt unattended jobs. Provide an explicit `AUTH_REQUIRED` state, retain timestamped cached data, and support CSV-based account input. Do not claim fully unattended TCBS access until its documented authentication flow has been demonstrated.

**Vnstock Community** is a possible complementary source. Current documentation describes a free personal/research key, roughly eight years of daily history, eight recent financial reporting periods, summarized statement fields, account-dependent quotas, and one-device restrictions. Quarterly requests mean eight quarters, not eight years. Do not assume the Guest tier is adequate for recurring operation. [S6]

Vnstock currently places foreign/proprietary-flow functions outside its Community market-data feature set. Its financial documentation distinguishes basic statements from restricted ratio/detail functions. Compute ratios only when the available fields support them; otherwise show unavailable. [S7–S8]

The earlier discussion also considered SSI FastConnect and DNSE. They remain alternatives if the user later requests a broker/source change; they are not prerequisites for a TCBS-based build. FiinPro/Vietstock subscriptions are optional future purchases.

### 4.2 Source routing

| Data | Preferred evaluation path | Required fallback/limitation |
| --- | --- | --- |
| Current prices, reference/ceiling/floor, trading status | Official TCBS market-data endpoints | Timestamped cache; unknown fields prevent checks that need them |
| Historical OHLCV and indices | Evaluate TCBS daily history; use permitted Vnstock data if needed | Document actual coverage, adjustments, gaps, and source identity |
| Listed securities and classifications | Supported provider reference data | A versioned, dated manual universe import for development |
| Current financial statements | Permitted Vnstock statements, official company disclosures, or another documented supported source | Partial summaries; no invented ratios or publication dates |
| Holdings, sellable shares, cash, debt | TCBS read operations where documented and available | Manual/CSV import with reconciliation and timestamps |
| Fees and account terms | User's current TCBS fee/account information | Explicit research assumptions only; account sizing remains unavailable if critical inputs are missing |
| Calendar and corporate actions | Exchange/depository/company notices or documented provider data | Versioned curated inputs; flag incomplete coverage |
| Foreign/proprietary flows | Optional supported, entitled feed | Excluded from required features when absent; missing is not zero |

The broker and the market-history source need not be identical. Keep providers behind adapters so one unavailable service does not force a rewrite. Never silently join incompatible price conventions or substitute an old cached snapshot as today's observation.

### 4.3 Initial capability report

Before committing the model to a provider, write `docs/data_capabilities.md` recording:

- Provider/version, terms or entitlement notes, authentication, quota behavior, and observed schema.
- Coverage by exchange and instrument, earliest usable date, and supported intervals.
- Price/volume/currency units; adjustment and corporate-action treatment.
- Whether turnover represents matched trades, negotiated trades, or both.
- Whether publication dates and historical statement versions are available.
- Whether historical universe membership, suspended/delisted stocks, and exchange transfers are recoverable.
- Supported account fields and the meaning of broker sellable quantity.
- A small set of sanitized response fixtures and checks against known values.

If an essential capability cannot be established, document the limitation and use the fixture/import route. Do not scrape undocumented TCBS/VNDirect endpoints because an old example happens to work.

## 5. Vietnam-specific mechanics and execution constraints

| Mechanic | Rule context | Implementation requirement |
| --- | --- | --- |
| Settlement | Formal settlement is T+2; normal purchased-share availability is the afternoon of the second business day. “T+2.5” is colloquial shorthand. [S9] | Track purchase lots and an exchange calendar; broker-confirmed sellability governs live quantities |
| Ordinary daily bands | HOSE ±7%, HNX ±10%, UPCoM ±15%; exceptional sessions can differ. [S10] | Prefer supplied daily reference/ceiling/floor values, with dated rules and correct tick rounding |
| UPCoM reference | Uses the relevant previous session's weighted-average matched price. [S11] | Do not simulate its reference price as a universal previous close |
| KRX order behavior | HOSE uses MTL; ATO/ATC do not automatically precede earlier ceiling-buy/floor-sell LO orders. [S10, S12] | Treat sessions and order types explicitly in later execution modeling |
| Missing opposing liquidity | MTL/market-style intent cannot ensure a fill. [S10] | A floor-locked sale can remain pending; an alert is not an executed trade |
| Lots and ticks | Board and instrument rules determine valid quantity/price increments. [S10] | Initial round-lot mode uses 100 shares; preserve imported odd-lot holdings without rounding them away |
| Sale tax | Individual securities sales ordinarily include a 0.1% tax on sale value, not profit. [S13] | Use effective-dated, configurable costs and verify treatment for the user's account/events |

Treat these as requirements for a simulator and alert engine, not permission to execute orders. Corporate-action deliveries, trading suspensions, account restrictions, and actual broker reconciliation can override a simple calendar estimate.

Daily OHLCV does not reveal order-book queues, intraday price ordering, or afternoon-only fill availability. Where those facts affect a result, use an explicitly conservative convention or mark the result indeterminate. A backtest must disclose that limitation.

## 6. Proposed architecture and repository layout

Prefer one local Python application with clear modules. The proposed stack is Python, pandas/NumPy, SQLite, scikit-learn, LightGBM, and Streamlit. Choose and lock compatible versions during implementation. LightGBM supports CPU execution; a GPU is unnecessary for the proposed first model. [S14]

| Layer | Responsibility |
| --- | --- |
| Provider adapters | Retrieve documented data and expose source capabilities/errors |
| Ingestion and normalization | Normalize units/timestamps, validate records, update cached history |
| Data store | Preserve observations, revisions, account records, runs, and model metadata |
| Features | Compute technical, financial, market, and sector features as of a decision time |
| Research and ML | Baselines, label construction, chronological evaluation, training and model registry |
| Signal policy | Convert analysis/ranks into conditional plans with explicit expiry |
| Risk and settlement | Determine assessability, sizing limits, sellable quantity, and risk reasons |
| Alerts and journal | Persist state transitions and outcomes; deliver configured notifications |
| Dashboard and CLI | Expose status, candidates, holdings, historical decisions, and operator controls |

Suggested paths are a scaffold, not evidence that these files exist:

| Path | Purpose |
| --- | --- |
| `pyproject.toml` and a lockfile | Reproducible dependencies and entry points |
| `src/ai_stock_scanner/config.py` | Validated settings and defaults |
| `src/ai_stock_scanner/providers/` | TCBS, optional Vnstock, and fixture/CSV adapters |
| `src/ai_stock_scanner/storage/` | Schema, migrations, queries, and snapshots |
| `src/ai_stock_scanner/features/` | Technical, financial, and market feature builders |
| `src/ai_stock_scanner/models/` | Baselines, training, scoring, evaluation, registry |
| `src/ai_stock_scanner/policy/` | Entry/exit policy and plan lifecycle |
| `src/ai_stock_scanner/risk/` | Settlement, constraints, stress, and sizing |
| `src/ai_stock_scanner/alerts/` | Inbox, digest, deduplication, optional transports |
| `src/ai_stock_scanner/ui/` | Streamlit pages |
| `src/ai_stock_scanner/cli.py` | Batch commands used by a local scheduler |
| `configs/example.yaml` | Non-secret defaults and empty user lists |
| `tests/fixtures/` | Synthetic and sanitized provider examples |
| `tests/` | Meaningful data, numerical, leakage, execution, and workflow tests |
| `docs/` | Setup, data capabilities, assumptions, model card, and operating notes |
| `data/` and `artifacts/` | Local runtime data/models; excluded from source control as appropriate |

Start with SQLite for simplicity. Add partitioned Parquet only if measured history volume or training performance warrants it. Avoid microservices, Redis, Kubernetes, a hosted database, and an LLM orchestration framework in Phase 1.

## 7. Data contracts and auditability

### 7.1 Minimum entities

| Entity | Minimum information |
| --- | --- |
| Security | Stable internal ID, ticker history, exchange, instrument type, sector/theme mapping with effective dates, listing/status dates |
| Market bar | Security ID, interval/session, OHLCV, turnover where known, price basis, unit, source, availability/retrieval timestamps |
| Trading snapshot | Reference/ceiling/floor, trading status, quote freshness, optional bid/ask and liquidity indicators |
| Corporate action | Event type, announcement/availability date, ex-date, effective/payment dates, adjustment terms, source |
| Financial observation | Company, statement type, fiscal period, metric/unit, consolidation basis, publication/availability/retrieval dates, revision ID |
| Account snapshot | Equity, available cash, pending cash, debt, source, reconciliation state, timestamp |
| Holding lot | Security, acquisition date, quantity, cost, expected settlement, broker sellability, original plan |
| Watchlist entry | Security, user tags/notes, creation date; no implied holding |
| Analysis run | As-of time, universe version, provider versions, coverage, errors, config/model IDs |
| Feature snapshot | Decision time, feature schema/version, values and missingness, input snapshot IDs |
| Signal/plan | State, side/context, reasons, price conditions, expiry, risk status, model/policy IDs |
| Alert delivery | Event key, channel, attempts, delivered status, timestamps, failure reason |
| Journal/outcome | Submitted/actual fills when known, costs, realized/unrealized results, deviations, outcome status |

Keep immutable identifiers even when human-readable tickers or exchange assignments change. Record overlapping sector themes separately from a single industry classification so concentration is not understated.

### 7.2 Time, units, and missing data

- Store timezone-aware timestamps; use `Asia/Ho_Chi_Minh` for exchange sessions and the UI's trading-day interpretation. Do not use the host's UTC date as the exchange date.
- Distinguish event/report period, original publication time, first locally observed time, and retrieval time. A report's quarter end is not its public availability date.
- A provider's daily-bar timestamp can label the session rather than the time its completed OHLCV became available. Never infer that a whole day's close/high/low were known that morning from the timestamp alone.
- Normalize execution prices to VND per share and quantities to shares. Validate each endpoint's units; do not assume every provider uses the same scale. Some Vnstock market outputs use thousand-VND prices. [S8]
- Preserve raw and adjusted series separately. Store the adjustment method and snapshot/version. Never double-count a dividend through both an adjusted return and a cash-flow credit.
- Validate OHLC relationships, duplicate keys, non-negative volume, date continuity against the calendar, extreme scale changes, and corporate-action consistency.
- Missing financial statements, missing flow data, zero volume, and a provider error are different states.
- Do not forward-fill executable prices through suspension, silently fill unavailable financials with zero, or infer a holding from a favorite ticker.
- Do not overwrite historical forecasts or previously observed statement versions when a provider restates its data.

### 7.3 Scan coverage

For every scan report total universe size, attempted securities, successful analyses, stale inputs, ineligible securities, insufficient history, and provider failures. Record separate denominators for technical coverage, financial coverage, and model eligibility.

Use holdings/watchlist priority followed by resumable market batches when quotas are tight. A partial scan must say **partial**; it must not claim to identify the best stocks in the entire market. A watchlist breadth statistic must not be labeled whole-market breadth.

## 8. Analysis specification

### 8.1 Technical features

Start with a small, documented set:

- Returns/momentum over several fixed lookbacks, such as 5, 20, and 60 sessions.
- Distance from moving averages and recent highs/lows.
- Volatility and ATR-style range measures.
- Relative volume and available turnover/liquidity measures.
- Relative strength against the chosen benchmark and sector.
- Explicit breakout/pullback conditions and distance from invalidation.

Indicators are inputs or testable rules, not proof of predictability. Each feature needs an as-of definition, warm-up requirement, adjustment basis, and missing-data behavior. Compute rolling features using only information available by the decision timestamp.

### 8.2 Financial analysis

Summarize supported metrics such as revenue/profit growth, profitability, cash generation, debt, and valuation. Show source period, publication date where known, and missing fields.

Use sector-appropriate interpretation. Bank funding and credit quality cannot be scored as if the bank were an industrial company's debt/cash-flow profile. For banks, use relevant banking metrics only when reliable inputs exist; do not invent NPL, NIM, capital adequacy, or provisioning data from incomplete statements.

Handle negative profit bases, non-comparable periods, restatements, cumulative versus standalone quarterly cash flows, and consolidated versus parent-only reports. Do not display meaningless percentage growth or P/E when the denominator invalidates the interpretation.

**Financial analysis is part of Phase 1. Historical ML financial features are conditional.** If public availability and historical versions cannot be established, show current financial context and exclude those fields from retrospective training. A latest financial summary must never be retroactively attached to earlier trades.

### 8.3 Market and sector context

Show index trend, participation within the covered universe, and sector relative strength. Include Banks, Securities, Real Estate, Steel, and Public Investment themes when classifications support them.

An initial observational heuristic from the discussion compares VN-Index with its 50-session moving average and covered-universe participation above a 20-session average. Agreement suggests stronger/weaker conditions; disagreement suggests mixed conditions. Thresholds are unvalidated proposals.

Market features can enter a tested model. A separate rule that blocks trades in a regime must demonstrate value against the same model without that block. Do not silently turn the observational panel into a proven market-timing filter.

### 8.4 ML role and explanation

The model ranks eligible opportunities for a defined horizon. A separate policy supplies entry conditions, invalidation, exit rules, expiry, and position constraints.

Use deterministic explanation templates initially. Feature importance or an attribution explains what influenced a model output, not a causal reason a stock must rise. An optional later LLM can summarize verified facts and journal notes; it cannot supply missing prices, do authoritative sizing, or invent model evidence.

## 9. ML training and evaluation contract

### 9.1 First research question

> Among stocks eligible using information available after session t, which rank best for a proposed 10-session holding horizon after estimated costs?

This is a proposed default because the user has not specified a holding period. Train across many eligible stocks, not one independent model per favorite ticker.

### 9.2 Baselines and initial model

1. A transparent technical rule/ranking baseline with its parameters frozen before evaluation.
2. A simple statistical regression baseline on the same features and target.
3. A CPU LightGBM regression model whose predictions are used for ranking.

Regression-to-rank is the simplest first implementation. A dedicated ranking objective or classifier is a later experiment, not a prerequisite. Never convert a raw score or percentile into a probability of profit.

As an implementable **research-only baseline**, agents may start with a 20-session relative-strength rank and one explicit trend/setup filter. Document the precise formula, warm-up, entry/exit policy, and costs before testing. Do not tune many variants and present the best as a preselected rule.

### 9.3 Labels and timing

For a simple ranking label, define features after session `t`, candidate entry at a specified next-session price convention `e`, and a target exit ten trading sessions after `e`. Freeze the convention in a versioned label specification.

For example, a next-open-to-open forward-return proxy uses entry at the next session's opening price and exit at the opening price ten exchange sessions after entry, less estimated costs. Handle corporate actions consistently. This is a **research price proxy**, not proof that either order could have filled.

- Do not enter at the same closing price that was required to generate an after-close signal.
- Preserve label-window start/end dates, missingness, and any suspected non-executable observation.
- Missing exits, suspensions, and disappeared securities are not zero returns or convenient dropped losers. Report the unresolved cohort and the resulting selection bias.
- Model ranking quality and executable-policy performance are separate evaluations.
- Re-evaluate the target if the chosen live entry/exit policy differs materially from the training horizon.

### 9.4 Leakage and selection controls

- Use chronological walk-forward splits, grouping all stocks from a decision date together.
- Purge training/validation samples whose future label intervals overlap the following evaluation period. Use actual label windows, not an assumed row gap in a ticker-stacked table.
- Fit imputation, scaling, feature selection, and calibration within the training data of each fold.
- Preserve a final untouched time period. Tune only using earlier training/validation periods.
- Use historical universe membership, delisted/transferred securities, and historical corporate-action/financial availability where recoverable.
- If only today's listed universe is available, explicitly label the survivorship limitation and restrict claims.
- Track every materially different experiment and parameter search. A large number of attempted strategies weakens apparent holdout evidence.
- Avoid features based on future revisions or adjustment factors unavailable at the decision time, especially absolute-price/volume features.

### 9.5 Executable-policy simulation

Evaluate model and baseline using the same accounting and execution assumptions:

- Cash, board-lot rounding, entry conditions, fees, sale tax, slippage, and unsettled sale proceeds.
- Entry/exit timing, lot settlement, suspensions, price bands, partial fills, and failed exits.
- Exposure caps and simultaneous signals competing for the same capital.
- Corporate actions, dividends and adjustments without double counting.
- Equity marked to available prices including open holdings; report stale marks separately.
- After-close invalidations produce subsequent-session actions. Do not simulate intraday stop execution unless that preplanned policy and data resolution justify it.

For daily-bar-only research, choose a conservative, documented fill convention and sensitivity analysis. A price touch alone is not proof of a fill. If a stop and target both appear reachable within one bar, do not select the favorable path without evidence.

Do not erase an unsold position at the horizon, force its exit at the stop, or treat a floor-locked position as cash. Preserve pending exits and show mark-to-market and liquidation uncertainty.

### 9.6 Metrics and promotion

| Area | Required measures |
| --- | --- |
| Ranking | Rank correlation, top-k results, coverage, and stability by period/sector |
| Economic performance | Net expectancy, total return, equity drawdown, turnover, exposure, and tail losses |
| Execution realism | Unfilled/partial/delayed exits, settlement conflicts, unavailable cash, and indeterminate observations |
| Comparison | Baseline versus ML under identical constraints; regime/risk changes isolated and compared at similar exposure |
| User value | Rule adherence, avoidable violations, alert usefulness, time spent operating the system |
| Reliability | Freshness, successful coverage, delivery failures, duplicate alerts, and missed jobs |

Promotion requires reproducible leakage checks, an explicit baseline comparison, plausible costs/execution, and evidence across more than one chronological period. Freeze a promotion rubric before looking at the final holdout; do not invent a guaranteed Sharpe or win-rate target.

If the model adds no credible value, retain it as experimental and keep the transparent baseline available. This is a valid research result, not a reason to hide the comparison. With insufficient history, show `ML_UNAVAILABLE`; a fixture or heuristic score must never masquerade as a trained model.

## 10. Signal and alert contract

### 10.1 User-facing states

| State | Meaning |
| --- | --- |
| `ENTRY_SETUP` | Conditional entry plan meets configured research/policy criteria |
| `WAIT` | Analyzed, but no qualifying entry condition |
| `WEAKENING` | Setup deteriorated; ownership not assumed |
| `EXIT_REVIEW` | A real holding meets a configured review/exit condition |
| `TAKE_PROFIT_REVIEW` | A real holding reaches a specified profit-taking condition |
| `INVALIDATED` | A saved setup/holding plan's invalidation condition has occurred |
| `INSUFFICIENT_DATA` | Required input/history is unavailable or unusable |
| `EXPIRED` | Entry window elapsed or plan superseded |

Keep analysis state, model availability, risk status, and execution availability separate. For example, a setup can exist while sizing is unavailable, or an exit-review can be urgent while sellable quantity is zero. Never suppress an important holding warning merely because a sale cannot execute.

### 10.2 Each saved plan includes

- Security/exchange; watchlist, holding, or discovery context.
- Generated time, market-data as-of time, and source coverage/freshness.
- Model/version, policy/config version, and input snapshot IDs.
- Model rank/score and an honest score label; probabilities only after separate calibration/validation.
- Technical reasons, available financial context, market/sector context, and material counterarguments.
- Entry trigger and acceptable price interval, conditional on the next available session.
- Invalidation level, time exit, and proposed target/trailing policy where defined.
- Expiry and reasons that cancel or replace the plan.
- Risk status and reason codes, permitted quantity if assessable, and settlement/sellability information.
- Status of required assumptions: costs, account snapshot, corporate-action data, and liquidity.

“Buy/sell points” means conditional plans, not a promise that a precise future turning point can be known.

### 10.3 Delivery behavior

- Generate a daily digest and event notifications for meaningful state changes, invalidation, and important operational failures.
- Persist the event before delivery. Use an idempotency key based on security, plan/policy version, event type, and relevant session/state transition.
- A digest can repeat the latest state; repeated scans should not create duplicate event notifications.
- Keep delivery attempts separate from signal generation; retry boundedly without losing the original event.
- Start with the local inbox/digest. Add the user's chosen external channel after its destination and credentials are configured.
- Clearly label synthetic/demo alerts. Do not deliver them to external recipients by default.

End-of-day operation cannot provide immediate intraday exit detection. Intraday monitoring is a later mode requiring a tested streaming feed, an awake service, and distinct freshness/delivery requirements.

## 11. Proposed risk controls

These were conservative pilot proposals in the panel discussion. They are **not confirmed user preferences or optimal allocations**. Store them as editable research defaults, show them transparently, and do not issue personalized sizing while account inputs are unknown.

| Control | Proposed initial setting |
| --- | --- |
| New borrowing | Disabled in the proposed strategy |
| Planned per-trade risk | Maximum 0.5% of current account equity, including modeled costs |
| Position stress loss | Maximum 1% of equity under the selected adverse scenario |
| Portfolio heat | Maximum 1.5% of equity in aggregate modeled stop losses |
| Joint portfolio stress | Maximum 3% of equity under the selected simultaneous shock |
| Single-name exposure | Maximum 10% of equity |
| Sector/theme exposure | Maximum 20% of equity, accounting for overlapping themes |
| Initial liquidity screen | At least VND 10 billion median matched turnover over 20 sessions |
| Initial order participation | Order value at most 0.1% of that median turnover |
| Drawdown response | At 4%, halve proposed new-trade risk; at 6%, pause new entries for review |
| Critical stale/missing inputs | `CANNOT_ASSESS`, never a fabricated approval |

Apply liquidity filters to new-entry eligibility; continue monitoring existing holdings that fail those filters. If only total turnover is available, do not label it matched turnover or silently claim the matched-turnover test passed.

For a long trade with entry price `P`, invalidation `S`, cost allowance `c` per share, equity `E`, and lot size `L`:

```text
planned_loss_per_share = P - S + c              # require P > S
q_planned = floor_to_lot(0.005 * E / planned_loss_per_share, L)
q_stress  = floor_to_lot(0.01  * E / stress_loss_per_share, L)
q_allowed = min(q_planned, q_stress, q_cash, q_name, q_sector,
                q_liquidity, q_remaining_heat, q_remaining_joint_stress)
```

Round down, never up. Include existing exposure, pending commitments, costs, and incremental risk. A zero result means no permissible new purchase under these settings. A missing critical input means unknown, not zero capital or an automatic rejection of all market analysis.

Use actual broker fees and nonlinear charges where applicable rather than relying forever on a constant per-share allowance. Recalculate available quantities at execution-review time; a saved plan is not a reservation of broker cash.

Drawdown must use a defined, deposit/withdrawal-adjusted equity series. A threshold triggers a response; it cannot guarantee that losses stop at that level. Portfolio heat is a stop-loss model, not a bound on losses in a floor lock.

Do not use Kelly sizing in Phase 1. Estimated probabilities/payoffs and unbounded stop slippage are too uncertain. If existing margin is reported, import debt and collateral information before labeling account-level risk complete; no-new-margin is not the same as debt-free.

## 12. Dashboard and configuration

### 12.1 Minimum screens

| Screen | Essential content |
| --- | --- |
| Overview | Last successful run, freshness, coverage, provider/auth status, market context, important holding alerts |
| Favorites | Editable watchlist, every ticker's state, technical/financial summary, saved plan |
| Holdings | Lots, settled/unsettled quantity, sellability, actual plan, modeled risk, reconciliation gaps |
| Discovery | Eligible ranked candidates, rejection reasons, exchange/sector filters, empty/partial states |
| Stock detail | Price history, indicator definitions, statement periods, model evidence, risks, signal history |
| Research | Baseline/ML comparison, date splits, costs, exposure, drawdown, limitations, model card |
| Journal | Plans, actual fills/imports, deviations, idea source, outcome status, notes |
| Settings | Sources, empty watchlist/holdings import, horizon, proposed risk settings, alert channel, secrets setup |

### 12.2 Example non-secret configuration

The following is a proposed schema for implementation, not a working application config. `null` values are intentionally unresolved and must not be replaced with guessed account details.

```yaml
project_name: AI_Stock_Scanner
broker: TCBS
exchange_timezone: Asia/Ho_Chi_Minh
mode: paper
analysis_frequency: end_of_day
model_horizon_sessions: 10  # proposed; user has not confirmed
watchlist: []
holdings: []
universe_exchanges: [HOSE, HNX, UPCOM]

data:
  preferred_broker_adapter: tcbs_official
  optional_history_and_financial_adapter: vnstock_community
  allow_fixture_mode: true
  require_fresh_inputs_for_new_plans: true

account:
  equity_vnd: null
  available_cash_vnd: null
  existing_margin_debt_vnd: null
  reconciliation_status: unknown

risk:
  use_new_margin: false
  max_planned_trade_risk_fraction: 0.005
  max_position_stress_fraction: 0.01
  max_portfolio_heat_fraction: 0.015
  max_joint_stress_fraction: 0.03
  max_name_exposure_fraction: 0.10
  max_sector_exposure_fraction: 0.20
  round_lot_shares: 100

alerts:
  in_app_enabled: true
  daily_digest_enabled: true
  external_channel: null
  external_destination: null

execution:
  broker_order_submission_enabled: false
```

Provider keys, tokens, passwords, and iOTP values must never be committed or inserted into this file. Configure secrets locally using documented mechanisms. Keep logs, screenshots, fixtures, and model reports free of credentials and sensitive account identifiers.

## 13. Agent work packages and dependency order

These packages can be assigned to separate coding agents or completed sequentially by one agent. They are planning assignments; no agents have been launched by this handoff.

| ID | Work package / owner role | Deliverables | Depends on | Completion evidence |
| --- | --- | --- | --- | --- |
| P0 | Foundation / technical lead | Repo scaffold, dependency lock, config validation, fixture mode, decision log | None | One documented command runs a labeled demo without credentials or user tickers |
| P1 | Data / data engineer | Capability report, normalized schema, calendar, ingestion/cache, provider adapters and imports | P0 | Unit/adjustment checks, resumable updates, explicit auth/quota/error states |
| P2 | Analysis / quant engineer | Technical features, current financial summaries, market/sector view, baseline | P1 contracts | Dated features, sector-aware output, explicit missing financials |
| P3 | ML / research engineer | Labels, chronological splits, statistical and LightGBM models, registry/model card | P1–P2 | Reproducible baseline comparison with leakage and execution limitations disclosed |
| P4 | Policy and risk / risk engineer | Plan lifecycle, lot settlement, size constraints, stress, execution simulator | P1 contracts; integrates P2–P3 | No premature sale, fabricated fill, or sizing on incomplete account data |
| P5 | UI and alerts / application engineer | Dashboard, inbox/digest, state transitions, imports, external-channel interface | P0–P1 contracts; integrates P2–P4 | End-to-end demo, valid empty/partial states, deduplicated event log |
| P6 | Integration and paper pilot / QA owner | Full pipeline, scheduler, operating guide, restore/export path, pilot report | P1–P5 | Tests pass; paper signals/outcomes retained; no broker trading mutations |

P4 and UI scaffolding can start against agreed schemas and fixtures while ML research proceeds. One owner should approve shared schema/config changes to prevent incompatible parallel implementations. Avoid multiple agents editing the same foundational module concurrently.

### Suggested delivery milestones

1. **Runnable foundation:** no credentials or stock list required; synthetic data clearly identified.
2. **Real data and analysis:** validated source adapter, watchlist/discovery workflows, current financial summaries, baseline plans.
3. **ML research:** reproducible training and walk-forward comparison; a model may remain experimental.
4. **Policy and alerts:** settlement-aware review, sizing where inputs exist, persistent inbox and digest.
5. **Paper operation:** reliable scheduled runs and recorded outcomes before promoting model use.

The earlier 2–4 part-time week estimate applied to a simpler risk co-pilot. A credible ML scanner was estimated at 6–12+ part-time weeks, with validation extending beyond implementation. Treat both as rough planning ranges; authentication, data history, and simulation quality can dominate effort. An 8–12-week pilot may establish usability, but cannot alone establish durable trading profitability.

## 14. Acceptance checks and failure scenarios

Use meaningful tests for the numerical, data, timing, and delivery failure modes below. Do not create tests merely to mirror getters or formatting choices.

| ID | Scenario | Expected result |
| --- | --- | --- |
| A01 | First launch, no tickers/holdings/credentials | Usable setup/empty screens and labeled fixture mode; no invented portfolio |
| A02 | Provider prices differ by a factor of 1,000 | Adapter normalization detects/corrects documented units; ambiguous units block affected sizing |
| A03 | Duplicate ingestion run or repeated scan | No duplicate bars, plans, or state-transition alerts |
| A04 | TCBS token expires | `AUTH_REQUIRED`, retained timestamps/cache, no fresh-data claim or fabricated success |
| A05 | Quota stops a universe scan halfway | Partial coverage with exact completed/failed counts; resumable next batch |
| A06 | One favorite lacks statements | Technical result with explicit financial gaps; no invented ratios |
| A07 | Financial report is published after a historical decision | Its features are absent from that decision's training snapshot |
| A08 | Train/test outcome windows overlap | Split validation rejects or purges the overlap |
| A09 | New lot purchased before a weekend/holiday | Exchange-calendar settlement; newly acquired quantity unavailable before eligible time |
| A10 | Same stock has old settled and new unsettled lots | Sellability is lot-aware, bounded by broker state; total holding is not treated as all sellable |
| A11 | Stop is crossed while shares cannot be sold | Warning retained; pending exit, no fictional stop fill |
| A12 | Floor lock or no opposing liquidity | No guaranteed sale; unsettled/pending position remains in equity/risk reporting |
| A13 | Opening price gaps outside the permitted entry range | Skip/reassess according to the saved policy; do not fill at yesterday's attractive price |
| A14 | Daily bar reaches both stop and target | Conservative documented ordering or indeterminate result; no favorable hindsight |
| A15 | Corporate action changes price/share count | Consistent holdings and return treatment; no fake crash or double dividend |
| A16 | Missing account equity/cash/debt state | Discovery works; personalized sizing/risk completeness shown as unavailable |
| A17 | Actual commission is zero but other costs remain | Applicable tax, exchange/other charges, and slippage still modeled |
| A18 | Minimum permitted size is below one configured lot | Zero allowed new purchase; no rounding up |
| A19 | Unowned favorite weakens | Setup warning, not a sell quantity |
| A20 | Model has no trained/validated artifact | `ML_UNAVAILABLE` or experimental label; baseline output identified honestly |
| A21 | Only today's survivors exist in history | Research limitations visibly flag survivorship bias |
| A22 | Alert transport fails | Persist event, bounded retries, delivery status, no signal loss or duplicate dispatch |
| A23 | Deposit/withdrawal occurs | Cash-flow-adjusted performance/drawdown avoids false gains/losses |
| A24 | Three simultaneous buys compete for cash/sector room | Sequential reservation/simulation respects aggregate constraints |
| A25 | Empty scan or no eligible opportunities | Valid no-candidate result; never force a top buy |
| A26 | Source revision or model retraining occurs | Historical forecasts remain immutable and traceable to the original versions |
| A27 | Host sleeps through scheduled analysis | Missed-run/catch-up status; no backdated claim that an alert was delivered on time |
| A28 | UPCoM or a restricted stock is unsupported | Visible eligibility/coverage reason; no silent claim of full-market support |

A developer-ready release requires documented setup, locked dependencies, an end-to-end fixture demonstration, passing relevant tests, a capability report, and a model card that separates measured results from untested assumptions. Real-data operation additionally requires verified access and a reconciled configuration.

## 15. Operating workflow

1. Load settings and provider capabilities; validate the exchange session/calendar.
2. Obtain or verify authorization, then incrementally update required market inputs.
3. Reconcile holdings/account data if configured; preserve unknown or stale fields.
4. Validate and snapshot inputs, recording coverage and data-quality failures.
5. Compute features and current financial summaries as of a declared cutoff.
6. Run the transparent baseline and any available approved/experimental model.
7. Create or update conditional plans; apply independent risk and sellability checks.
8. Save the analysis run, plans, and events before displaying/delivering alerts.
9. Generate the digest and deliver only configured channels.
10. Update subsequent observed outcomes without rewriting historical predictions.

Schedule by completed data and an exchange calendar, not just a fixed wall-clock assumption. If data are late, retry boundedly and surface incomplete analysis. A local scheduler runs only while the machine/service is available.

Retrain on a deliberate versioned schedule after enough new data are available, not whenever a day's predictions look disappointing. Retain the previous model for rollback; keep training and inference schemas compatible.

## 16. Open decisions for later configuration

| Question | Needed before | Safe development default |
| --- | --- | --- |
| Which favorites? | Personalized watchlist analysis | Empty watchlist and fixture examples |
| Which actual holdings/lots? | Holding-specific exits and portfolio risk | No claimed holdings; import interface |
| Usual holding horizon? | Final label/strategy selection | Proposed 10-session horizon, configurable |
| Preferred alert channel/destination? | External delivery | In-app/local only |
| Account size, cash, and existing margin? | Personalized sizing and complete portfolio risk | Unknown; unsized analysis only |
| TCBS and optional data credentials? | Authenticated integration validation | Fixture/CSV mode and documented adapter contracts |
| OS and machine uptime? | Reliable local scheduling | Manual CLI run plus setup notes |
| Actual costs and desired limits? | Account-specific simulation and sizing | Explicit research-only assumptions |

Do not block unrelated implementation on these answers. Ask for them at the relevant setup milestone, not repeatedly during scaffolding. Never request passwords, access tokens, or iOTP values in a shared Markdown file or source-control commit.

## 17. Copyable kickoff prompt for coding agents

```text
You are implementing AI_Stock_Scanner using this handoff as the product specification.

Confirmed user direction:
- ML-assisted financial and technical analysis of Vietnamese equities.
- Watchlist entry/exit-review alerts plus broader HOSE/HNX/UPCoM discovery.
- Broker: TCBS.
- Free-first, local, solo-user implementation.
- Favorite tickers will be provided later. Holdings, account inputs, horizon,
  and alert channel are not yet confirmed.

Start by inspecting the existing repository and applicable project instructions.
Preserve existing work. If no project exists, create a small Python application
with reproducible dependencies, validated configuration, SQLite storage,
provider interfaces, synthetic fixtures, and a Streamlit dashboard/CLI.

Deliver P0 and a thin P1/P2/P5 vertical slice first: a clearly labeled demo that
loads data, analyzes a watchlist or discovery universe, creates conditional
plans, and persists an in-app digest. Empty user configuration must work.
Then implement real supported data access, baselines, actual ML training and
chronological evaluation, settlement/risk checks, and the paper workflow.

Verify current official TCBS OpenAPI documentation and real account entitlement.
Handle token expiry honestly. Evaluate permitted Vnstock Community data where
it fills an observed need. Do not depend on undocumented endpoints or a paid
service. Keep credentials local and out of the repository.

Keep favorites separate from holdings. Mark unknown data explicitly. Do not
invent live prices, owned shares, financial values, model results, or account
limits. A baseline is not a trained ML model. A ranking score is not a calibrated
probability. Missing account inputs must prevent personalized sizing, while
allowing unsized research and discovery to continue.

Use point-in-time features, date-grouped chronological validation, purged
overlapping labels, and a held-out period. Evaluate costs, settlement, cash,
corporate actions, partial/no fills, and floor locks. Preserve original signals
before outcomes are known. Compare ML against the transparent baseline.

Phase 1 is analysis and alerts with manual execution. Do not implement broker
order/transfer mutations. Keep external notifications disabled until the user
configures a channel and destination. The 10-session horizon and risk settings
are proposed defaults, not confirmed account facts or proven trading rules.

Work in small reviewable milestones. For each milestone, provide changed files,
run instructions, relevant test results, known limitations, and the next task.
Keep implementation moving on fixtures/imports if credentials or tickers are
unavailable. Do not stop at architecture prose; deliver working code within
the assigned milestone and accurately distinguish demo from real-data behavior.
```

## 18. Earlier panel: assumptions and root-cause diagnosis

The initial problem was consistently poor retail trading performance. The initial idea was an AI buy/sell predictor. Five perspectives challenged whether prediction, behavioral diagnosis, risk controls, or market context would have the largest practical effect.

### 18.1 Original assumptions, not user facts

| Dimension | Original panel assumption | Current interpretation |
| --- | --- | --- |
| Style | Long-only swing trades, roughly 3–15 sessions | Later ML proposal used 5–20; neither is user-confirmed |
| Capital | VND 100–500 million; VND 200 million examples | Unknown actual account size |
| Margin | Possibly used; no new borrowing proposed | Unknown existing usage |
| Coverage | Monitor all three exchanges; initially screen liquid HOSE/HNX names | User wants wider-market discovery; stage coverage openly and include UPCoM eligibility reporting |
| Technical ability | Able to learn Python and maintain a local app | Assumption, not established skill level |
| Budget | VND 0 recurring data/software cost target | Consistent with the user's free preference |
| Execution | Manual order placement | Phase 1 design |

### 18.2 Competing explanations for losses

| Possible cause | Evidence to inspect | Useful software response |
| --- | --- | --- |
| Late breakout entries | Entry distance from planned trigger and adverse movement before sellability | Entry range/expiry, settlement exposure, plan history |
| FOMO from social rooms | Results and violations by idea source | Journal provenance and a required plan |
| Averaging down/strategy drift | Additions after invalidation; intended swing becoming a long-term holding | Flag unplanned additions and changed exits |
| Oversizing/concentration | Worst-loss contribution and sector exposure | Fixed-fractional sizing, concentration, joint stress |
| Margin pressure | Debt, collateral changes, financing costs, forced sales | Broker-specific reconciliation and risk completeness |
| No underlying strategy edge | Compliant trades still lose after costs | Baseline/ML research and strategy rejection when evidence fails |

These are hypotheses, not findings about this user. A useful optional diagnostic is the last 50–100 completed trades, or all available history, plus deposits, withdrawals, costs, and open positions. Do not reconstruct an absent original plan after seeing the outcome; record it as unknown.

The key distinction is between rule-adherent expectancy and losses associated with violations. Better discipline can reduce avoidable damage without creating positive expectancy.

## 19. Earlier panel: independent assessments and cross-examination

### 19.1 Five roles

| Role | Initial blueprint | Primary objection |
| --- | --- | --- |
| Product Owner (PO) | A small pre-trade screen showing permitted size, settlement, and portfolio impact | A large scanner may miss the actual cause if a few oversized losses dominate |
| Business Analyst (BA) | Journal separating strategy, execution, behavior, and costs | Calling every loss poor discipline can conceal a losing strategy |
| Tech Lead (TL) | Reliable daily data, deterministic rules, reproducible evaluation | Leakage and unrealistic fills can manufacture model performance |
| Vietnam Stock Trader Expert (VSTE) | Liquidity, settlement-aware plans, sector participation | A breakout that requires an exit before new shares are sellable may be unusable |
| Financial Risk Expert (FRE) | Fixed-fractional sizing plus stress and concentration constraints | A stop price does not bound the realized loss |

### 19.2 Debate that shaped the design

**Exchange 1 — Prediction target versus trade path.** TL proposed forecasting multi-day returns. VSTE challenged whether the stock could become unsellable or cross invalidation before settlement. FRE challenged assumed liquidity and financing. Outcome: a price forecast requires a separate executable policy; directional accuracy is insufficient.

**Exchange 2 — Guardrails versus strategy edge.** PO prioritized oversized trades and averaging down. BA challenged the claim that preventing violations would necessarily create profits. FRE agreed that risk controls slow capital destruction but do not create an edge. Outcome: measure compliant trades separately and test the underlying strategy.

**Exchange 3 — Sector rotation versus inferred smart money.** VSTE emphasized sector rotation, breadth, and participant flows. TL objected that turnover and participant categories do not establish motives; trading can include hedging. PO challenged the cost and complexity of complete institutional-flow feeds. Outcome: start with price/participation; optional verified flows stay separate and absent values remain unknown.

**Exchange 4 — More alerts versus better decisions.** TL proposed alerts across breakouts, volume, news, and sectors. BA warned that volume of alerts can increase FOMO and turnover. VSTE challenged after-close signals assuming same-close fills. Outcome: actionable conditional plans, expiry, deduplication, and holding/risk changes take priority over alert quantity.

**Exchange 5 — Detailed risk models versus solo development.** FRE proposed correlation, collateral, and floor-lock modeling. PO challenged the implementation burden. TL proposed simpler exposure/stress rules and no new borrowing. BA requested comparable-exposure evaluation. Outcome: simple inspectable controls first; broker-specific margin simulation later if required.

The earlier consensus was a pre-trade risk co-pilot with a journal and an observational regime panel. The user then chose an ML scanner. The current specification adopts that choice while preserving these design constraints.

## 20. Earlier decision gate and illustrative calculations

### 20.1 Five product directions considered

| Direction | Best fit | Main trade-off | Original rough effort |
| --- | --- | --- | --- |
| A. Trading Journal & Behavior Coach | Loss causes are unclear | Fast diagnosis, few new ideas | About 1 part-time week |
| B. Pre-Trade Risk & Settlement Co-Pilot | Oversizing/settlement/concentration dominate | Reduces avoidable damage without creating strategy edge | About 2–4 weeks |
| C. Market Regime & Sector Rotation Filter | Setup quality depends on conditions | Can miss recoveries; free flow coverage incomplete | About 2–3 weeks |
| D. Transparent Scanner & Strategy Lab | Need a consistent testable method | Requires realistic simulation and may find no profitable rule | About 3–6 weeks |
| E. ML Buy/Sell Predictor | Clean data and a credible baseline are available | Highest overfitting and maintenance burden | About 6–12+ weeks |

The user selected an ML-assisted version of **E**, incorporating financial/technical analysis, favorites monitoring, alerts, and market discovery. Elements of A–D support it; they are not replacement product choices.

### 20.2 Expectancy example

```text
Expectancy = win_probability * average_win
           - loss_probability * average_loss
           - average_costs

Example: 0.65 * 0.7R - 0.35 * 1.8R - 0.08R = -0.255R per trade
```

A 65% win rate can lose money. `R` is initially planned risk; actual losses can exceed it. Avoid double-counting costs when average wins/losses are already net.

### 20.3 Position-sizing example

All numbers below are hypothetical and do not describe the user's account.

| Input | Value |
| --- | --- |
| Equity | VND 200,000,000 |
| Entry | VND 30,000/share |
| Invalidation | VND 28,500/share |
| Round-trip costs/slippage allowance | VND 150/share |
| Planned-risk budget | 0.5% of equity = VND 1,000,000 |
| Stress scenario | 20% price decline plus the same illustrative costs |
| Stress budget | 1% of equity = VND 2,000,000 |
| Round-lot convention | 100 shares |

```text
Planned loss/share = 30,000 - 28,500 + 150 = 1,650 VND
Planned-risk size  = floor_to_100(1,000,000 / 1,650) = 600 shares

Stress loss/share  = 30,000 * 20% + 150 = 6,150 VND
Stress-risk size   = floor_to_100(2,000,000 / 6,150) = 300 shares
```

The stress constraint reduces the permissible size to at most 300 shares before the other constraints are applied. A stop-only calculation would permit twice as many shares.

For an ordinary HOSE scenario, two successive 7% declines compound to about 13.51%; three compound to about 19.56%, ignoring tick rounding and special events. These are arithmetic scenarios from a starting reference/closing level, not maximum losses from a particular entry. Continued floor locks, entry-day movement, and account leverage can worsen outcomes.

### 20.4 Original risk MVP retained as supporting capabilities

The original Phase 1 proposal contained a journal/account reconciliation, pre-trade ticket, holdings/risk alerts, and a small regime panel. Its validation questions remain useful:

1. Is accounting correct against broker records?
2. Could the simulated trade actually be executed?
3. Does each added component help beyond the baseline at comparable exposure?
4. Does evidence survive chronological evaluation and realistic costs?

An application-level rejection cannot stop the trader placing a separate broker order. A sell alert cannot create buyers. A drawdown response cannot enforce a guaranteed maximum loss. These practical limits should remain visible where they affect a decision.

## 21. Source register and verification boundaries

The references below support specific market/data statements, not the profitability of any proposed model, threshold, or strategy. All architectural choices and risk settings in this handoff are design proposals. Account-specific access, costs, and live responses remain untested.

| ID | Primary source | Used for |
| --- | --- | --- |
| S1 | [TCBS OpenAPI developer portal](https://developers.tcbs.com.vn/) | Official API existence, market coverage, supported capabilities |
| S2 | [TCBS OpenAPI workflow](https://developers.tcbs.com.vn/docs/v1.0.0/workflow/) | Free registration, authentication workflow, token lifetime |
| S3 | [TCBS token exchange](https://developers.tcbs.com.vn/docs/v1.0.0/auth/token/) | API-key/iOTP authentication endpoint |
| S4 | [TCBS long-term OHLCV](https://developers.tcbs.com.vn/docs/v1.0.0/stock/bars-long-term/) | Documented daily/weekly/monthly history endpoint |
| S5 | [TCBS stock assets](https://developers.tcbs.com.vn/docs/v1.0.0/stock/asset/) | Documented account stock-assets endpoint |
| S6 | [Vnstock account levels and limits](https://www.vnstocks.com/docs/vnstock/tham-khao/cap-quyen-va-gioi-han) | Free-tier history, financial periods, quota/device restrictions |
| S7 | [Vnstock financial data](https://www.vnstocks.com/docs/vnstock/co-ban-fundamental) | Statement availability and restricted detail/ratio functions |
| S8 | [Vnstock market data](https://www.vnstocks.com/docs/vnstock/thi-truong-market) | Market-data semantics, units, foreign/proprietary-flow restrictions |
| S9 | [VNDirect settlement guidance](https://support.vndirect.com.vn/hc/vi/articles/9816355920153-Chu-k%E1%BB%B3-thanh-to%C3%A1n-ch%E1%BB%A9ng-kho%C3%A1n) | T+2 and business-day/afternoon availability |
| S10 | [SSI equity trading rules](https://www.ssi.com.vn/khach-hang-ca-nhan/quy-dinh-giao-dich/quy-dinh-giao-dich-co-phieu) | Bands, lots/ticks, sessions, and order behavior |
| S11 | [SSI UPCoM rules](https://www.ssi.com.vn/khach-hang-ca-nhan/quy-dinh-giao-dich-tai-upcom) | UPCoM reference-price definition |
| S12 | [SSI KRX FAQ](https://www.ssi.com.vn/khach-hang-ca-nhan/krx-thi-truong-co-so-faq) | ATO/ATC priority changes |
| S13 | [TCBS 2026 prospectus](https://www.tcbs.com.vn/wp-content/uploads/2026/03/3.-Ban-cao-bach.pdf) | Individual securities-transfer tax description; verify current applicability |
| S14 | [LightGBM parameters](https://github.com/lightgbm-org/LightGBM/blob/main/docs/Parameters.rst) | CPU execution and model capabilities |

Additional references retained from the earlier discussion, for optional future re-evaluation rather than required integration:

- [SSI FastConnect overview](https://developers.ssi.com.vn/docs/faq/service-overview)
- [SSI FastConnect market data](https://developers.ssi.com.vn/docs/faq/market-data)
- [DNSE API platform](https://developers.dnse.com.vn/docs/guide/intro/api_platform/)
- [DNSE AmiX FAQ](https://hdsd.dnse.com.vn/san-pham-dich-vu/ami-x/faq-amix)
- [Streamlit source repository](https://github.com/streamlit/streamlit)
- [scikit-learn TimeSeriesSplit documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

A generic time-series splitter alone does not solve overlapping financial labels, point-in-time universes, or execution realism. Verify provider/library versions and market rules again when implementing or changing an adapter; do not treat a dated planning document as a permanent API contract.
