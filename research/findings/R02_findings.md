# R02 Findings — Free Complementary Data Sources (Vnstock and Alternatives)

**Researcher:** research agent R02 (Claude) · **Date:** 2026-11-05 (all sources accessed this date) · **Effort spent:** ~3 agent-hours of live research (budget ~8 h; exchange-portal depth and every authenticated check were not attempted, see §7) · **Spec:** [specs/R02_free_data_sources.md](../specs/R02_free_data_sources.md)

Evidence labels: **Documented** = a primary source says so; **Observed** = seen directly in a public response or in public library source I read; **Inferred** = my reasoning; **Unknown** = could not be established from public sources. Web-page figures were extracted by a summarising fetch tool, so every number that drives a decision is marked for re-verification with `vnstock policy` / `vnstock usage` once a key exists (see §7).

---

## 1. Recommendation (read this first)

- **Recommend (primary combination, "P1"):**
  1. **Prices, indices, current trading data:** the documented **TCBS OpenAPI** (`bars-long-term`, R01 owns the verdict) behind an adapter.
  2. **Universe, delistings, exchange transfers, ticker changes, corporate actions:** a **versioned, dated, curated reference file** built from HOSE/HNX/VSDC notices, extended forward by a **daily snapshot** of today's listing (point-in-time from day 1 of operation).
  3. **Financial statements:** show **current** statements only (company disclosures / optional Vnstock Community level-1 data) and **exclude all financial fields from retrospective ML training in Phase 1** (§8.2 already allows this).
  4. **Vnstock Community v5 = OPTIONAL, isolated, non-blocking** (listing/ICB snapshot, events calendar, level-1 statements, cross-check series). It routes through **undocumented broker front-end endpoints** (VCI, KBS), so under the project's no-undocumented-dependency gate it **cannot be the sole source of anything the model trains or trades on**.
- **Runner-up / fallback ("P2"):** **SSI FastConnect Data** (documented REST: `data/ohlc`, `data/corporateActions`, indices, securities lists; daily history "since the security started trading"; currently fee-free; key + secret auth, no OTP mentioned for data). **Choose it instead if** TCBS cannot run unattended or has too little history (R01), **and** the user is willing to open an SSI trading account (SSI says FastConnect is "chỉ cấp cho khách hàng đã có tài khoản giao dịch"). DNSE is the same pattern (account needed, fee unverified) and ranks third.
- **Confidence:** **Medium-low on the history source** (TCBS depth, units, adjustment, quota are all unstated in its docs, and R01 has not reported); **High** on the negative findings (no free documented source gives point-in-time universe, delisted prices, restatement versions or disclosure dates; Vnstock Community cannot supply them either).
- **Would flip the decision:**
  - R01 shows TCBS history is deep (≥ 8 years daily, all three exchanges) and a token flow works unattended → P1 stands as written.
  - R01 shows TCBS cannot run unattended or history is short → fallback P2 (SSI) or, if the user refuses another account and accepts the risk, **Vnstock Community promoted to primary history source with an explicit G1 sign-off** (still labelled undocumented-upstream).
  - A `vnstock usage` reading showing Community daily quota < ~1,700 calls/day (Guest is 300/day, §4.6) → Vnstock cannot even be the optional full-universe cross-check; fall back to a sampled cross-check.
  - Evidence that delisted tickers' price history is retrievable from TCBS or SSI → survivorship limitation can be narrowed (currently assumed not recoverable).
- **Needs user decision / gate:**
  - **G1: Triggered (conditionally, pending R01).** No free, documented, no-new-account source covers history **and** reference data **and** corporate actions. The user must choose: (a) TCBS if R01 passes; (b) open an SSI account for FastConnect Data; or (c) accept Vnstock's undocumented upstreams as the history source.
  - **G3: Not triggered by P1 or P2** (TCBS free registration per handoff §4.1; SSI states "chưa thu phí" which is *not* a promise of permanent zero cost). **Contingent trigger:** if Vnstock Community quota proves inadequate and the user wants Vnstock to stay in the loop, the only upgrade is a paid Bronze/Silver/Golden/Diamond plan (price not retrievable, §7), which would break the VND 0 target. Do not take it.

**Headline warnings for the Tech Lead** (details in §4 and §6):
1. Vnstock v5 changed materially in the last 8 weeks (see Q1): proprietary licence, release-expiry (365 days), a remote policy server that can disable the library, device registration, PyPI project **quarantined on 2026-09-24**, v5 distributed pre-compiled from a vendor index whose source I could not inspect.
2. Legacy vnstock ≤ 4.0.8 wrote text downloaded from vnstocks.com into the **global rule files of Claude Code, Codex and Antigravity on every `import`** (CHANGELOG 4.0.9, Observed). This project is built with coding agents; anyone who ever imported an old version should inspect their agent rule files. Never let a data library run in a context where it can write agent configuration.
3. Vnstock equity OHLCV is **adjusted only, in thousand VND, rounded to 2 decimals by default**. A raw series cannot be requested. That conflicts with handoff §7.2 ("preserve raw and adjusted separately") unless the project captures raw closes forward in time.

---

## 2. Answers to the spec's research questions

