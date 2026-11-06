# R06 Findings — Technical Features, Research Baseline and Market/Sector Context

**Researcher:** Codex, with BA/product, financial and trading/risk reviews · **Date:** 2026-11-06 (Asia/Bangkok) · **Spec:** [R06](../specs/R06_technical_market_context.md)

**Status: research contract drafted and synthetic checks completed; empirical literature review incomplete.** The feature definitions, baseline, context panel and Graham reference review below are concrete proposals. The required bibliography of at least eight verified relevant papers/reports, especially Vietnam evidence, is **not complete**. Academic retrieval was blocked by the active network policy; §4.1 separates verified material from a reading queue rather than inventing paper findings. No market-return data, ranks, strategy results or real-data backtests were examined for R06. The existing R02 capability report and backfill schema were inspected.

Evidence labels: **Documented** = read in a cited source; **Observed** = inspected repository/PDF/source or checked a synthetic example; **Inferred** = a proposed definition, policy or implication; **Unknown** = evidence not established. All numerical strategy thresholds below are **Inferred research choices**, not empirically validated optima.

## 1. Recommendation (read this first)

- **Recommend:** freeze `R06-RS20-SMA20-v1`, a 20-session cross-sectional return rank against VNINDEX, one trend condition (`close > SMA20`), and explicit eligibility/execution-data gates. Specify 19 candidate model features, but use only the named baseline inputs for this baseline. Keep market regime as context/model input, not an extra trade block.
- **Runner-up:** the same eligibility and timing contract with a 20-session breakout filter instead of the SMA20 condition. Retain it as a separately registered alternative, not a second condition silently added to v1.
- **Confidence:** high in the identified data limitations and reproducible definitions; low in any claim of Vietnamese predictive power. This pass establishes no trading edge or implementable return.
- **Would flip the choice:** verified Vietnam/comparable-market evidence showing a materially different appropriate horizon or mechanism, followed by a prospectively registered comparison under R08/R09. Any change gets a new version; preserve v1 and record whether results had been seen.
- **Needs user decision / gate:** no architecture, paid-service or broker change. Academic-domain additions have been saved to the environment draft but are not active. Missing public data semantics require R01/R02 evidence, not invented user inputs or credentials.

## 2. Answers to the research questions

| # | Question | Answer in this pass | Status / evidence |
| --- | --- | --- | --- |
| Q1 | Vietnam momentum/reversal, 52-week high, industry effects | No verified Vietnam paper retrieved. A 5–20-session edge is not established. The handoff's 20-session rank/10-session horizon is a hypothesis; monthly momentum results cannot automatically justify it. | Unknown for empirical VN conclusion; Inferred transferability warning; §4.1 |
| Q2 | Price limits | Separate a recorded limit touch from a lock, an executable order and future return. Raw prices, dated bounds and settlement state are required; existing adjusted bars cannot certify these states. Vietnam/China/Taiwan mechanism studies remain to be read. | Observed data gap [S2,S4]; Inferred handling §4.6; empirical mechanisms Unknown |
| Q3 | Liquidity/size | Retain VND 10bn median 20-session **matched turnover** as an unvalidated research gate. Number passing is unknown; do not substitute total exchange turnover or adjusted close × volume. | Documented proposed gate [S1]; Observed missing input [S2]; §4.3 |
| Q4 | Feature set | Nineteen definitions with warm-up, units, price basis and missingness; empirical support not overstated. | Inferred contract §4.4; candidate reading links §4.1 |
| Q5 | Frozen baseline | Explicit universe, percentile/tie rule, one trend condition, next-session entry convention, ten-session time exit and failure behavior. Freeze is before R06 outcome evaluation, not a claim nobody previously saw any data. | Inferred contract §4.5 |
| Q6 | Market/sector context | VNINDEX/SMA50, coverage-aware breadth, point-in-time sector return and separate overlapping themes. No automatic market-timing block. | Documented handoff default [S1]; Inferred panel §4.7 |
| Q7 | Explanations/SHAP | Deterministic evidence templates first. SHAP describes a model output relative to a reference distribution; it is not a price forecast guarantee, causal claim or calibrated win probability. | Documented authors' documentation [S6]; Inferred presentation contract §4.8 |

## 3. Options compared and team resolution

| Candidate | Benefit | Main limitation | Decision before evaluation |
| --- | --- | --- | --- |
| RS20 rank + close above SMA20 | Small, auditable specification consistent with handoff §9.2 | No verified VN edge; may chase late moves and be sensitive to reversal/costs | Freeze as v1 research baseline |
| RS20 rank + breakout above prior 20-session high | Explicit setup and simple explanation | More event/price-limit sensitivity; requires consistent highs and independent validation | Runner-up; separate version only |
| Rank by 5-session reversal + close above SMA20 | Tests a competing short-horizon mechanism | Different hypothesis; high turnover/settlement effects; no verified VN advantage here | Keep as a future registered comparator, not an ensemble |

