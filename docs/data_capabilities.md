# Data capabilities — vnstock 5.2.1 Community (draft)

Status: **draft from the 2026-11-06 pilot** (handoff §4.3). Sources: `research/findings/R02_findings.md` Addenda A–D.
TCBS OpenAPI (R01) is not yet evaluated, so nothing here describes TCBS.

| Topic | Observation |
| --- | --- |
| Provider / version | vnstock 5.2.1 (core 0.7.2), Community tier, 42 of 126 functions. Upstreams: VCI (Vietcap) for stock bars and the universe, KBS for indices and constituent lists. Requests are made from this machine. |
| Terms / entitlement | Proprietary vnstock licence (new text effective 2026-11-30); build expires after 365 days (2027-10-27 for this install); a signed remote policy (cached 1 h) can disable releases (5.0.0–5.0.2 are disabled). Upstream robots.txt for the trading host: `Crawl-delay: 10`. |
| Authentication | API key via `vnstock register` (sealed in `~/.vnstock/auth/`); one device registered. |
| Quota | Meter shows percent of 24 h and 30 day quota only; absolute numbers unpublished. ~1% after ≈ 200 calls. |
| Daily bars | Since 2020-01-01 in one call; ~1,700 rows per liquid symbol. Not tier-capped. |
| 1-minute bars | Since ~2023-09-11 (some symbols 2024-05-27); only minutes with trades; ≤ 20,000 bars per call. Same price basis and volume as daily (volume ratio median 0.999). |
| 1-hour bars | Tier-capped to 365 days; not crawled (derivable from 1m). |
| Tier-gated | `trade_history`, `foreign_flow`, `session_stats` (VNSTOCK_TIER_ROUTE). Not available. |
| Price units / adjustment | Thousand VND (FPT 2020-01-02 close = 18.99 in default rounding); **adjusted**, no raw series, no adjustment-factor column, no turnover value column. Use `floating=None` for full precision (default rounds to 10 VND). |
| Timestamps | Daily `time` is stamped 07:00 Asia/Ho_Chi_Minh (a session label, not an availability time). 1m bars run 09:15–14:45. |
| Volume | Matched vs negotiated not stated; 1m sums match daily volume (median 0.999). |
| Universe | `Reference().equity.list_by_exchange()`: 1,755 rows — HOSE 408, HNX 299, UPCOM 810, DELISTED 238 — with ICB level-2 code. Current snapshot only. |
| VN100 | `list_by_group("VN100")` = 100 symbols (current only; no membership history). |
| Delisted symbols | Daily prices returned from 2020 up to the delisting date (e.g. NS2 to 2026-02-12). Delistings before 2020 and membership by date are not recoverable. |
| Zero-volume rows | ~21% of daily rows in the pilot (tier 3 and delisted most) are flat filler bars with volume 0: no trade. |
| Data quality | 0.04% of rows (volume > 0) fail high/low bounds, probably mixed adjustment between fields. |
| Corporate actions / financials | Not yet crawled or tested (`Reference.company.events`, `Fundamental.equity.*`). Statements: 8 periods, no publication dates (R02 Q5). |
| Indices | VNINDEX, VN30, HNXINDEX, UPCOMINDEX: 1,707 sessions from 2020-01-02 via `Market().index(symbol)` (source KBS). **Max ~1,000 rows per call** (newest kept), so fetched in 730-day windows. VN100 index series: not available (0-1 rows); VN100 constituents list works. |
| Fixtures | None committed yet. Sanitized response samples should be added under `tests/fixtures/` from the local database (no credentials in responses). |