| # | Question (short) | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Q1 | Vnstock today: version, licence, tiers, quotas, devices, depth, routes | **v5.0.x** (docs header 5.0.1; release log lists 5.0.3 on 2026-10-15). **Proprietary licence** (not OSI): free for personal/study/research; `license-2026.09` in force, **`license-2026.11` published 2026-10-24, effective 2026-11-30**, needs explicit electronic acceptance. Tiers: **Guest** (no key) 10/100/300/1,000 calls per min/hour/day/month; **Community** (free key) quota "per account, see `vnstock usage`", **no number published**; **paid** Bronze/Silver/Golden/Diamond (prices not retrieved). Community: **1 device**, daily history **2,920 days (~8 years)**, 1-min 180 d, 5m–1H 365 d, daily row cap 10,000, financials **8 periods, level-1 line items only**. Each release valid **365 days**, then data calls fail; a remote policy (refreshed ~10 min) gates all calls. Upstreams: **VCI, KBS** (Community), plus vnd/mas/asean/cafef (paid only), builtin tables. TCBS and MSN **not in v5** (TCBS source removed in 3.5.0, 2026-03-07). | Documented (vendor docs); upstream URLs Observed in legacy 4.0.9 source | [S1][S2][S4][S5][S6][S8][S9][S10][S11] |
| Q1b | Are the underlying sources documented and permitted? | **No.** VCI = `trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart`, `iq.vietcap.com.vn/api/iq-insight-service/...`, GraphQL; KBS = `kbbuddywts.kbsec.com.vn/iis-server/...` and `/sas/...`. These are the brokers' web/app back-ends; no developer documentation or licence for third-party use was found. Vnstock's own page "does not say whether any source is an official API"; its licence says the user must check each source's terms and that it grants **no** rights to third-party data. Classification: **UNDOCUMENTED upstream (high break/permission risk)**. | Observed (source) + Documented (licence text) | [S4][S10][S11] |
| Q2 | Units and adjustment | Equity/ETF/warrant OHLCV: **thousand VND** (57.9 = 57,900 VND); indices/futures: points; `quote()`/`order_book()`: **full VND**; financial statements: **full VND** (`unit` column). OHLCV is **adjusted for corporate actions**; VCI and KBS adjust **differently ("a few đồng")**; **no raw-price option documented**; `trade_history()` exposes `*_adjusted` next to unadjusted columns (not verified to be a raw daily OHLC). Legacy source divides raw full-VND by 1,000 for stocks/ETFs and rounds to `floating=2` (= 10 VND resolution) unless `floating=None`. Adjustment method is **not documented**. TCBS and SSI docs state neither unit nor adjustment for their bars. | Documented (v5 docs); Observed (4.0.9 code) | [S2][S4][S11][S16][S22] |
| Q3 | Universe and survivorship | **Not recoverable from any free structured source found.** Vnstock `equity.list()` = current symbols only (about 1,754 codes on the doc's test day; fields `symbol`, `org_name`; no status/listing-date/delisting field). `index.members()`, `list_by_group()` = current constituents; sources disagree (HOSE group: 430 on VCI vs 406 on KBS). No ticker-change or exchange-transfer history. Delisting/transfer events are public as exchange announcements and press (e.g., 25 UPCoM firms delisted in one day in 2022; FLC-group moves), but no bulk machine-readable history was found on hsx.vn/hnx.vn/vsd.vn (HOSE site is a JS single-page app; HNX/VSD pages refused or failed in this session). Best approach: curated event file + forward daily snapshot (§4.3). | Documented (Vnstock docs) / Unknown (exchange bulk lists) | [S7][S24][S27] |
| Q4 | Corporate actions | **Best free structured source = Vnstock `events.calendar()` (VCI; Community route)**: `ex_right_date`, `record_date`, `payout_date`, `issue_date`, `value` (VND/share), `ratio`, `event_type` (DIV, ISS, AIS, DDIND, DDINS, EGME, AGME); one call can span a date range (limit 20,000). Undocumented upstream. **Documented alternative: SSI `GET /api/v3/data/corporateActions`** (`exrightDate`, `recordDate`, `issueDate`, `ratio`, `eventTitle`; **max 5-day window per call**; no event-type field; history depth not stated; account required). TCBS: no corporate-action endpoint found in its public docs. Coverage quality, split vs bonus ratio semantics, and completeness: **Unknown, needs a sample audit with a key**. | Documented | [S7][S17] |
| Q5 | Financial statements | **Line items (not only ratios): yes, but reduced.** Vnstock Community: income statement, balance sheet, cash flow, **level-1 items only**, **8 periods**, sources VCI/KBS, full VND. **No publication/report-date column** (docs say so explicitly). **Restatement/version history: not documented, assume none.** Consolidated vs parent basis: **not stated** by the functions. Ratios, notes, `filing()` (disclosure list with links) are Extended/PAID. Banks detected automatically. **No free source found with publication dates or restatement versions.** Conservative proxy: availability date = statutory deadline after period end (R07 owns the rule; §4.5). | Documented | [S3][S1] |
| Q6 | Alternatives | **SSI FastConnect Data:** documented, "chưa thu phí" (no fee for now), **needs SSI trading account**, one-year validity, per-key rate limits not published, 90-day inactivity suspension, SSI may stop service anytime without notice, data usable only for the customer's own securities trading and not shareable (even processed). **DNSE OpenAPI/LightSpeed:** documented; account at DNSE apparently required; fee and rate limits **Unknown**; OHLC/EOD/intraday/index baskets advertised. **Exchanges (HOSE/HNX/VSDC), SSC disclosure system:** authoritative human-readable pages; **no documented free bulk API found**; HOSE sells market-data products (paid). **Other OSS** (vietfin Apache-2.0, vnquant stale, pyvietstock, vntickers, community forks): all wrap undocumented broker/portal endpoints. **Paid:** FiinPro, Vietstock DataFeed, FiinGroup API, vnstock paid tiers. | Documented (SSI, DNSE) / Inferred (exchanges, OSS) | [S14]–[S21][S24]–[S28] |
| Q7 | Indices and sectors | VN-Index/HNX-Index/UPCoM-Index/VN30/HNX30 **daily OHLC**: Vnstock `market.index.ohlcv` (KBS default; VCI for intraday), TCBS bars `type=index` (documented), SSI index endpoints (documented, account). **Historical VN30 membership: not available free** (current constituents only). **Sector:** ICB via VCI (`list_by_industry`: levels 1–4, 177 industries) and a KBS/CafeF classification that is Extended-gated; **no effective dates** anywhere. Handoff §7.1 requires effective dates, so the classification must be snapshotted forward by us. | Documented | [S2][S7][S22] |
| Q8 | Cross-checking | Method and tolerances in §4.7: stratified 20 tickers x 3 dates, unit normalised first, raw-to-raw before adjusted-to-adjusted, tolerance in ticks. | Inferred (design) | n/a |

---

## 3. Options compared

| Option | Free-first gate | Fit to handoff | Effort / complexity | Key risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| **P1: TCBS bars + curated reference files + forward snapshots; Vnstock optional** | Pass (TCBS free registration per handoff §4.1; Vnstock Community free) | Matches §2 (TCBS first), §4.2 (curated fallbacks), §8.2 (financial features conditional) | Medium: curation of delist/transfer/corporate-action events is manual work | TCBS depth/units/adjustment unknown; iOTP every 8 h (R01) | **Recommended** |
| P2: SSI FastConnect Data (+ TCBS for holdings) | Pass today ("chưa thu phí"), not a permanence promise | Documented API incl. corporate actions; but needs a second broker account (§2 says do not *require* one) | Low-medium | Account/eligibility unverified; ToS lets SSI end service unannounced; per-key quota unknown | **Fallback** |
| P3: Vnstock Community as primary history + events + financials | Free for personal use; **fails the "no undocumented dependency" gate** | Fits §4.1/§4.2 wording "permitted Vnstock data if needed" | Lowest coding effort | Undocumented VCI/KBS upstreams; release expiry (365 d) and remote kill switch; PyPI quarantine; unpublished quota; 1 device; adjusted-only; cannot inspect v5 binary | Not primary. Allowed only as isolated optional adapter, or primary only with explicit G1 sign-off |
| P4: DNSE OpenAPI | Unknown (fee, rate limits unstated) | Needs DNSE account | Medium | Same account issue as SSI, less documented | Third choice, revisit only if SSI is refused |
| P5: Exchange sites / SSC / company IR only | Free | Authoritative, but manual | High | No bulk API found; scraping SPA portals is out of bounds | Use for reference data and spot checks only |
| P6: Paid feeds (FiinPro, Vietstock DataFeed, Vnstock paid) | **PAID/OPTIONAL** | Would give financials with dates, restatements | n/a | Breaks VND 0 | Out of scope; list only |

---

## 4. Details and evidence

### 4.1 Q1: Vnstock today (access date 2026-11-05)

**Version and distribution.** Docs show `vnstock v5.0.1` ([S1], [S4], [S9]); the release log lists `5.0.3` (2026-10-15, replacing withdrawn 5.0.2) ([S8]). Generation 5 merges the old community `vnstock` 4.x and the paid `vnstock_data` 3.x into one package with a Rust core ([S9]). The GitHub repo is the **legacy 4.x** code (latest changelog entry 4.0.9, 2026-09-26; commit `71b853f` 2026-10-13) and says gen-5 ships pre-compiled from `https://vnstocks.com/api/packages` ([S11]). **PyPI:** `https://pypi.org/simple/vnstock/` returns `pypi:project-status: quarantined` and no files; the project page says PyPI admins quarantined it on 2026-09-24, "cannot be installed or modified until a security review is complete", latest listed 4.0.8; `pip download vnstock` failed with "no versions" on my machine ([S12], Observed). I could not find a public statement of the reason. I did not register or download from the vendor index, so **v5 source is uninspected** (Unknown).

**Licence.** `license-2026.09` (repo `LICENSE.md`, summary; web text governs): not OSI; free for "cá nhân, học tập và nghiên cứu"; scope is measured by users, registered devices and tier quota, not purpose; redistribution and "products whose main value is giving third parties market-data access" need written agreement; reverse engineering, fake device identity and evading rate limits are prohibited; the licence "không cấp quyền sử dụng dữ liệu của nguồn bên thứ ba" ([S11]). **`license-2026.11`**, published 2026-10-24, effective **2026-11-30**, says "Downloading, installing, or continuing to use the software does not count as acceptance of a new version" and requires explicit electronic confirmation; Community remains "free for personal, study and research"; it **does not explicitly address scheduled jobs** and bans "abnormal query volume" ([S10]). Our use (single user, local, personal analysis) fits the Community scope (Inferred). **Action:** the user must read and accept the 2026.11 text on 2026-11-30 or the Community path may lapse (Inferred from the acceptance clause).

**Tiers and quotas** ([S1], v5.0.1 page, policy snapshot 2026-10-18):

| Item | Guest | Community (free key) | Paid |
| --- | --- | --- | --- |
| Calls min/hour/day/month | 10 / 100 / 300 / 1,000 | "account quota, see `vnstock usage`" (**no number published**) | per tier (not published) |
| Devices | not stated | **1** | differs by tier |
| 1-minute history | 30 d | 180 d | unlimited |
| 5m–1H history | 90 d | 365 d | unlimited |
| Daily/weekly/monthly | 365 d | **2,920 d (~8 y)** | unlimited |
| Daily rows per call | 1,000 (market page says 5,000; inconsistent) | 10,000 | unlimited |
| Financial periods | none (docs elsewhere say 4) | **8, level-1 only** | all, full tree |
| Pacing | 1 s between queries | 1 s | 0.1 s |
| Routes | 8 routes, 3 sources | **42 routes, 6 sources** (14 market, 13 reference, 10 company, 3 statements, 2 retail; gold retired) | all |

The quota is **account-wide and shared across 4.x/5.x libraries and devices**, hourly/daily/monthly in Vietnam time ([S13]). A single call may send at most 50 queries; whether one *call* equals one quota unit, or one *query* does, is **not documented** (Unknown). `VNSTOCK_AUTH_*_LIMIT` errors are raised on exhaustion; tier caps truncate results (with `df.attrs["tier_cap_*"]`) rather than fail ([S5]). Foreign/proprietary flow functions are **paid only** (`VNSTOCK_TIER_ROUTE`) ([S2]).

**Operational constraints that matter for an unattended scanner** ([S1], [S5], [S6]):
- **Release expiry:** each build is usable 365 days from approval; warnings start at 30 days; after expiry every data call raises `VNSTOCK_RELEASE_EXPIRED`. A pinned, locked dependency (handoff §14) therefore **stops working by design**.
- **Remote policy:** no data call runs if the policy cannot be loaded (`VNSTOCK_POLICY_UNAVAILABLE`); sources, hosts and releases can be **disabled remotely and cannot be overridden locally** (`VNSTOCK_*_DISABLED`).
- **Login/device:** `vnstock register` (key typed at a hidden prompt, or `VNSTOCK_API_KEY` env var / stdin), saves an encrypted key locally and registers the device. Headless use is supported through the env var. CI use requires a key. One device on Community.
- **Telemetry:** the vendor services process account, device, quota and "đo lường kỹ thuật" data ([S11]); `vnstock_quant` telemetry is opt-in/out ([S8]).
- **No automatic source fallback; no caching** documented ([S4], [S5]); 429/403/anti-bot challenges are not retried.

**Upstream sources by tier** ([S2], [S4]): Community may use `vci`, `kbs`, `builtin`, `dukascopy`, `binance`, `vcb`. `vnd`, `mas`, `asean`, `cafef` raise `VNSTOCK_TIER_SOURCE`. Not in v5: `msn`, `tcbs`, `fxsb`, `fmp`, `dnse`. Source defaults can change between versions "when a source stops serving"; read `df.attrs["source"]`.

**Undocumented-upstream classification (hard constraint).** Constants in the 4.0.9 code (Observed): VCI `https://trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart` (POST `{"timeFrame","symbols","to","countBack"}`), `https://iq.vietcap.com.vn/api/iq-insight-service/v1/{events,company,market-indices,sectors/icb-codes}`, `.../data-mt/graphql`; KBS `https://kbbuddywts.kbsec.com.vn/iis-server/investment/...` and `/sas/kbsv-stock-data-store/...`. These are the same endpoints the brokers' own web apps use. **Risk:** they can change schema, add anti-bot or block IPs without notice (Vnstock itself documents `VNSTOCK_SOURCE_BLOCKED/CHALLENGE`), and nothing grants third-party licence. I did **not** call these endpoints myself.

**Security finding (Observed).** vnstock CHANGELOG 4.0.9 (2026-09-26): earlier versions "wrote an instruction block into AI assistants' rules files on every `import vnstock`: the project's `AGENTS.md` and, by default, the global files of Claude Code, Codex and Antigravity... downloaded from vnstocks.com at write time" ([S11]). 4.0.9 made this opt-in (`enable_agent()` / `setup_agent()`, `vnai >= 2.6.2`). Whether v5 retains the opt-in hooks is Unknown. Mitigation for this project: install any Vnstock build only in an isolated venv/container, forbid it write access to the home directory's agent configuration, and have the user inspect `~/.claude/CLAUDE.md` and project `AGENTS.md` if an older version was ever imported.

### 4.2 Q2: units and adjustment

- **Vnstock equity OHLCV:** thousand VND, adjusted, VCI vs KBS differ by "a few đồng" for old candles; "older candles can show two decimal places"; no raw option ([S2], [S4]). `floating=None` keeps source precision ([S2]).
- **Observed (4.0.9 code):** VCI helper uses `scale_map = {"VCI": 1000, "MAS": 1000}` (price ÷ 1000); KBS OHLC divides stock/ETF prices by 1,000 and leaves indices and derivatives in points; default `floating=2` rounds to 0.01 thousand VND = **10 VND**, coarser than the 1-VND resolution an adjusted price can carry. In the trades transform helper `volume.fillna(0)` turns a missing volume into zero, exactly the missing-vs-zero conflation handoff §7.2 forbids (legacy helper; v5 behaviour Unknown).
- **Interval timestamp convention:** VCI returns epoch seconds localised by the library; whether the daily bar's timestamp marks session open or end of data availability is Unknown. Per §7.2 treat the bar as available only after the session close plus a safety margin.
- **TCBS** `bars-long-term`: units, adjustment, max `countBack` and history depth are **not stated** in the docs; the example `34550.00` suggests full VND (Inferred). **SSI** `data/ohlc`: units and adjustment **not stated**; fields are strings ([S16]). Both must be validated against a known value (R01 for TCBS).
- **Consequence for A02/A15:** adapters must (a) detect scale by comparing the first returned close to a documented reference quote (full VND `quote()` vs thousand-VND OHLCV is exactly a x1,000 gap), (b) never persist an adjusted series without the **retrieval date** and source (the adjustment factor changes with every later corporate action, so an adjusted close fetched in 2026 is not identical to one fetched in 2027), and (c) capture a **raw close snapshot forward in time** (full-VND `quote()` / TCBS price snapshot after the close) because no raw history is available.

### 4.3 Q3: universe and survivorship

- Vnstock lists are **today's snapshot** only ([S7]). I found no status, delisting date, ticker-change or exchange-transfer fields.
- **Free manual route (recommended in P1):**
  1. Seed from today's `list_by_exchange` (Vnstock, optional) or HOSE/HNX/UPCoM web lists, stored as a **dated snapshot** (`universe_version`, `retrieved_at`, `source`).
  2. **Re-snapshot daily** and diff: new symbols = listings, missing symbols = delisting/suspension candidates, exchange-label change = transfer. This builds a true point-in-time universe **from the first run onward** (Observed design, no source needed).
  3. **Back-fill events for 2018–2026** into a curated CSV (`ticker, event, effective_date, from_exchange, to_exchange, source_url`) from exchange announcements. Volume is moderate (press shows batches such as 25 UPCoM delistings in one day, HOSE/HNX forced delistings, FLC-group moves HOSE→UPCoM, UPCoM→HOSE/HNX moves); budget this as a bounded manual task owned by P1 data work, not an ongoing dependency.
  4. Flag every symbol without a verified `first_seen`/`last_seen` as `universe_status = UNVERIFIED`.
- **Price history for delisted tickers is probably not retrievable** from Vnstock/TCBS (symbols are absent from the lists). That is Inferred; a one-time test with a key against two known delisted tickers (e.g., those named in §4.3 sources) should confirm (§7).
- **Official routes:** HOSE (`hsx.vn`) is a JS single-page app (Observed: 1.9 KB shell, `main.*.js`; no documented API; `robots.txt` allows all). `hnx.vn` serves HTML pages but I could not parse the structure in this session; `vsd.vn` did not respond to my requests; `congbothongtin.ssc.gov.vn` (SSC disclosure portal, Decision 245/QĐ-UBCK 2024; since 2024-03 listed firms disclose via a single entry point) did not connect. HOSE sells market-information and historical-statistics products (paid). These are **reference-reading** sources, not APIs.

### 4.4 Q4: corporate actions

- **Vnstock** (VCI): `events.calendar()` fields listed in the Q4 row ([S7]); also `company(s).events()` (22 columns, FPT = 234 rows, depth unstated) and `capital_history()` (KBS; charter capital over time, date/charter_capital/currency, can sanity-check share-count changes).
- **SSI:** `GET /api/v3/data/corporateActions`: params `from`, `to` (**span capped at 5 days**), `symbol` (optional; omit for all), `pageSize` 10/20/50/100; response `symbol, eventTitle, exrightDate, recordDate, issueDate, exchange, ratio`; sorted by ex-date descending; for new announcements `exrightDate`/`ratio` may be empty; **no event-type field** (type only implied in `eventTitle`) ([S17]). Back-filling 8 years needs at least 2,920 / 5 = **584 windowed calls** plus paging.
- **Handoff §7.1 needs** announcement date, ex-date, effective/payment date, adjustment terms, source. Vnstock gives `public_date`, `ex_right_date`, `record_date`, `payout_date`, `ratio`, `value`; SSI gives no announcement date field. Neither is verified for completeness (e.g., 5:1 splits, rights ratios, stock dividends). **Unknown** until a sample audit.
- **Fallback for A15:** where an event cannot be confirmed, do not trust any series crossing it: mark the span `ADJUSTMENT_UNVERIFIED` and exclude it from return features (the "no fake crash" rule).

### 4.5 Q5: financial statements and availability dates

- Community statements are **reduced and period-capped**: 8 most recent periods, level-1 only, so **8 quarters ≈ 2 years**, not 8 years ([S1], [S3]). With 8 periods and no publication date, **no retrospective training use is possible from this source** (A07).
- **Availability proxy:** the handoff says a quarter end is not the public availability date (§7.2). Conservative proxy = fiscal period end + the statutory disclosure deadline, applied by R07; from memory (not verified this session) the rules in Circular 96/2020/TT-BTC set short deadlines for quarterly statements and 90 days for audited annual statements. R07 must confirm exact numbers and any 2024 amendment. Real publication timestamps exist on the exchange/company disclosure pages and in the PDF upload paths on third-party hosts (e.g., `static2.vietstock.vn/vietstock/2025/1/22/...baocaotaichinh_q4_2024.pdf`, Observed in search results); these are usable only for **manual spot checks** of the proxy, not as a dependency.
- **A06** (favorite lacks statements): Vnstock raises/returns NaN for missing items; keep "missing" distinct from "provider error" (§7.2) in the adapter.
- **Paid/extended:** `ratio`, `note`, `financial_health`, `filing()` (with report links, both separate "riêng" and consolidated "hợp nhất") are Extended ([S3]) → `PAID/OPTIONAL`.

### 4.6 Quota-fit: daily scan of ~1,600 tickers (real numbers)

Assumptions: universe 1,600 tickers (handoff figure; Vnstock's own list returned ~1,754 codes that include non-stock symbols); one incremental daily-bar request per ticker; 22 sessions per month; Vnstock enforces 1 s spacing on Guest/Community ([S1]); TCBS guidance "< 10 requests per second" ([S23]).

| Workload | Calls | Guest (10/min, 100/h, 300/day, 1,000/month) | Vnstock Community (quota unpublished) | TCBS OpenAPI (R01) | SSI Data |
| --- | --- | --- | --- | --- | --- |
| **Daily incremental OHLCV** | 1,600/day (~35,200/month) | Max 300/day = **18.8% of universe/day; full cycle = 6 sessions**; monthly cap 1,000 = **0.63 of one full scan per month**. **Not viable** | Needs **≥ 1,600/day and ≥ ~35,200/month**; at 1 s spacing a run takes **≥ 26.7 min**; hourly quota must be ≥ 1,600 or the run must span 2+ hours | 1,600 / 10 rps = **160 s (2.7 min)**; one 8-hour token covers it | per-key limit **unpublished**; response headers `X-RATELIMIT-*` report it |
| **One-time backfill OHLCV** (8 y ≈ 2,000 rows/ticker, under the 10,000 row cap) | 1,600 calls (3.2 M rows total) | 1.6 months of monthly quota | Same 1,600 calls; but **history only reaches back ~8 years from today (≈ Nov 2018)**; the early window moves forward each day | depth unstated | "since the security started trading"; paging needed (default pageSize 10; max unstated) |
| **Statements refresh** (3 statements, period empty returns annual and quarterly) | 4,800 per full refresh | Not available (no financial periods) | 4,800 calls ≈ 80 min at 1 s; concentrated in reporting seasons | no endpoint found | n/a |
| **Indices** (VN, VN30, HNX, UPCoM, HNX30) | 5/day | trivial | trivial | trivial | trivial |
| **Corporate events** (date-range calls) | 1–10/day | trivial | `events.calendar` 1 call per range (limit 20,000 rows) | none | 584 windowed calls for an 8-year backfill |
| **Universe snapshot** | 1–3/day | trivial | trivial | unknown endpoint | `securitiesByBoard` |

**Conclusions:** (1) Guest is **unusable** for a whole-market scan (A05 will always be "partial"). (2) Community adequacy cannot be decided from public pages; it needs the number from `vnstock usage` (see §7). (3) Handoff §7.3 priority rule applies: holdings → watchlist → resumable batches; the scan report must show exact attempted/completed/failed counts (A05). (4) At 10 req/s TCBS fits easily if R01 confirms the endpoint and token flow. (5) Whether a multi-symbol request (the VCI payload accepts a `symbols` list) counts as one quota unit is Unknown; do not rely on it.

### 4.7 Q8: cross-check method and tolerances

**Sample (20 tickers x 3 dates = 60 point checks), stratified, fixed and versioned in the repo:** 8 HOSE (2 VN30, 3 mid-cap, 3 small/low-priced), 6 HNX, 6 UPCoM; **must include** ≥ 1 bank, ≥ 5 tickers with a cash/stock dividend, split or rights event in the 8-year window, ≥ 2 low-liquidity names with suspension days, ≥ 1 ticker listed < 3 years.
**Dates:** (a) a recent session (most recent completed), (b) a session shortly **before** a known ex-date of a sampled corporate action, (c) a session near the **start** of available history (depth boundary, ~2018-11 for Community).
**Reference ("known values"):** the official exchange close/volume from the exchange's own daily report for that ticker/date (manual lookup, 60 values once) and the corporate-action ratio from the company's disclosure.

| Check | Rule | Tolerance | On failure |
| --- | --- | --- | --- |
| Unit | After normalising to VND, source A close ÷ source B close | in [0.99, 1.01]; ratios near 1,000 or 0.001 = unit error | Block affected sizing (A02) |
| Raw close, same date, no corporate action after it | |A − B| | ≤ 1 price tick (HOSE equities: 10 VND below 10,000; 50 VND to 49,950; 100 VND from 50,000, tick table from memory, R03 owns) | Investigate |
| Adjusted close, any date | |A − B| / B | ≤ max(0.1%, 1 tick) (Vnstock itself documents VCI vs KBS differing "by a few đồng"); > 0.5% = FAIL | Mark series `ADJUSTMENT_UNVERIFIED` |
| Daily return across a corporate-action date | |r_A − r_B| | ≤ 0.2 percentage points, and no |r| beyond the ±7%/10%/15% band without an event | Flag fake crash (A15) |
| Volume | matched volume, same definition | exact match expected; ≤ 1% difference tolerated; larger = check negotiated/put-through inclusion (turnover definition is a §4.3 item) | Record definition difference |
| High ≥ max(open, close), Low ≤ min, volume ≥ 0, no duplicate dates | all rows | zero violations | Reject bar |
| Calendar continuity | trading dates vs exchange calendar | 0 missing sessions except documented suspensions; zero-volume days kept as rows (not forward-filled) | Gap report |
| Corporate-action coverage | events found in source A for sampled tickers vs company disclosure | 100% of sampled events found; ratio exact | Source marked incomplete |

Run on first integration, after every library/provider version change (A26), and monthly on a rotating sample of 5 new tickers. Store results with provider version and `retrieved_at`.

### 4.8 Q6: alternatives, short evidence

- **SSI FastConnect.** Documented REST, e.g. `GET /api/v3/data/ohlc` (`symbol, from, to, timeFrame 1m–1d, pageIndex, pageSize`; intraday = most recent 1 year; daily since first trading; bearer JWT) and `corporateActions`; endpoint list also includes securities by board, securities summary, index list/summary, and a market-data file download. Service overview: "SSI chưa thu phí sử dụng dịch vụ FastConnect API"; "FastConnect API chỉ cấp cho khách hàng đã có tài khoản giao dịch"; keys (ConsumerID, ConsumerSecret, RS256 PrivateKey, shown once), validity one year with renewal, 90-day inactivity suspension, SSI "có quyền ngừng cung cấp dịch vụ... bất cứ khi nào" ([S14]–[S19]). Terms: information "chỉ phục vụ cho mục đích giao dịch chứng khoán của Khách hàng" and may not be given to third parties even processed ([S15]). A local personal scanner fits; any later sharing of derived data would not. This gives SSI a **permission** profile (documented, account-bound) better than Vnstock's, at the cost of a second account.
- **DNSE.** Docs describe market data (depth, price moves, OHLC, indices) and trading; key + secret auth; OTP for orders; a DNSE education page (via search summary only) says an existing DNSE securities account is required and the service covers daily/EOD/intraday OHLC and index baskets; fee, rate limits and history depth were **not** found ([S20], [S21]).
- **TCBS.** `bars-long-term` accepts `resolution` D/W/M, `to` (epoch), `countBack`; Bearer token; units, adjustment, max `countBack`, history depth, rate limits **not stated**; portal advises < 10 req/s, tokens up to 8 hours; no corporate-action or statement endpoint found ([S22], [S23]). R01 owns the rest.
- **OSS libs:** vietfin (Apache-2.0, "publicly available APIs from multiple brokerage firms", README warns data is "not necessarily accurate"; income statement, ratios, dividends, events; no delisted data), vnquant (stale), pyvietstock, vntickers, forks of old vnstock. None documented as official-endpoint clients ([S25], [S26]).
- **Paid (PAID/OPTIONAL):** Vietstock DataFeed, FiinGroup/FiinPro API, Vnstock Extended tiers (ratios, notes, filings, foreign/proprietary flow, `vnd`/`mas` sources).

---

## 5. Impact on the handoff

- **Acceptance checks affected (§14):**
  - **A02** (x1,000 prices): Vnstock thousand-VND OHLCV vs full-VND quotes is a real, documented trap; adapter scale detection is mandatory.
  - **A05** (quota stops scan): Guest cannot scan the market (300/day); Community's number is unknown; test with real counts.
  - **A06** (favorite lacks statements): Community gives level-1, 8 periods only; missing vs error must be distinct.
  - **A07** (publication after decision): no free source supplies publication dates or versions; training features from statements stay excluded.
  - **A15** (corporate actions): adjusted-only series with undocumented method; raw series must be captured forward; events audit needed.
  - **A21** (survivors only): confirmed; no free recovery of delisted histories or historical membership.
  - **A26** (source revision/retraining): vendor release expiry, remote disable and un-adjusted-vs-adjusted drift require pinned snapshots and stored `retrieved_at` + adjustment version.
  - **A28** (UPCoM/restricted unsupported): Vnstock lists UPCoM; coverage and trading restriction status of UPCoM symbols is Unknown for TCBS.
- **Proposed handoff changes (proposal only):**
  - §4.1, Vnstock paragraph: current text "roughly eight years of daily history, eight recent financial reporting periods, … account-dependent quotas, and one-device restrictions" → add "Vnstock v5 is a proprietary-licence client over undocumented broker endpoints (VCI, KBS); builds expire after 365 days; a remote policy can disable the library; the PyPI project is quarantined (2026-09-24); licence-2026.11 takes effect 2026-11-30 and needs explicit acceptance." Reason: the handoff wording implies a stable optional dependency.
  - §4.1/§4.2: add the sentence "Vnstock Community is never the sole input of a trained or traded signal; Guest tier is unsuitable for any universe scan (300 calls/day)."
  - §7.2: add "Vnstock equity OHLCV is adjusted-only and thousand-VND, rounded to 2 decimals by default (`floating=None` for source precision); capture a raw close snapshot forward in time because raw history is not offered."
  - §9.4 / model card: adopt the limitation wording in §5 below.
  - §14: add an acceptance check for **data-library supply-chain/agent-config safety** (see §6, trap 7), e.g., "A29: installing/importing a data library does not modify agent rule files, shell profiles or global config (verified by file-hash diff before/after)".
- **Input for `docs/data_capabilities.md` / ADRs:**
  - ADR candidate: "Data source routing": P1/P2/P3 as in §3; all providers behind adapters; Vnstock allowed only as `optional` adapter flagged `UNDOCUMENTED_UPSTREAM`.
  - Capability matrix below (copy directly).
  - Cross-check protocol §4.7 and the sample file as a fixture.
  - Daily universe snapshot table + curated events CSV schema (§4.3).

### 5.1 Source x capability matrix

| Capability | TCBS OpenAPI | SSI FastConnect Data | DNSE OpenAPI | Vnstock Community v5 (VCI/KBS) | Exchanges / VSDC / SSC portals | Paid (PAID/OPTIONAL) |
| --- | --- | --- | --- | --- | --- | --- |
| **Documentation status** | Documented | Documented | Documented | Library documented; **upstream undocumented** | Human pages; no documented bulk API found | Documented |
| **Price history (daily)** | `bars-long-term` D/W/M; depth **Unknown** | `data/ohlc` 1d; since first trading (Documented) | Advertised (EOD/intraday); depth Unknown | ~8 y (2,920 d), adjusted, ≤ 10,000 rows | Official daily stats on site; manual | Full |
| **Intraday** | Not R02 scope | 1m–1h, last 1 year | Advertised | 1m 180 d; 5m–1H 365 d | n/a | Unlimited |
| **Universe (current)** | Unknown endpoint | `securitiesByBoard`, `securitiesSummary` | Unknown | `equity.list` / `list_by_exchange` (current only) | Web lists per exchange | Yes |
| **Universe (historical) / delisted / transfers / ticker changes** | Unknown | Unknown | Unknown | **No** | Announcements only (manual curation) | Likely, not verified |
| **Corporate actions** | None found | `corporateActions` (5-day window, no type field, account) | Unknown | `events.calendar` (VCI), `company.events`, `capital_history` | Company/exchange notices; VSDC | Yes |
| **Financial statements (items)** | None found | None found | None found | 3 statements, level-1, 8 periods | Company/SSC disclosure PDFs (manual) | Full tree, notes, ratios |
| **Publication dates / restatement versions** | n/a | n/a | n/a | **No / not documented** | Timestamp on each disclosure page (manual); versions = separate filings | `filing()` links (Extended), not versioned |
| **Indices (VN, HNX, UPCoM, VN30)** | `type=index` | index list/summary | Index baskets | `market.index.ohlcv` (KBS/VCI) | Official | Yes |
| **Index membership history** | Unknown | `IndexComponents`-type data not confirmed | Unknown | Current only | HOSE review announcements (manual) | Likely |
| **Sector/ICB with effective dates** | Unknown | Unknown | Unknown | ICB L1–4 current snapshot, **no effective dates** | Exchange sector indices | Yes |
| **Units** | Not stated (example looks like full VND) | Not stated (strings) | Unknown | Equity OHLCV thousand VND; quotes/statements full VND | Official VND | Per provider |
| **Adjusted vs raw** | Not stated | Not stated | Unknown | **Adjusted only** (VCI ≠ KBS by few đồng) | Raw official | Per provider |
| **Quota / rate** | "< 10 req/s" advice; token ≤ 8 h | per-key, unpublished (headers) | Unknown | Guest 10/100/300/1,000; Community unpublished; 1 s pacing | n/a | Higher |
| **Auth** | API key + iOTP → JWT | ConsumerID/Secret + RS256 key → JWT | API key + secret (+OTP for orders) | API key (vendor) + device registration; remote policy | none | Vendor key |
| **Terms / eligibility** | Free registration (handoff §4.1); terms to be read (R01) | Free "for now"; **SSI trading account required**; personal trading use only; no third-party sharing; 1-year term | DNSE account apparently required; fee unknown | Free personal/study/research; 1 device; **licence-2026.11 effective 2026-11-30**; release expires in 365 d; source terms are the user's duty | Public reading; HOSE data products paid | Paid |

### 5.2 Model-card limitations (exact wording proposed)

These are the things that remain unavailable under P1 and must appear in the model card and capability report.

1. **Survivorship bias.** "The training universe consists only of securities that were listed on the date the data was first captured. Securities delisted, merged or suspended before that date are absent from the price history, so backtests are optimistic by an unknown amount. Delisting/transfer events from 2018 onward are recorded only where a curated announcement was found."
2. **No point-in-time universe before first capture.** "Exchange membership (HOSE/HNX/UPCoM), ticker names and index membership (VN30, HNX30) before the first locally captured snapshot are reconstructed from announcements and may be incomplete."
3. **Adjusted prices only; adjustment method not disclosed by providers.** "Historical prices are provider-adjusted for corporate actions using an undocumented method and snapshot date. Raw (unadjusted) closes exist only from the first local capture date. Absolute-price features are excluded; returns spanning unverified corporate actions are excluded."
4. **Corporate-action coverage unverified.** "Dividend, bonus, rights and split events come from a provider event calendar or curated notices; completeness and ratio accuracy were checked on a sample only."
5. **No publication dates and no restatement history for financial statements.** "Financial-statement fields are shown as of the latest provider snapshot with no verified disclosure date. They are not used as training features. Original-versus-restated values cannot be recovered."
6. **Financial depth.** "Free statement data covers the most recent 8 reporting periods at summary (level-1) granularity only: no notes, no detailed line items, no ratios beyond what can be computed from level-1 fields; banking metrics (NPL, NIM, capital adequacy) are unavailable unless supplied by an entitled source."
7. **History depth.** "With the free Vnstock tier the daily history window is limited to about 8 years back from the retrieval date; the training window is therefore at most about 2018-11 onward."
8. **Unavailable fields.** "Foreign and proprietary trading flows, historical sector classification with effective dates, intraday history beyond provider windows, and turnover split between matched and negotiated trades are not available."
9. **Source stability.** "Optional Vnstock inputs depend on undocumented broker endpoints and on a vendor policy service that can disable the library or expire a release; values may change between runs and are cross-checked on a sample only."

---

## 6. Risks and traps found

1. **Vnstock v5 can stop working for reasons unrelated to our code:** release expiry in 365 days, remote kill switch, policy-fetch dependency, licence re-acceptance on 2026-11-30, PyPI quarantine. A locked dependency (handoff §14, A26) conflicts with expiring builds.
2. **Undocumented upstreams** (VCI, KBS): permission and stability risk; Vnstock disclaims third-party data rights.
3. **Thousand-VND trap and rounding trap** (Q2): x1,000 mismatches (A02) and 10-VND rounding by default.
4. **Adjusted-only history:** values drift with each later corporate action; a stored adjusted series without its retrieval date is not reproducible (A26).
5. **Guest tier silently inadequate** (300 calls/day, no financials); Community quota unpublished.
6. **Survivorship** is structural, not fixable with free data.
7. **Agent-configuration injection by a data library (≤ 4.0.8)**; and the vendor index ships v5 as compiled artefacts that cannot be audited. Use an isolated environment, hash agent config files before/after install, never run it inside the agent's home directory context.
8. **Source disagreement:** HOSE group count 430 (VCI) vs 406 (KBS); VCI vs KBS adjustment differences; the docs themselves are inconsistent (Guest daily-row cap 1,000 vs 5,000; financial periods for Guest "none" vs "4").
9. **SSI ToS:** use limited to own trading, no sharing of processed data, may be withdrawn without notice, 90-day inactivity suspension.
10. **Fetch-tool caveat:** my page extractions came from a summariser; I cross-checked the 2,920-day figure on two Vnstock pages but other numbers are single-source.

---

## 7. Open questions

- **Answerable later by research:**
  - Vnstock v5 source/behaviour (does it still expose agent-setup hooks; exact transforms; whether `symbols` lists count as one query) once a legitimate build is available. Confirm the reason for the PyPI quarantine and whether it is lifted.
  - Vnstock paid-tier prices (pricing page content was truncated in my fetch) and Community numeric quota.
  - Exact statutory disclosure deadlines and any 2024 amendment (R07 owns).
  - HOSE/HNX/VSDC pages that publish listing, delisting and transfer lists in bulk, and any official free historical data downloads (the `awesome-vietnam-finance-data` list mentions an "HNX Market Data" official free download; not verified). My fetches of `hnx.vn`, `vsd.vn` and `congbothongtin.ssc.gov.vn` failed on certificates/connection, and `hsx.vn` is a JS app.
  - SSI per-endpoint rate limits, `pageSize` maximum, history depth of `corporateActions`; whether SSI Data requires an activated, funded account; DNSE fees, limits and depth.
  - Existence and units of a TCBS securities-list / corporate-action endpoint (R01).
- **Needs user input or real credentials:**
  - **User decision (G1):** if R01 says TCBS cannot run unattended or lacks history, choose between opening an SSI account (documented, free now) and accepting Vnstock's undocumented upstreams.
  - **User action:** create a Vnstock Community key *only if* the user wants the optional adapter; then run `vnstock usage`, `vnstock policy`, `vnstock status` and report the numbers (daily/hour/month quota, 1 device, expiry), and read licence-2026.11 before 2026-11-30.
  - With keys: test a delisted ticker on TCBS/Vnstock/SSI; compare units/adjustment against known exchange closes (§4.7); count whether a multi-symbol call is one quota unit; sample-audit corporate actions.
  - Whether the user already has a SSI or DNSE account (would change the ranking).

---

## 8. Sources

All accessed **2026-11-05**. "Version" is the library/doc version shown at access.

| ID | Title / URL | Type | Version / date |
| --- | --- | --- | --- |
| S1 | Vnstock: Cấp quyền và giới hạn — https://www.vnstocks.com/docs/vnstock/tham-khao/cap-quyen-va-gioi-han | official | vnstock v5.0.1; policy "bản 1" 2026-10-10, route list 2026-10-18 |
| S2 | Vnstock: Truy xuất dữ liệu thị trường — https://www.vnstocks.com/docs/vnstock/thi-truong-market | official | v5.0.1 |
| S3 | Vnstock: Truy xuất báo cáo tài chính — https://www.vnstocks.com/docs/vnstock/co-ban-fundamental | official | v5.0.1 |
| S4 | Vnstock: Nguồn dữ liệu — https://www.vnstocks.com/docs/vnstock/tham-khao/data-sources | official | v5.0.1 |
| S5 | Vnstock: Xử lý lỗi — https://www.vnstocks.com/docs/vnstock/tham-khao/xu-ly-loi | official | v5.0.1 |
| S6 | Vnstock: Đăng nhập và dòng lệnh — https://www.vnstocks.com/docs/vnstock/cau-hinh-va-dong-lenh | official | v5.0.1 |
| S7 | Vnstock: Truy xuất thông tin tham chiếu — https://www.vnstocks.com/docs/vnstock/tham-chieu-reference | official | v5.0.1 |
| S8 | Vnstock: Lịch sử phiên bản — https://www.vnstocks.com/docs/tai-lieu/lich-su-phien-ban | official | latest entry 2026-10-27 |
| S9 | Vnstock: Giới thiệu thế hệ 5 — https://www.vnstocks.com/docs/vnstock/gioi-thieu | official | v5.0.1 |
| S10 | Vnstock Software License — https://www.vnstocks.com/policies/license | official | license-2026.11, published 2026-10-24, effective 2026-11-30 |
| S11 | thinh-vu/vnstock repo (README, LICENSE.md, CHANGELOG.md, `vnstock/explorer/{vci,kbs}/const.py`, `quote.py`, `core/utils/transform.py`) — https://github.com/thinh-vu/vnstock (cloned to scratchpad, read only) | OSS | 4.0.9, commit `71b853f` (2026-10-13); licence license-2026.09 |
| S12 | PyPI: vnstock — https://pypi.org/project/vnstock/ and https://pypi.org/simple/vnstock/ | official registry | quarantined 2026-09-24; latest listed 4.0.8; direct index check 2026-11-05 |
| S13 | Vnstock blog: API rate limit — https://vnstocks.com/blog/api-rate-limit-la-gi-cach-xu-ly-trong-vnstock | official blog | article 2025-04-12, quota section updated 2026-10 |
| S14 | SSI FastConnect service overview — https://developers.ssi.com.vn/docs/faq/service-overview | official | accessed 2026-11-05 |
| S15 | SSI developer terms — https://developers.ssi.com.vn/term-condition | official | accessed 2026-11-05 |
| S16 | SSI `data/ohlc` — https://developers.ssi.com.vn/docs/api-reference/data-ohlc | official | API v3 |
| S17 | SSI `data/corporateActions` — https://developers.ssi.com.vn/docs/api-reference/data-corporateActions | official | API v3 |
| S18 | SSI market-data FAQ — https://developers.ssi.com.vn/docs/faq/market-data | official | accessed 2026-11-05 |
| S19 | SSI guide, general information — https://guide.ssi.com.vn/ssi-products/general-information | official | accessed 2026-11-05 |
| S20 | DNSE API platform — https://developers.dnse.com.vn/docs/guide/intro/api_platform/ | official | accessed 2026-11-05 |
| S21 | DNSE LightSpeed API explainer (search-result summary only) — https://www.dnse.com.vn/hoc/dnse-lightspeed-api-la-gi ; PyPI `dnse-sdk-openapi` | official/secondary | dated 2026-06-08 per search |
| S22 | TCBS `bars-long-term` — https://developers.tcbs.com.vn/docs/v1.0.0/stock/bars-long-term/ | official | docs v1.0.0 |
| S23 | TCBS developer portal — https://developers.tcbs.com.vn/ | official | accessed 2026-11-05 |
| S24 | HOSE site https://www.hsx.vn/vi (JS SPA; robots allows all); HNX https://www.hnx.vn/ (HTML, structure not parsed) | official | observed 2026-11-05 |
| S25 | awesome-vietnam-finance-data — https://github.com/estevecastells/awesome-vietnam-finance-data | practitioner | accessed 2026-11-05 |
| S26 | vietfin — https://github.com/vietfin/vietfin | OSS | Apache-2.0; no releases listed |
| S27 | Press on delistings/transfers (vneconomy, 24hmoney, doanhnghiephoinhap, vietnamfinance, tuoitre; various dates, several re-dated 2026 but older events) via web search | secondary | 2026-11-05 |
| S28 | SSC disclosure system background (Decision 245/QĐ-UBCK 2024; single-point disclosure from 2024-03) via web search; portal `congbothongtin.ssc.gov.vn` did not connect | secondary | 2026-11-05 |
| S29 | HOSE market-information service (Vietstock EN 2019 summary) and ICE HOSE catalogue — https://en.vietstock.vn/2019/07/about-hoses-market-information-service-113-365572.htm | secondary | 2026-11-05 |

---

## Addendum A — Observed on this machine (2026-11-06)

First hands-on connection with Vnstock generation 5, Community tier. All items below are **Observed** unless stated. No key, device id or account data is recorded here.

| Item | Observation |
| --- | --- |
| Install | vnstock **5.2.1** (core 0.7.2) from `https://vnstocks.com/api/packages`, into `~/.venv` (Python 3.13.1, 64-bit). Install is pandas-only; no write to Claude/Codex/Gemini config files (SHA256 of `settings.json`, `.codex/AGENTS.md`, `.codex/config.toml` identical before/after). |
| Release lifetime | Build usable until 2027-10-27 (365 days). |
| Remote policy | Policy is fetched from vnstocks.com, signed, **cached for 1 hour**. It lists disabled releases: 5.0.0a2, 5.0.0, 5.0.1, 5.0.2. This confirms the remote-disable mechanism described in Q1 is live, and has already been used against released builds. |
| Tier | Guest: 8/126 functions. Community: **42/126** functions. |
| Quota display | `vnstock usage` shows **percent only** (24 h and 30 days), no absolute call counts. After one call: "<1%" for both. The absolute Community quota is therefore still **unknown**, but is now measurable by calibration (percent after N calls). |
| History depth | One call `Market().equity("FPT").ohlcv(start="2020-01-01", end="2026-11-05")` returned **1,707 daily rows** (2020-01-02 to 2026-11-05) in 623 ms. **One call per ticker covers the whole 2020-present backfill**; row cap is not a constraint at this depth. |
| Columns / types | `time` (tz-aware, Asia/Ho_Chi_Minh, stamped 07:00 — a session label, not an availability time), `open/high/low/close` float64, `volume` int64. No turnover/value column, no adjustment-factor column. |
| Units / adjustment | Prices are in **thousand VND** (FPT 2020-01-02 close = 18.99) and appear **adjusted** (an unadjusted FPT close at that time would be far higher). Default `floating=2` → 10 VND resolution. Consistent with Q2/Q3 findings; raw series still unavailable. |
| Upstream | Default source `vci` (Vietcap), request is made **from the user's machine** (POST, `vietcap.com.vn`). The library's own metadata states robots.txt for the trading host is `Crawl-delay 10` and that data is a reconstruction that "may not match the original exactly". Terms URL is returned in `df.attrs`. |

### Consequences for the plan

1. **Backfill size:** ~1,600 calls, one per ticker, rows well under any cap.
2. **Pacing is now the binding constraint, not quota or depth.** With the source's published `Crawl-delay: 10`, 1,600 calls take ≈ **4.4 hours** at 10 s spacing (vs. 27 min at the library's 1 s pacing). Recommend honoring the 10 s delay for the bulk job: it fits a single evening run and respects the upstream's stated preference. This is a decision for the user (see ADR candidate).
3. **Store the raw `df.attrs` request metadata** (source, requested_at, route, length) with each response for auditability (handoff §7.1 "Market bar" source/retrieval timestamps).
4. **Still true:** adjusted-only, thousand-VND, current-listing universe only (survivorship), no restatement/publication dates.

### Open questions closed / still open

- Closed: whether Community can reach back to 2020 (yes, observed); whether one call covers the full range (yes, observed).
- Still open: absolute Community daily/monthly quota (calibrate by percent after a known number of calls); behavior on delisted tickers; the licence text change effective 2026-11-30.

## Addendum B — Capability probe for crawl scoping (Observed 2026-11-06, vnstock 5.2.1 Community, ~20 read-only calls at 10 s spacing)

| Item | Observation |
| --- | --- |
| Daily bars | Full history from 2020 in one call (Addendum A). Not tier-capped. |
| 1H bars | **Tier cap: 365 most recent days** (library dropped 2,353 older rows). ~1,241 bars/year for FPT in one call. |
| 1m bars | **Source cap: 20,000 bars per query** (~74 sessions; "applies to every tier"); older parts need start/end windows. Estimated ~697k bars in 2020–now per ticker. A 365-day tier cap probably applies as for 1H (not separately confirmed). Intraday older than ~1 year **cannot be backfilled**; it must be collected forward. |
| Tick (seconds) | `Market().equity(s).trades()` exists (VCI); **not tested**. Out of Phase 1 scope (handoff §10.3: EOD first). |
| Tier-gated (Community) | `trade_history`, `foreign_flow`, `session_stats` → `VNSTOCK_TIER_ROUTE`. Consistent with Q1. |
| Universe | `Reference().equity.list_by_exchange()` returns 1,755 rows with `exchange`: HOSE 408, HNX 299, UPCOM 810, **DELISTED 238**; plus `organ_name`, `icb_code_lv2`. One call. |
| VN100 | `Reference().equity.list_by_group("VN100")` returns 100 symbols, all in the HOSE list. **Current snapshot only** (no membership history). |
| Sector | `Reference().industry.sectors()` returns ICB levels (8,254 rows, includes funds); `icb_code_lv2` also in the universe list. |
| **Delisted prices (revises Q3)** | Daily OHLCV from 2020 **is returned for delisted symbols** up to their delisting date: CTA 1,139 rows to 2024-07-25; KAC 1,139 rows to 2024-07-25; PSH 1,178 rows 2020-06-24 to 2025-03-11; NS2 1,517 rows to 2026-02-12. This weakens the earlier "no delisted prices" limitation for **post-2020** delistings. Caveats: n=4; CTA and KAC have identical row count/range (verify, possible coincidence); delistings before 2020, and historical *universe membership by date*, are still not available; prices remain adjusted. |
| API usage note | Constituent/list helpers hang off `Reference().index` / `Reference().equity` (not on the called `index(symbol)` object); `list_by_exchange` takes no exchange argument. |

Effect on R02 conclusions: survivorship risk is **reduced but not removed** for 2020-onward research; model-card wording must change from "no delisted prices" to "delisted prices available from 2020 only where the provider retains them; sample-verified, not exhaustively audited".

## Addendum C — 1-minute bar depth and density (Observed 2026-11-06; **corrects Addendum B on 1m**)

| Probe (interval 1m) | Result |
| --- | --- |
| FPT 2025-11-06 → 2026-01-31 | 13,551 rows, 60 sessions (≈226 bars/session). |
| FPT 2025-01-02 → 2025-03-31 (older than 365 days) | 13,126 rows. **1m is NOT capped at 365 days** (only 1H is). |
| FPT 2024-01-02 → 2024-03-29 | 12,663 rows. |
| FPT 2023-07-03 → 2023-09-29 | 3,279 rows, **first bar 2023-09-11 09:15**. |
| FPT 2023-01-03 → 2023-03-31; 2022-07-01 → 09-30; 2020-01-02 → 03-31 | 0 rows. |
| YTC (illiquid UPCoM) 2026-08-01 → 2026-11-05 | **3 rows** in 3 months: minutes with no trade have no bar. |

Conclusions: 1m history starts around **2023-09-11** (FPT; other symbols not yet checked), i.e. ~3.2 years, not 2020. Bars exist only for minutes with trades, so row count scales with liquidity (≈226/session for FPT, ≈0 for thin UPCoM names). A per-query cap of 20,000 bars exists (≈75–85 liquid sessions), so windows of ~60 sessions are safe for liquid names. 1H is fully derivable from 1m after 2023-09, so a separate 1H crawl is redundant. First bar 09:15 and last 14:45 — ATO/ATC minutes need checking against the daily bar in the pilot. Unknown: whether intraday prices are adjusted like daily ones (pilot check: compare aggregated 1m close/volume with the daily bar).

## Addendum D — Pilot results (Observed 2026-11-06; 29 symbols, 182 calls, 30 min at 10 s spacing, 0 failures)

| Check | Result |
| --- | --- |
| Throughput | 182 calls in 30.4 min = 10.0 s/call. 8 of 182 calls (4%) were truncated 1m windows that were discarded and retried smaller. |
| Calls per symbol (1m) | Tier 1 (VN100) ≈ 15.8; tier 2 ≈ 4.6; tier 3 ≈ 3.4; tier 4 ≈ 2.3. Daily = 1. |
| Rows per symbol (1m, since ~2023-09) | VN100 ≈ 175k; other HOSE ≈ 28k; HNX/UPCoM ≈ 23k (very uneven); delisted ≈ 5k. |
| Projection, full universe (1,760 symbols) | ≈ 9,300 calls ≈ **26 h** at 10 s (range 20–32 h); ≈ 53M 1m rows; ≈ 3 GB SQLite (measured 58.7 bytes/row). |
| Precision | `floating=None` returns full precision (26,209 of 39,704 rows have > 2 decimals, e.g. BFC 6.79114), confirming prices are **adjusted** (non-integer VND). The default would have rounded to 10 VND. |
| 1m vs daily | Over 8,341 symbol-days: volume ratio median 0.999 (p5 0.996, p95 1.000); last-1m-close / daily-close = 1.0000 at p5, median and p95. Intraday and daily share the same adjusted price basis and volume definition. |
| Earliest 1m date | 2023-09-11 for most HOSE/HNX names; some symbols start 2024-05-27 (e.g. BCA, DC2, E12). |
| CTA / KAC suspicion | **Closed.** Different series (CTA ≈ 0.1–3.0, KAC ≈ 14.7), same delisting date. CTA's ×2/×0.5 jumps are real tick steps on a 100–200 VND penny stock, not errors. |
| Zero-volume rows | 8,179 of 39,704 daily rows have volume 0 (tier 2: 320, tier 3: 5,166, tier 4: 2,693); 7,926 of them are flat (open=high=low=close). These are provider filler bars for days without trading, **not executable prices** (handoff §7.2). Treat `volume = 0` as "no trade", never as a price observation or a zero return. |
| OHLC inconsistencies | 269 rows violate high/low bounds; 253 of them are zero-volume filler rows, **16 have volume > 0** (e.g. CEO 2025-05-14, ND2 2020-01-02) and look like a mixed adjustment factor between fields on that day. 0.04% of rows; kept as returned and flagged by `validate`; features must not trust a bar that fails the check. |
| Calendar gaps | Two of 29 symbols miss sessions vs the VNINDEX calendar (QNP 26 of 695, MZG 8 of 493), consistent with suspensions or late listing; not verified individually. |
| Quota | ~1% of the 24 h meter after ≈ 200 calls (display is rounded; absolute number still unpublished). Not a constraint at the projected load unless the meter says otherwise during the full run. |
| Identical series | None. |

Model-card wording updated by this pilot: prices are adjusted with full precision; zero-volume bars are non-trading fillers; delisted prices exist from 2020 where retained (sample of 4 + pilot symbols); 1m history begins 2023-09 (some symbols 2024-05).

## Addendum E — Index daily data: ~1,000-row cap per call (Observed 2026-11-06)

The pilot stored only **999 rows per index starting 2022-11** for VNINDEX, VN30, HNXINDEX and UPCOMINDEX: `Market().index(sym).ohlcv` (source KBS) returns at most ~1,000 rows per call and silently keeps the newest. Fix: indices are fetched in 730-day windows; result 1,707 sessions per index from 2020-01-02 (VN30: 1,706). **`VN100` index returns 0–1 rows from this source** (the VN100 *constituent list* works), so no VN100 index series is available. Equity daily calls are not affected (VCI returned 1,700+ rows in one call). Lesson recorded as a test: `test_index_is_fetched_in_contiguous_windows`. The first `validate` run compared symbol calendars against a VNINDEX series that began in 2022-11, so its "missing sessions" figure for earlier dates was understated and must be re-run after the full crawl.