**BA:** define every denominator, timestamp, missing state and eligibility reason; A20/A25/A28 must be visible. **Financial expert:** Graham informs discipline and the investment/speculation distinction, not the empirical validity of a ten-session trade. **Trading expert:** distinguish a ranking observation from a feasible next-session order and a filled position. **Risk expert:** retain raw-price/settlement/fee gates and unresolved exits; no guaranteed stop fill. **Product Owner:** keep free-first analysis-only scope, empty results and honest coverage; avoid adding untested filters or a paid data dependency by stealth.

The proposed P2/P3 flow is `versioned local input → quality/availability checks → point-in-time feature snapshot → eligibility and rank → one baseline trend condition → candidate plan → R09 execution assessment / R10 sizing → dated explanation and journal`. Market/sector context is a parallel view and optional model input, not a hidden second strategy filter.

**Files:** this R06 finding is the only repository change. Existing `scripts/backfill/backfill.py` and `tests/test_backfill.py` implement ingestion and fake-source ingestion checks; they do not implement technical features or models. R06 explicitly excludes real-data backtests and application code. Later implementation needs a separate P2/P3 task; it must not retrofit the existing crawler into a trading engine.

## 4. Details and evidence

### 4.1 Literature evidence, verification boundary and reading queue

**Requirement not yet met:** do not count the Graham book, repository specifications or a list of remembered titles as eight verified empirical papers/reports. In particular, no Vietnam sample period, net-return estimate, passing-ticker count or price-limit causal effect has been verified in this pass.

Two methodology citations were checked against the SHAP authors' versioned bibliography and README [S6]. This verifies citation identity and the documented attribution interface, not a full-paper review:

| ID | Paper / verified material | Market, period, method and finding boundary |
| --- | --- | --- |
| M01 | Lundberg & Lee (2017), *A Unified Approach to Interpreting Model Predictions*. Citation verified in authors' `shap_nips.bib`; README inspected. | General prediction explanation, not a financial-market sample; trading period not applicable. Authors document Shapley-based additive explanations of model output. No Vietnam return result or causal claim is inferred; full paper not retrieved. |
| M02 | Lundberg et al. (2020), *From local explanations to global understanding with explainable AI for trees*. Citation verified in authors' `tree_explainer.bib`; README inspected. | Tree-model explanation; not a VN trading experiment. README explicitly lists LightGBM support and explains baseline-to-output contributions. Full-paper empirical scope and assumptions were not independently reviewed; do not infer profitable signals from an attribution. |

The following is an **unverified research queue**, not completed annotated evidence. Titles/authors are discovery leads and must be checked against publisher/author records. Each entry has a distinct reason for inclusion; no numerical finding is attributed to an unread paper.

| ID | Bibliographic lead | What to extract before citing a finding | Relevance / transfer limit |
| --- | --- | --- | --- |
| L01 | Jegadeesh & Titman (1993), *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency* | US sample/exchanges and dates; exact formation/holding windows, skip convention, costs and survivorship treatment | Momentum benchmark; verify whether horizons are months rather than the requested 5–20 sessions |
| L02 | Jegadeesh (1990), *Evidence of Predictable Behavior of Security Returns* | US universe and dates; short-lag versus longer-lag dependence, estimation and microstructure controls | Reversal competing hypothesis; an observed return pattern is not a net executable strategy |
| L03 | George & Hwang (2004), *The 52-Week High and Momentum Investing* | US sample dates, distance definition, formation/holding windows, industry controls and costs | Motivates testing F16; does not establish that 252 sessions or a VN implementation works |
| L04 | Moskowitz & Grinblatt (1999), *Do Industries Explain Momentum?* | US sample/industry definitions, dates, weighting, individual versus industry effects and costs | Sector context; historical classifications and membership cannot be replaced with today's ICB snapshot |
| L05 | Rouwenhorst (1999), *Local Return Factors and Turnover in Emerging Stock Markets* | Exact emerging-market list and period; size/value/momentum/turnover methodology and implementability | Comparable-market evidence; explicitly check whether Vietnam is represented rather than assume it |
| L06 | Amihud (2002), *Illiquidity and stock returns: cross-section and time-series effects* | Sample period, return/dollar-volume definition, zero-volume exclusions, size controls and estimation | Candidate support for F11; a liquidity premium does not validate a VND 10bn cutoff |
| L07 | Kim & Rhee (1997), *Price Limit Performance: Evidence from the Tokyo Stock Exchange* | Tokyo sample dates, limit rules and event-control construction; reported spillover/discovery/trading effects | Price-limited-market mechanism lead; Japan is not evidence about current VN limits or fill probability |
| L08 | Lo, Mamaysky & Wang (2000), *Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation* | US sample period, pattern definitions, statistical testing and out-of-sample/net-cost scope | Technical pattern methodology; avoid turning conditional-distribution evidence into a profit claim |

**Mandatory Vietnam/comparable-market search still open:** search HOSE/HNX momentum, reversal, 52-week-high and industry momentum; Vietnam liquidity/size effects; Vietnam/China/Taiwan price-limit magnet effects, delayed discovery and spillovers. For every accepted paper record title/authors/year, DOI or stable primary URL, actual sample dates/venues, formation/holding periods, liquidity exclusions, taxes/fees, delistings, pre/post market-rule regimes, method, stated finding and transfer limits in 2–3 lines. Replace this queue with at least eight verified relevant annotations before marking R06's literature requirement complete. Do not pad the count with unrelated explanation papers.

