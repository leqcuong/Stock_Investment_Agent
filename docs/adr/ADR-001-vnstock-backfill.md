# ADR-001 — Use vnstock (VCI/KBS upstreams) for the initial historical backfill

- **Status:** Accepted by the user on 2026-11-06 (exception to handoff §4.3 and R02's primary recommendation)
- **Deciders:** project owner; research input from R02

## Context

Handoff §4.3 says not to depend on undocumented broker endpoints. R02 found that vnstock 5's data comes from
Vietcap (VCI) and KBS front-end endpoints that are not documented as public APIs, that the library has a
proprietary licence (new text effective 2026-11-30), expiring builds (365 days) and a remote policy that has
already disabled some releases. R02 therefore ranked it "optional, isolated, non-blocking" and TCBS OpenAPI as
primary. R01 (TCBS) has not been researched yet. The owner wants daily data from 2020 and 1-minute data for
all stocks now, prioritising VN100, then HOSE, then the rest.

R02 observations on this machine (Addenda A–C): one call returns daily history from 2020; 1-minute history exists
from about 2023-09; delisted symbols return prices up to their delisting date; prices are adjusted and in thousand VND.

## Decision

Use vnstock Community for a one-time historical backfill and for later incremental updates **until a documented
source is validated**, under these conditions:

1. Calls go through one isolated script (`scripts/backfill/`), not through application code; the rest of the
   system reads only the local SQLite files.
2. Pace at the upstream's published `Crawl-delay` (10 s); stop on policy/auth/quota signals; never bypass limits.
3. Store request metadata with every call; keep adjusted and (future) raw series separate.
4. The vnstock licence and the upstream terms remain the owner's responsibility (terms URL is in each response's metadata).
5. The 365-day release expiry and remote disable are accepted risks: the local database is the system of record,
   so losing vnstock stops updates but not analysis.

## Consequences

- Fast start; ~19–30 hours of crawling across several evenings; data limited to what Community exposes
  (no foreign/proprietary flows, no raw prices, no statement publication dates).
- Revisit when R01 shows TCBS history depth, units and adjustment: a documented source should become primary and
  vnstock the cross-check (R02 recommendation).
- Survivorship: delisted prices are available from 2020 where the provider keeps them; historical index/universe
  membership by date is not — VN100 is a current snapshot only.
