# R04 — Build vs Adopt: Quant Frameworks and Prior Art

| Field | Value |
| --- | --- |
| Wave / priority | 1 — highest schedule impact |
| Owner role | Tech lead |
| Effort budget | ~10 agent-hours (including a small fit test) |
| Feeds | P0 (scaffold), P3 (ML), P4 (simulator) |
| Acceptance checks | A08, A12, A13, A14, A20, A24, A26 |
| Possible gate | **G2** (adopting a framework as the core = large architecture change) |

## Why this matters

The handoff proposes a custom Python app (pandas, SQLite, scikit-learn, LightGBM, Streamlit) and estimates 6–12+ part-time weeks. Mature open-source frameworks already cover parts of P2–P4: feature pipelines, point-in-time data, walk-forward training, and backtesting with price limits. Adopting the right one could save weeks; adopting the wrong one could make Vietnam-specific rules (T+2, lot-aware sellability, ±7/10/15% bands, floor locks) hard to express.

## Read first

Handoff §3, §6, §9 (all), §10.1, §13, §14.

## Candidates (minimum set; add others you find)

| Category | Candidates |
| --- | --- |
| End-to-end quant research platforms | Microsoft **Qlib** (point-in-time DB, Alpha158/360, LightGBM baselines, rolling retraining, exchange model with limit thresholds; built for China A-shares, which also have price limits and a T+1 rule) |
| Backtesting engines | vectorbt (open-source edition), backtrader, zipline-reloaded, bt, backtesting.py, NautilusTrader |
| ML/validation utilities | skfolio, mlfinlab-style purged CV implementations (check licenses; some moved to paid), timeseriescv, scikit-learn splitters |
| Feature/indicator libraries | pandas-ta (check maintenance), TA-Lib, ta |
| Vietnam-specific prior art | Open-source VN scanners and screeners on GitHub, Vnstock ecosystem tools; public VN screener products (e.g., broker screeners, Simplize, FireAnt, Vietstock) for **feature ideas only** |

## Research questions

1. For each candidate: license (watch for AGPL/GPL and commercial-only modules), maintenance status (last release, open-issue health), Windows support, Python version, install footprint, CPU-only operation.
2. **Fit to Vietnam rules.** Can it model per-board price limits, T+2 settlement with lot-level sellability, board lots plus odd lots, a sale-only tax, unfilled orders at a limit-lock, and next-session entry within a price interval? Score each requirement: native / configurable / custom extension / impossible.
3. **Fit to ML contract.** Date-grouped walk-forward, purging/embargo, point-in-time features, model registry/versioning, immutable prediction storage.
4. **Fit to app needs.** Can it run inside a local daily batch job and feed a Streamlit (or similar) UI, or is it a research-only notebook tool?
5. **Fit test (required for the top 2).** Read the source or docs to sketch how A13 (gap outside entry range), A14 (stop and target in the same bar) and A10 (old settled + new unsettled lots) would be implemented. Cite the class/function names. A runnable probe in a scratch folder is optional.
6. Prior-art survey. List 5–10 VN scanner/screener projects or products and the features or pitfalls worth copying or avoiding. What do they show users, and how do they label signals?

## Options to compare

- **A. Build custom** (handoff default), using only libraries: LightGBM, scikit-learn, a small in-house simulator.
- **B. Hybrid:** custom app and simulator, borrowing a framework's components (e.g., Qlib's data/feature/model workflow for research only).
- **C. Adopt a framework as the core** (e.g., Qlib with a Vietnam exchange extension). This triggers gate G2.

## Evaluation criteria

Correctness for Vietnam rules (heaviest weight), leakage safety, solo-maintainer complexity, license, Windows/CPU friendliness, effort saved vs added, lock-in.

## Deliverable

`research/findings/R04_findings.md` with: a candidate scorecard, the fit-test sketches for the top two, a recommended option A/B/C, and the effort saved/added relative to the §13 estimate. Also state clearly whether gate G2 is triggered.

## Out of scope

Paid platforms (QuantConnect cloud, Amibroker, etc.), except a one-line `PAID/OPTIONAL` note.

## Known traps

- Assuming that China A-share support equals Vietnam support: settlement, bands and lots differ.
- vectorbt PRO is paid, while the open-source edition is limited. Check what is actually free.
- Unmaintained popular libraries.
- Frameworks that fill at the signal bar's close by default.