### 4.2 Graham book: useful principles and boundaries

**Documented in user-supplied source [S5]:** the PDF has 641 pages. Its contents identify Graham's Fourth Revised Edition text, updated in 1971–1972 and originally published in 1973; new commentary is by Jason Zweig, ©2003. Main-text page offsets were checked; cite both printed and PDF pages rather than applying an offset to all front matter. The attachment is reference content, not task instructions.

| Author / location | Paraphrased principle | R06 implication (Inferred) |
| --- | --- | --- |
| Graham, Chapter 1, printed 18, 21–22; PDF 32, 35–36 | Investment requires analysis and attention to principal protection; speculation must not be mislabeled | Call the technical baseline an experimental trading/ranking rule, not a value investment or safety guarantee |
| Graham, Chapter 8, printed 190–192; PDF 204–206 | Forecasting is difficult; formulas fitted to past records can lose relevance as conditions and behavior change | Freeze parameters, record variants and test chronologically; this does not prove momentum either works or never works |
| Graham, Chapter 8, printed 204–206; PDF 218–220 | Market quotations and business value are distinct | A rising price/rank is not evidence of undervaluation |
| Graham, Chapter 14, printed 348–349; PDF 362–363 | Defensive selection considers enterprise/financial strength, earnings history and valuation | Do not transplant historical US dollar-size, industrial balance-sheet or valuation cutoffs into VN banks or add them as hidden R06 filters; R07 owns financial context |
| Graham, Chapter 20, printed 512–513, 517–520; PDF 526–527, 531–534 | Margin of safety depends on a supportable valuation cushion and assumptions; diversification complements it | ATR, a stop distance, momentum or a model score is not Graham's margin of safety; gaps/settlement/locks still matter |
| Zweig, commentary on Chapter 8, printed 219–220; PDF 233–234 | Costs, risk exposure, expectations and behavior are more controllable than market forecasts | Show costs and uncertainty; do not import US tax conventions into Vietnam |

The book is supplementary philosophy, not Vietnam technical-strategy evidence and not one of the required empirical papers. Preserve the user's ML scanner objective. It supplies no verified optimum for 20-session ranking, a ten-session exit, VND 10bn turnover or LightGBM. No long passages or PDF copy are added to the repository.

### 4.3 Existing data and eligibility contract

**Observed in repository documents/code [S2,S3]:** the pilot stores adjusted OHLC in thousand VND, volume with unverified matched/negotiated scope, no raw prices, no adjustment factors and no turnover value. Daily timestamps at 07:00 are session labels, not publication timestamps. Current VN100/ICB snapshots do not establish historical membership. The R02 report also records zero-volume filler bars and some inconsistent adjusted high/low values. These are R02 observations, not newly measured R06 results.

The isolated backfill approval in ADR-001 remains in effect. R06 consumes versioned local data and does not change the approved ingestion route. No API authentication, download of market history or inspection of local market-return rows is needed for this contract.

| Input | Strict R06 requirement | Current disposition |
| --- | --- | --- |
| Session calendar | Verified exchange sessions for the date/venue; do not infer holidays from missing bars | R03 settlement calendar alone is insufficient for every trading-calendar use |
| Universe/status | Point-in-time ordinary-equity universe for HOSE/HNX/UPCoM, dated listing/status and supported mechanics | Current snapshot only; historical strict universe unavailable |
| Signal prices | Internally coherent OHLC adjustment vintage available at decision time; positive prices, valid high/low bounds, complete required sessions | Provider-adjusted retrospective series cannot automatically be called point-in-time |
| Monetary units | Explicit conversion from thousand VND to VND where applicable; never mix units in costs or liquidity | Metadata available; this does not recover raw prices |
| Matched turnover | Verified session matched traded value in VND; median of the last 20 exchange sessions | Missing; **adjusted close × volume is not a valid substitute** |
| Actual raw price/bands | Verified raw close for the plan and dated next-session reference/limits/ticks | Missing; execution assessment remains unavailable |
| Volume | Documented scope and split/bonus-share normalization for cross-date comparisons | Unverified; affected features null |
| Sectors | Versioned ICB taxonomy/membership known at the relevant date; distinct theme tags | Current ICB level-2 snapshot is not historical evidence |

Let `U_t` be the declared, versioned ordinary-equity universe at session `t`. Account for every member as eligible, known ineligible, insufficient history, stale, unsupported, failed fetch or unknown eligibility. A known failure/unknown is not silently excluded from the denominator. Strict baseline release requires all members' eligibility to be determined; a partial view may be shown as `PARTIAL_RANKING`, but is not the strict baseline result.

For strict eligible set `E_t`, require supported venue/status, a fresh traded bar and **21 consecutive exchange sessions of valid traded closes** (no provider filler carried forward), benchmark availability, coherent price vintage and `median(matched_turnover[t-19:t]) >= 10_000_000_000 VND`. The consecutive-traded-close requirement is a conservative v1 research choice, not an exchange regulation. Genuine zero-turnover sessions count as zero in the liquidity window; an unknown turnover is null, not zero. A name failing the traded-close gate remains in coverage accounting.

