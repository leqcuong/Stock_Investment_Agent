# vnstock backfill

Resumable crawler that stores vnstock (generation 5, Community) data in local SQLite.
Runs with the vnstock environment's Python only (`~/.venv`); it needs no extra packages.

```powershell
$py = "$HOME\.venv\Scripts\python.exe"; $env:DO_NOT_TRACK = "1"
& $py scripts\backfill\backfill.py refs                       # universe, VN100, indices (2 calls)
& $py scripts\backfill\backfill.py run --pilot                # 24-symbol pilot, daily + 1m
& $py scripts\backfill\backfill.py run --phase daily          # all symbols, tiers 0..4 in order
& $py scripts\backfill\backfill.py run --phase 1m             # 1-minute bars, same order
& $py scripts\backfill\backfill.py status                     # progress by kind/tier/status
& $py scripts\backfill\backfill.py validate                   # writes data\validation_report.md
```

Options: `--tiers 1,2` (0 indices, 1 VN100, 2 other HOSE, 3 HNX+UPCoM, 4 delisted), `--symbols FPT,VCB`,
`--max-calls N` (stop after N calls; run the same command again to resume), `--delay 10` (seconds between calls).

## What it stores (`data/`, git-ignored)

| File | Table | Content |
| --- | --- | --- |
| `market_daily.sqlite` | `daily_bars` | Daily OHLCV from 2020-01-01, one row per (symbol, date, batch). Prices are **adjusted, thousand VND** as returned by vnstock. |
| | `symbols`, `universe_snapshot` | Exchange, tier, VN100 flag, ICB level-2 code, snapshot time. VN100 is a **current** list only. |
| | `crawl_job` | One row per call window: status, rows, error code, latency, request metadata. |
| `intraday_1m.sqlite` | `bars_1m` | 1-minute OHLCV from ~2023-09-11 (`ts` = UTC epoch seconds; session = Asia/Ho_Chi_Minh). Bars exist only for minutes with trades. |

vnstock returns a rebuilt table, not the source's raw payload, so the table plus request metadata is what is kept.

## Behaviour

- **Pacing:** 10 s between calls (the upstream's published `Crawl-delay`).
- **Resume:** per symbol, continues after the last window marked `done`; completed work is never refetched. Delisted symbols are fetched once.
- **1m windows:** start at 80/160/480 days by tier, then adapt to about 12,000 bars per call. A result of 19,000+ bars is treated as truncated (cap 20,000), is **not stored**, and the window is halved.
- **Errors:** `*_LIMIT` → wait 20 min and retry (give up after 6 h, exit 2); release-expired / policy / auth / tier errors → stop at once (exit 2); network-type errors → 3 retries (30/60/120 s), then the symbol is marked `failed` and the run moves on. Failed symbols are retried by the next run.
- **End date:** the last completed session (today only after 15:30 Vietnam time), so an unfinished day is never stored.
- **Sleep:** the process asks Windows not to sleep while it runs (no system setting is changed). Keep the machine powered.
- **Adjusted prices change over time:** after a dividend/bonus issue vnstock re-adjusts old bars. `daily_bars.batch` identifies the retrieval batch so a later full refetch can be stored beside this one instead of overwriting it.

Never put the API key in any command or file; log in with `vnstock register` in your own terminal.

## Tests

```powershell
& "$HOME\.venv\Scripts\python.exe" -m unittest discover -s tests -v
```
