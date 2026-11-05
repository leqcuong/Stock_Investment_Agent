# R05 — Local Stack: Point-in-Time Storage, UI, Scheduler, Config and Secrets

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | Tech lead / application engineer |
| Effort budget | ~6 agent-hours |
| Feeds | P0, P1, P5, P6 |
| Acceptance checks | A01, A03, A04, A07, A26, A27 |

## Why this matters

The handoff proposes Python + SQLite + Streamlit for a solo user on an unknown OS (the current dev machine is Windows 11). The storage design must preserve point-in-time history, revisions and immutable forecasts (§7). Getting the schema pattern right in P0/P1 is far cheaper than migrating later.

## Read first

Handoff §6, §7 (all), §10.3, §12, §15, §16 (OS row).

## Research questions

1. **Point-in-time / bitemporal patterns.** Compare: (a) append-only observations with `valid_from/valid_to` plus `recorded_at`; (b) snapshot tables keyed by `run_id`; (c) event-sourced log plus materialized views. Which best supports as-of queries ("what did we know at decision time t?"), restatements (A07, A26), and idempotent re-ingestion (A03) in SQLite? Show example DDL and an as-of query for financial observations and market bars.
2. **SQLite at this scale.** Estimate row counts (≈1,600 tickers × ~2,000+ sessions; features; plans). Check WAL mode, concurrent read (UI) while batch writes, and indexing. Is DuckDB (or Parquet) a better analytical companion for training? When does the handoff's "add Parquet only if measured" threshold get hit?
3. **Migrations.** Alembic vs a lightweight custom migrator vs sqlite-utils. Is an ORM (SQLAlchemy 2.x) worth it vs plain SQL?
4. **Packaging.** uv vs Poetry vs pip-tools for a locked, reproducible environment on Windows. Python version choice given LightGBM/Streamlit wheels.
5. **Config and secrets.** pydantic-settings (YAML + env) for validated config. Secrets via OS keyring (`keyring` → Windows Credential Manager) vs `.env` with gitignore. Show how the §12.2 config with `null` unknowns validates without inventing values.
6. **UI.** Streamlit vs NiceGUI vs Panel vs Dash for: multi-page dashboard, editable watchlist tables, a CSV upload, charting, local-only use, and low maintenance. Is Streamlit's rerun model a problem for inbox/journal edits?
7. **Scheduling on Windows (and portable).** Windows Task Scheduler vs APScheduler-in-process vs cron/systemd (if the user later switches OS). Detecting missed runs after sleep and catch-up behavior (A27). Wake-to-run options.
8. **Run audit.** A minimal pattern for `analysis_run` records (inputs, versions, coverage, errors) and structured logging without leaking credentials.

## Deliverable

`research/findings/R05_findings.md` with: a recommended stack table (library + pinned major version + reason), a schema-pattern recommendation with sample DDL/as-of queries, a scheduler/missed-run design, and a secrets approach.

## Out of scope

Hosted databases, Docker/Kubernetes, microservices, and LLM frameworks (all excluded by §6).

## Known traps

- Storing only the latest financial values.
- Using the host's UTC date as the exchange date (§7.2).
- Streamlit session state lost on rerun.
- Task Scheduler jobs that silently skip while the machine sleeps.