The threshold's economic suitability and passing-ticker count are **Unknown**. Aggregate market value cannot determine a per-security median count. The nominal VND threshold is fixed for v1; do not optimize it by year after results. The handoff's 0.1% participation cap is a later sizing constraint: at exactly VND 10bn turnover it implies at most VND 10m order value before other constraints, not guaranteed fill capacity.

### 4.4 Feature set v1 — 19 candidate model inputs

All feature definitions are **Inferred**. `t` indexes verified exchange sessions, never compressed rows after deleting gaps. Brackets are inclusive. `C,H,L` refer to a consistent decision-time adjusted price vintage; `O_raw,C_raw,H_raw,L_raw` are raw prices; `B` is VNINDEX on the same sessions; `V` is consistently split-normalized, scope-verified volume; `M` is actual matched turnover in VND. `r_k=C_t/C_{t-k}-1`; `SMA_k=mean(C[t-k+1:t])`. No forward fill, backfill or zero imputation of missing observations. A missing/invalid required observation makes that feature null and records a reason. Feature warm-ups count required consecutive valid session observations, not listing age.

| ID | Feature / exact definition | Warm-up | Basis / units | Missingness / evidence link |
| --- | --- | --- | --- | --- |
| F01 | Return 5: `C_t/C_(t-5)-1` | 6 closes | Coherent adjusted; fraction | Null on gaps/nonpositive values; L01/L02 pending, handoff §8.1 |
| F02 | Return 20: `C_t/C_(t-20)-1` | 21 closes | Same; fraction | Baseline-critical; L01 pending |
| F03 | Return 60: `C_t/C_(t-60)-1` | 61 closes | Same; fraction | Optional for short histories; L01 pending |
| F04 | MA20 distance: `C_t/SMA20_t-1` | 20 closes | Same; fraction | Baseline-critical; positive denominator; handoff proposal, not verified alpha |
| F05 | MA50 distance: `C_t/SMA50_t-1` | 50 closes | Same; fraction | Null if warm-up incomplete; L08 pending |
| F06 | Realized volatility20: sample SD (`ddof=1`) of 20 log returns, times `sqrt(252)` | 21 closes | Adjusted; annualized fraction | 252 is a reporting convention, not asserted VN session count; constant series gives zero |
| F07 | NATR14: `mean(TR[t-13:t])/C_t`, `TR_d=max(H_d-L_d, abs(H_d-C_(d-1)), abs(L_d-C_(d-1)))` | 15 coherent OHLC/close sessions | Adjusted; fraction | **Simple mean**, not Wilder smoothing; null on inconsistent OHLC; handoff risk-description choice |
| F08 | Range20: `mean((H_d-L_d)/C_(d-1))`, d=t-19…t | 21 sessions | Adjusted; fraction | Requires coherent OHLC, not a separate liquidity estimate; descriptive choice |
| F09 | Relative volume: `V_t/median(V[t-20:t-1])-1` | 21 volume observations | Split-normalized volume; ratio | Null if volume scope/normalization unknown or prior median ≤0; raw/adjusted mix forbidden |
| F10 | Liquidity level: `ln(1 + median(M[t-19:t])/1e9)` | 20 turnover observations | Actual matched VND; dimensionless | Null if any M unknown; separate raw median retained for gate; L06 pending |
| F11 | Illiquidity20: `mean(abs(C_d/C_(d-1)-1)/(M_d/1e9))`, d=t-19…t | 21 closes + 20 M | Adjusted return per VND billion traded | Null if any required M≤0 or unknown; do not discard zero-volume days to create a flattering average; L06 pending |
| F12 | Index-relative20: `r20_stock - (B_t/B_(t-20)-1)` | 21 aligned stock/index closes | Same declared return convention; percentage-point difference as fraction | Null on benchmark gaps or incompatible return bases; index is price-return context, not a total-return claim |
| F13 | Sector-relative20: stock r20 minus equal-weight mean peer r20 | 21 aligned closes + dated membership | Adjusted stock/peer prices; fraction | Peer set fixed at t-20, excludes subject; ≥5 valid peers and ≥80% valid coverage of that fixed peer set, otherwise null. Current-only ICB cannot populate history; L04 pending |
| F14 | Prior-high breakout distance: `C_t/max(H[t-20:t-1])-1` | 21 OHLC sessions | Adjusted; fraction | Current high excluded from reference; null if inconsistent highs; L08 pending |
| F15 | Pullback from close high20: `C_t/max(C[t-19:t])-1` | 20 closes | Adjusted; fraction, ≤0 | Zero when today's close is window maximum; descriptive choice |
| F16 | Distance to 252-session high: `C_t/max(H[t-251:t])-1` | 252 OHLC sessions | Adjusted; fraction | Null before warm-up; 252 is operational proxy for 52 weeks; L03 pending |
| F17 | Market trend: `B_t/SMA50(B)_t-1` | 50 index closes | VNINDEX price basis; fraction | Shared per session; no automatic entry block; handoff §8.3 |
| F18 | Breadth20: `count(C_i,t > SMA20_i,t)/N_valid20` | 20 closes per assessable U_t member | Point-in-time declared universe; [0,1] | Null if N=0 or assessable coverage <80%; show numerator/denominator regardless. Not restricted to winners or trend-filtered E_t; handoff §8.3 |
| F19 | Limit-touch count5: sum of sessions with `H_raw=ceiling` OR `L_raw=floor`, each session counted once | 5 raw OHLC + verified band rows | Integer 0…5, compare exact tick-normalized units | Null if any bounds/raw data unknown; a touch is not a lock/fill; L07 and VN/China/Taiwan review pending |

