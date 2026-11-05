# R02 — Free Complementary Data Sources (Vnstock and Alternatives)

| Field | Value |
| --- | --- |
| Wave / priority | 1 — critical path |
| Owner role | Data engineer |
| Effort budget | ~8 agent-hours |
| Feeds | P1, P2, P3 |
| Acceptance checks | A02, A05, A06, A07, A15, A21, A26, A28 |
| Possible gate | **G1**, **G3** |

## Why this matters

ML training needs years of daily history across HOSE/HNX/UPCoM, a universe that includes delisted stocks, corporate actions, and financial statements with publication dates. The handoff names Vnstock Community as the free complement but warns about quotas, device limits, and restricted fields. This track finds the best free (or permitted) combination and documents what cannot be obtained.

## Read first

Handoff §4 (all), §7, §8.2, §9.4, §14 (A06, A07, A15, A21), §21 (S6–S8).

## Research questions

1. **Vnstock today.** Current major version, license (personal/non-commercial terms), tiers (Guest / Community / paid) with exact quotas, device restrictions, history depth per interval, financial periods (8 quarters ≠ 8 years), and which underlying sources it routes to (e.g., VCI, TCBS, MSN). For each underlying source: is it documented and permitted, or undocumented?
2. **Units and adjustment.** Price units per function (thousand VND vs VND), adjusted vs raw prices, adjustment method, and whether raw series are available at all. (A02, A15)
3. **Universe and survivorship.** Can historical listings, delistings, exchange transfers (HOSE↔HNX↔UPCoM), and ticker changes be recovered from any free source? If not, the best manual approach (e.g., exchange announcements, HOSE/HNX/VSDC lists). (A21)
4. **Corporate actions.** Free sources of dividends (cash/stock), bonus issues, rights issues, and splits, with ex-dates and ratios. Coverage quality. (A15)
5. **Financial statements.** Which free sources give statement line items (not only ratios)? Do they include **publication/disclosure dates** and keep **restatement versions**? If not, what conservative proxy is possible (R07 owns the disclosure-deadline rule)? (A06, A07)
6. **Alternatives to evaluate.** At minimum: SSI FastConnect Data (free tier? eligibility), DNSE API, exchange websites (HOSE/HNX/VSDC) for reference data, official company IR/disclosure portals, and other free OSS libraries for VN data. For each: documented?, permitted?, free?, coverage, history depth, auth, rate limits.
7. **Indices and sectors.** VN-Index, HNX-Index, UPCoM-Index, VN30 history; sector/industry classification (ICB or provider-specific) with effective dates.
8. **Cross-checking.** Propose a method to check one source against another (e.g., a sample of 20 tickers, 3 dates each) and the tolerances to use.

## Options to compare

Combinations, for example: TCBS history + Vnstock financials; Vnstock history + TCBS holdings; exchange reference data + manual corporate-action file; and so on. Recommend one **primary combination** and one fallback.

## Evaluation criteria

Gates: free for personal recurring use, permitted by terms, no undocumented scraping as a dependency. Then: history depth, point-in-time support (universe, financials), unit/adjustment transparency, quota fit for daily scans of ~1,600 tickers (state the actual counts), maintenance risk.

## Out of scope

Paid feeds (FiinPro, Vietstock subscriptions): list them as `PAID/OPTIONAL` only. Foreign/proprietary flow data beyond noting whether it is available.

## Method and starting sources

vnstocks.com docs (S6–S8), the Vnstock GitHub repo and changelog, developers.ssi.com.vn, developers.dnse.com.vn, hsx.vn, hnx.vn, vsd.vn, and the SSC/state disclosure portals.

## Deliverable

`research/findings/R02_findings.md` with:
- A source × capability matrix: history, universe, delisted, corporate actions, financials, publication dates, units, quota, terms.
- The recommended combination, plus an exact list of what remains unavailable, worded as model-card limitations.

## Known traps

- Some library outputs are in thousand VND.
- A "free" tier may forbid scheduled or automated use or limit you to one device.
- Today's ticker list is a survivorship-biased universe.
- A library that silently forward-fills or adjusts prices.