The two 80% coverage cutoffs and minimum five peers are explicit unvalidated data-quality choices. Log the selected peer identities, denominator and dropped reasons. Sector peer-return averages are not an investable industry index. Require adjustment methodology compatible across all compared return series; report missing compatibility rather than calling F12/F13 alpha.

Missingness reasons, source hashes, coverage counts and status flags are **metadata**, not extra numeric model inputs hidden beyond the 19-feature budget. Baseline inputs do not require F03/F05/F16 warm-up, so a 252-session feature must not silently eliminate a stock from a 21-session baseline. R08 must specify missing-feature behavior for regression/LightGBM and fit imputation/scaling only in training folds. All features remain candidates until evaluated; literature associations alone do not validate them.

**Adjustment nuance:** uniform rescaling can leave some ratios unchanged; this does not prove every retrospective provider-adjusted feature is leak-free. Corporate-action conventions, nonuniform field adjustments, late corrections and volume changes require versioned evidence. Existing adjusted-only data may support a separately labeled retrospective feasibility experiment, not certification of strict point-in-time inputs or raw-price execution.

### 4.5 Frozen baseline specification

**Freeze declaration:** `R06-RS20-SMA20-v1` is fixed here before R06 return/rank/P&L evaluation. R02 has already collected data and documented capabilities; do not claim a universal “before anyone saw data” preregistration. No performance-driven threshold search was run. Literature review may motivate a later version before evaluation, but v1 must remain recoverable and every change logged.

```yaml
baseline_id: R06-RS20-SMA20-v1
research_only: true
freeze_scope: signal_selection_and_opening_price_research_proxy
executable_order_policy: unavailable_until_R09_defines_venue_event_and_deadline
signal_frequency: every_completed_exchange_session
universe: point_in_time_ordinary_equities_HOSE_HNX_UPCOM
benchmark: VNINDEX
core_price_sessions: 21
liquidity_window_sessions: 20
median_matched_turnover_min_vnd: 10000000000
minimum_eligible_names: 10
ranking_score: stock_return20_minus_benchmark_return20
percentile: 100_times_n_less_plus_half_n_equal_over_N
percentile_min_inclusive: 90
trend_condition: adjusted_close_strictly_above_SMA20
maximum_candidates_per_signal: 5
ties: score_descending_then_security_id_ascending
entry_session: next_exchange_session
entry_limit_cap_multiple_of_signal_raw_close: 1.02
entry_order_expiry: end_of_opening_execution_attempt
target_exit_sessions_after_entry: 10
exit_policy: time_exit_only
market_regime_trade_block: false
missing_eligibility_policy: strict_result_unavailable
```

**Ranking and candidates:** require the strict E_t contract in §4.3 and N≥10. Rank **before** the trend condition. For score s_i, percentile `p_i=100*(number(s_j<s_i)+0.5*number(s_j=s_i))/N`, with equality on stored deterministic values (no display rounding). Select p≥90 and C>SMA20, then retain at most five sorted by score descending and stable security ID ascending. All equal scores yield percentile 50; they do not produce top-decile candidates. The same benchmark return is subtracted from every name, so this ordering is mathematically identical to ranking their r20; it is not beta-adjusted or sector-neutral alpha. Report N and the tie convention.

**Signal time:** form a dated snapshot only after session t data are confirmed complete for the declared inputs. The 07:00 provider session label is not a data-ready time. If readiness arrives after the next session has opened, record a missed signal; never backdate a next-open order. Partial analyses may be displayed with their own coverage/status, not released as the strict baseline.

**Entry research convention:** e is the next verified exchange session after t. Before e's opening execution event, set a buy limit cap to `1.02 × raw_close_t`, clamp to the verified e ceiling and round **down** to a legal tick. Cancel if the resulting limit is below the legal floor, status is unsupported, input freshness is lost, or a reference-changing corporate action occurs between t and e and the plan is not supported. V1 conservatively cancels any such entry-day action rather than invent an adjustment. Never observe e's price and retrospectively alter the cap.

For an **opening-price research proxy**, a valid raw O_e at or below the pre-set cap and within the verified daily band satisfies the proxy price condition. Daily open may be the first trade much later than the intended opening attempt; without its timestamp it cannot establish that the condition was met before order expiry. This freeze covers signal selection and the daily opening-price proxy, not a complete executable order policy. Actual fillability belongs to R09, which must define each venue's opening event, exact submission/cancellation deadlines and treatment of missing or late first trades before execution simulation. Until then display `EXECUTION_UNAVAILABLE`; never infer a fill from O_e alone, including at a ceiling/auction queue. Under that future policy, an unfilled attempt expires; do not chase later in the session or defer entry to the next day under the same signal. Eligibility at t is retained in the audit even when the future attempt fails.

**Exit and horizon:** target the opening execution event ten exchange sessions after entry session e. If e=t+1, the target is t+11, not t+10. No reranking exit, profit target or intraday stop is added to this reference rule. Time-only exit is a baseline convention, not a risk guarantee; R10 still limits any future funded position. Before actual exit, verify lot sellability. A suspension, floor lock, missing price or absent liquidity leaves a pending exit and unresolved exposure; never replace it with a fictional fill. R09 owns executable-fill rules and liquidation uncertainty. A missing target observation is a missing label, not zero return or a dropped loser.

**Candidate studies versus portfolio:** daily signals define independent dated candidate cohorts for ranking/label research. If a cohort return is later reported, use an equal notional per selected name, with no assumed leverage; preserve unavailable components and do not renormalize away failed exits. Overlapping cohorts are not a funded portfolio. R09/R10 must define cash reservation, duplicate position suppression, aggregate exposures and quantity constraints before any portfolio P&L or personalized order size is claimed. No fictional account is created.

**Costs and labels:** R08 owns the target definition; preserve this ten-session timing in that contract or explicitly version a change. Gross adjusted-return labels and raw-price execution/cash-flow ledgers must use a consistent corporate-action convention. Deduct documented buy/sell fees, applicable sale/dividend tax, custody/financing where relevant, and the R09 slippage scenario once their versions are verified. R03 records that tax and some rule evidence remain open; this baseline therefore cannot currently certify net returns. Do not silently assume zero costs or use both the TCBS total tariff and an already-included exchange fee.

**Failure states:** fewer than ten eligible names → `INSUFFICIENT_CROSS_SECTION`; determined eligibility with no selected names → `NO_CANDIDATES`; unresolved required data → `BASELINE_UNAVAILABLE`; unsupported venue/status → visible per-security reason; partial scan → `PARTIAL_RANKING`. These are separate from model state: with no validated trained artifact, display `ML_UNAVAILABLE` and identify the deterministic baseline as research-only.

### 4.6 Price limits, liquidity and risk implications

The literature review must distinguish magnet effects, post-hit price discovery and spillovers using each study's actual rule regime and identification method. None of these empirical mechanisms has been established for this project in this pass.

**Inferred operational consequences:** record whether a verified band was touched, whether raw observations are unavailable, and whether the signal precedes settlement release. Daily OHLCV does not establish queue position, opposing depth, the order of high/low, or whether a stop was reachable after shares became sellable. A floor close is not proof of an all-day lock, and positive daily volume is not proof our sale filled. Do not label missing foreign/proprietary flows as zero or manufacture a “smart money” score.

Size and liquidity are different: no validated market-cap field exists in this contract, and high volume is not proof of a large capitalization. The turnover gate is an implementability hypothesis, not a proven illiquidity premium or economic-optimal cutoff. Limit touches, stale bars and missed outcomes must remain in diagnostic counts and the evaluation cohort rather than selectively disappearing.

### 4.7 Market/sector context panel

| Panel field | Definition / display rule | Failure / interpretation |
| --- | --- | --- |
| Market trend | VNINDEX level, SMA50, F17, date and source | Above/below/equal/unknown, not a buy/sell command; requires 50 aligned observations |
| Covered breadth | Number above SMA20 / number with valid20, plus valid20 / declared U_t | Label the actual universe and date; under 80% coverage show `LOW_COVERAGE`, not a whole-market regime conclusion |
| Regime description | Index above SMA50 and breadth >50% → stronger observations; both below → weaker; opposite signs → mixed; equality → neutral; missing/low coverage → unknown | 50% is an unvalidated descriptive split; never blocks v1 candidates |
| Sector relative return | Equal-weight 20-session return of fixed t-20 sector members with ≥5 valid members and ≥80% coverage, minus VNINDEX r20 | Show classified/valid/total counts and taxonomy vintage; not an investable index or historical signal from today's mapping |
| Theme tags | Versioned many-to-many tags such as Steel or Public Investment with rationale and known/effective dates | Themes can overlap sectors and each other; never sum theme percentages as disjoint market breadth |
| Execution/data context | Supported venue/status, raw/band/turnover availability, stale or no-trade bars | Visible reasons; no inference that technical strength makes the trade executable |

Store one primary documented ICB sector per security per effective interval; do not assume ICB level-2 uniquely separates Banks, Securities, Real Estate and Steel. If available taxonomy depth cannot express a requested group, show it as unavailable or as an explicitly curated classification. Public Investment is a theme requiring documented tagging, not an automatic sector label. No retrospective theme assignment based on later news.

F13 excludes the subject from its peer set; panel sector returns include all fixed-set members meeting the published coverage rule. Explain that difference. Count distinct securities for universe breadth; a stock tagged in multiple themes is counted once overall. Missing sector/thematic data does not invalidate a baseline that does not use those inputs.

### 4.8 Deterministic explanations and model attribution

Templates use stored snapshot values and reason codes, not generated market narratives:

- “20-session return {r20}; index-relative difference {relative20}; midrank percentile {p} among {N} eligible covered securities as of {date}. This is a rank, not a probability of profit.”
- “Close is {distance}% above/below its 20-session average; the v1 trend condition {passed/failed}. Eligibility and execution checks are shown separately.”
- “Breadth is {above}/{valid} ({breadth}%) across {universe_name}; usable coverage is {valid}/{declared}. {partial/low-coverage label}.”
- “Liquidity eligibility unavailable: verified matched-turnover data are missing. Adjusted close × volume was not substituted.”
- “No candidates satisfy the frozen baseline today.” / “Baseline unavailable because required inputs could not be verified.” Use the correct state, not the same empty-list message for both.
- “Technical observation; not an intrinsic valuation or a demonstrated margin of safety.”

**Documented [S6]:** SHAP explains prediction outputs, and the authors' documentation describes base-value-to-output additive contributions and LightGBM support. **Inferred product contract:** if used later, display model/version, raw output units, expected/base value, selected background data, explainer settings and feature contributions. Check `base + sum(contributions) ≈ model output` in the chosen output space. A regression score is not a calibrated probability. Correlated return/MA/sector features can share attribution differently under different reference assumptions; neither signs nor importance establish causation. Keep deterministic fact explanations available when no model is trained; never fabricate SHAP values for the rule baseline.

### 4.9 Synthetic validation plan and results

Checks use invented arrays only; they exercise definitions rather than claiming a trading result. The scratch validation script is outside the repository. No backfill, real-price query or trained model was run.

**Observed, 2026-11-06:** `python3 /tmp/r06-research/validate_r06.py` passed **14 checks** (12 synthetic arithmetic/selection checks and two document checks). Local Markdown links resolve, the F01–F19 feature list is complete, and there is no trailing whitespace. Pandoc successfully rendered this document to `/tmp/r06-research/R06_findings.html`. These scratch checks validate examples and document consistency; they are not tests of a feature engine or execution simulator, neither of which exists here.

| Check | Expected behavior |
| --- | --- |
| Percentile and ties | Scores 1…10 give best percentile 95; all-equal scores give 50 and no top-decile candidate; equal candidates sort by stable ID |
| Benchmark invariance | Subtracting one common benchmark return preserves cross-sectional order |
| One strict trend filter | Close equal to SMA20 fails `>`; no market-regime predicate is introduced |
| Baseline warm-up | 21 closes required for r20, 20 for SMA20; lack of 252 observations does not become an extra baseline filter |
| Temporal high reference | F14 uses only t-20…t-1 highs; changing today's high alone does not change its denominator |
| Volume/missingness | Missing median/zero prior-volume denominator gives null, not infinity or a fabricated zero signal |
| Tick cap | A hypothetical cap 102 with tick 5 rounds down to 100, never 105 |
| Horizon | Entry index t+1; ten sessions later is t+11 |
| Breadth/tags | All-equal-to-MA names are not above; zero denominator gives null; overlapping theme labels do not duplicate securities |
| Liquidity participation arithmetic | VND 10bn × 0.001 = VND 10m, before other constraints; not a fill guarantee |
| ATR convention | Fourteen true ranges of 5 and close 100 give simple-mean NATR 0.05 |
| Limit-touch counting | A session touching both ceiling and floor counts once, not twice |

## 5. Impact on the handoff and implementation readiness

| Check / dependency | Contract outcome | Readiness |
| --- | --- | --- |
| A20 | Baseline and model states separate; no trained artifact means `ML_UNAVAILABLE`; no rank-to-probability relabeling | Specification defined; application not implemented |
| A25 | Genuine no-candidate output distinguished from unavailable/partial analysis; no forced pick | Synthetic selection cases checked; application not implemented |
| A28 | Venue/status support and universe coverage explicit; unsupported does not mean silently omitted | Specification defined; authoritative R03/data inputs still needed |
| P2 features | 19 formulas, units, warm-ups, adjustment and missingness rules | Ready for review and later synthetic implementation, not certified historical features |
| P3 baseline | Versioned rank/trend/candidate/timing contract, parameter choices visible | Frozen before R06 outcome evaluation; real-data net evaluation blocked |
| Required ≥8-paper bibliography | Verification queue and extraction fields established | **Incomplete**; Vietnam/comparable empirical evidence not verified |

Proposed changes to the handoff only: clarify the 20-session percentile/ties and ten-session entry-to-exit offset; distinguish raw execution from adjustment-vintage features; define coverage denominators; preserve Graham's margin-of-safety meaning; and make `NO_CANDIDATES` versus data-unavailable visible. No handoff, ADR, backfill source or existing test was modified.

Future P2 implementation should add a pure feature function over a versioned local-data interface and synthetic tests for gaps, corporate-action bases, ties and warm-up. P3 should consume its immutable snapshots; R08 owns fold/label/probability methodology, R09 fills and costs/slippage, R10 funded sizing/exposure. Do not change the isolated ingestion route merely to make missing downstream fields appear available.

## 6. Risks and traps found

- Existing historical adjusted-only bars and current-only membership cannot prove strict point-in-time results.
- A 20-session stock-minus-index score is not beta-neutral alpha; subtracting a common benchmark does not change rank.
- Adding breakout, valuation, market regime or ATR-stop conditions to the baseline would change the frozen hypothesis.
- Genuine zero-trade rows and missing data require different handling; deleting either can distort rolling windows and eligibility.
- A feature's long warm-up must not silently change the baseline universe; model eligibility and baseline eligibility are separate.
- A book's investment philosophy, an unread paper title, or an in-sample paper return is not empirical evidence for this strategy.
- Price-limit touches, next-open proxies, overlapping research cohorts and funded portfolio trades answer different questions.
- Unavailable tax/fees/raw bands must not become zero-cost or guaranteed-execution assumptions.

## 7. Open questions and continuation

**Academic-source blocker (Observed):** a proxy request to `api.crossref.org` returned HTTP 403 at CONNECT on 2026-11-06. No general web-search tool is available in this session. The active environment allowlist still contains the earlier Vietnamese-rule domains, not academic sources. The following additions were saved in the environment draft, preserving all previous domains: `api.crossref.org`, `ideas.repec.org`, `econpapers.repec.org`, `doi.org`, `arxiv.org`, `export.arxiv.org`, `onlinelibrary.wiley.com`, `academic.oup.com`, `www.sciencedirect.com`, `link.springer.com`, `www.emerald.com`, `jabes.ueh.edu.vn`, `www.nber.org`, `www.imf.org`, `documents1.worldbank.org`. Saving did not apply or publish them. Review/save the draft and publish through environment settings when required, then retry affected research. No secret is needed.

**Remaining public-source work:** complete ≥8 relevant annotations, with direct Vietnam and comparable price-limit evidence; verify study horizons/costs/survivorship; resolve whether the evidence supports or challenges the chosen horizon; seek a dated public count/distribution for the exact matched-turnover screen or retain it as unknown. R06 cannot be labeled fully researched while these requirements are open.

**Remaining data work:** R01/R02 must establish raw/adjusted vintages, matched turnover/volume, point-in-time universe/sector coverage and the benchmark return convention. The current VN100 list can support a clearly labeled present-snapshot exploratory study only; do not silently treat it as a historical VN100 universe. R03 must supply verified exchange-session and execution rules. Account-specific fees/holdings and user risk preferences are later inputs, not prerequisites for writing the research contract.

**No new application code or real-data backtest is included.** The unavailable repository-prescribed `~/.venv/bin/vnstock onboard` executable was reported; no substitute installation, login or API-key request was made. Existing ingestion functionality remains intact.

## 8. Sources and provenance

| ID | Source | Version / scope inspected |
| --- | --- | --- |
| S1 | [Product handoff](../../requirement/AI_Stock_Scanner_Agent_Handoff.md) | v1.0, 2026-11-05; §§8.1/8.3/8.4/9.1–9.5/11/18.2 read on 2026-11-06; internal requirements, not empirical evidence |
| S2 | [Data capabilities](../../docs/data_capabilities.md) and [R02 findings](R02_findings.md) | 2026-11-06 pilot report; inspected at repository HEAD `edca46d2469f656de10d60f51be01410fca8b74c`; observations attributed to R02 |
| S3 | [Backfill implementation](../../scripts/backfill/backfill.py), [tests](../../tests/test_backfill.py), [ADR-001](../../docs/adr/ADR-001-vnstock-backfill.md) | Read schema and fake-source testing structure; no market database rows or real API calls inspected |
| S4 | [R03 findings](R03_findings.md) | Current committed report; settlement/calendar/fee findings and explicit unresolved execution/tax rules |
| S5 | User attachment: *The Intelligent Investor — Revised Edition*, Benjamin Graham, with commentary by Jason Zweig | 641-page PDF; Graham ©1973 / Zweig ©2003; eISBN 0-06-058328-2. Inspected 2026-11-06. SHA-256 `2fca98ab2511938ca6f9b4e024e7bd6e456c9d41c46ac16c99da38912f876f33`; page citations in §4.2. Not copied into Git. |
| S6 | [SHAP authors' README](https://github.com/shap/shap/blob/fc3e290e97ce12f76d1175d24c6e3023b4ca7d69/README.md), [2017 bibliography](https://github.com/shap/shap/blob/fc3e290e97ce12f76d1175d24c6e3023b4ca7d69/docs/references/shap_nips.bib), [TreeExplainer bibliography](https://github.com/shap/shap/blob/fc3e290e97ce12f76d1175d24c6e3023b4ca7d69/docs/references/tree_explainer.bib) | Retrieved/read 2026-11-06; README pinned-content equality checked. Author documentation/citation records, not a review of all cited papers. |

**Decision retained:** RS20 plus one SMA20 trend condition is a frozen, unvalidated research baseline. Its definitions and Graham boundaries are reviewable now; empirical Vietnam support, the required bibliography and strict data/execution readiness remain open and must not be presented as completed validation.
