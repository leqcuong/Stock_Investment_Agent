"""Resumable vnstock (generation 5, Community) backfill into local SQLite.

Phases
  refs    universe (exchange, VN100, ICB) + index symbols
  daily   daily OHLCV from 2020-01-01 (adjusted, thousand VND as returned by vnstock)
  1m      1-minute OHLCV from ~2023-08 (earliest available bar is ~2023-09-11)
Priority tiers: 0 indices, 1 VN100, 2 other HOSE, 3 HNX + UPCoM, 4 DELISTED.

Safety: fixed spacing between calls (default 10 s = the source's published
Crawl-delay), stop on policy/auth problems, wait and retry on quota limits,
idempotent inserts, no key is ever read or printed. Run with the vnstock venv:
  & "$HOME\\.venv\\Scripts\\python.exe" scripts\\backfill\\backfill.py <command> ...
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
import sys
import time
import warnings
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
LOGS = ROOT / "logs"
DAILY_DB = DATA / "market_daily.sqlite"
INTRA_DB = DATA / "intraday_1m.sqlite"

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
DAILY_START = "2020-01-01"
INTRADAY_START = "2023-08-01"
DELAY_S = 10.0
TRUNC_ROWS = 19_000          # per-query cap is 20,000 bars; at/above this we assume truncation
TARGET_ROWS = 12_000         # aim for windows that return about this many bars
WIN_DAYS_INITIAL = {1: 80, 2: 160, 3: 480, 4: 480}
WIN_MIN, WIN_MAX = 7, 800
INDEX_WINDOW_DAYS = 730      # index source returns at most ~1,000 rows per call
INDEX_SYMBOLS = ["VNINDEX", "VN30", "VN100", "HNXINDEX", "UPCOMINDEX"]
TIER_OF_EXCHANGE = {"HOSE": 2, "HNX": 3, "UPCOM": 3, "DELISTED": 4}
PILOT_FIXED = {1: ["FPT", "VCB", "HPG", "SSI", "VNM"], 4: ["CTA", "KAC", "PSH", "NS2"]}

SCHEMA_DAILY = """
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS symbols(
  symbol TEXT PRIMARY KEY, exchange TEXT, organ_name TEXT, icb_code_lv2 TEXT,
  in_vn100 INTEGER, tier INTEGER, snapshot_at TEXT);
CREATE TABLE IF NOT EXISTS universe_snapshot(
  snapshot_at TEXT, symbol TEXT, exchange TEXT, in_vn100 INTEGER,
  PRIMARY KEY(snapshot_at, symbol)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS daily_bars(
  symbol TEXT, d TEXT, batch TEXT, open REAL, high REAL, low REAL, close REAL,
  volume INTEGER, source TEXT, retrieved_at TEXT,
  PRIMARY KEY(symbol, d, batch)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS crawl_job(
  kind TEXT, symbol TEXT, win_start TEXT, win_end TEXT, status TEXT, rows INTEGER,
  attempts INTEGER DEFAULT 0, error_code TEXT, error_msg TEXT, requested_at TEXT,
  latency_ms INTEGER, meta TEXT,
  PRIMARY KEY(kind, symbol, win_start, win_end)) WITHOUT ROWID;
"""
SCHEMA_INTRA = """
CREATE TABLE IF NOT EXISTS bars_1m(
  symbol TEXT, ts INTEGER, open REAL, high REAL, low REAL, close REAL, volume INTEGER,
  PRIMARY KEY(symbol, ts)) WITHOUT ROWID;
"""


class StopRun(Exception):
    """Fatal condition: stop the whole run (policy, auth, release, tier)."""


class MaxCalls(Exception):
    """The per-run call budget (--max-calls) is used up."""


def classify(exc: BaseException) -> str:
    code = str(getattr(exc, "code", "") or type(exc).__name__).upper()
    if "LIMIT" in code:
        return "limit"
    if any(k in code for k in ("EXPIRED", "POLICY", "DISABLED", "AUTH", "TIER_ROUTE", "CREDENTIAL")):
        return "fatal"
    return "transient"


def now_vn() -> dt.datetime:
    return dt.datetime.now(VN_TZ)


def last_complete_session_date(now: dt.datetime | None = None) -> dt.date:
    """Today if the close (15:30) has passed, else yesterday. Weekends are harmless:
    the source simply returns no bar for a non-session day."""
    now = now or now_vn()
    d = now.date()
    return d if now.time() >= dt.time(15, 30) else d - dt.timedelta(days=1)


def iso(d: dt.date) -> str:
    return d.isoformat()


def parse(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


# --------------------------------------------------------------------------- sources
class VnstockSource:
    """Thin wrapper over vnstock 5. Returns (DataFrame[time,open,high,low,close,volume], meta)."""

    def __init__(self) -> None:
        from vnstock import Market, Reference  # imported late so tests need no vnstock

        self._Market, self._Reference = Market, Reference

    @staticmethod
    def _meta(df: pd.DataFrame, caught: list) -> dict:
        a = getattr(df, "attrs", {}) or {}
        msgs = [str(w.message) for w in caught]
        return {
            "source": a.get("source"), "route": a.get("route"), "requested_at": a.get("requested_at"),
            "latency_ms": a.get("latency_ms"), "length": a.get("length"),
            "truncated": any("20.000" in m or "20,000" in m for m in msgs),
            "warnings": [m[:160] for m in msgs],
        }

    def _ohlcv(self, handle, start: str, end: str, interval: str):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            df = handle.ohlcv(start=start, end=end, interval=interval, floating=None)
        return df, self._meta(df, caught)

    def daily(self, symbol: str, start: str, end: str, is_index: bool = False):
        h = self._Market().index(symbol) if is_index else self._Market().equity(symbol)
        return self._ohlcv(h, start, end, "1D")

    def minute(self, symbol: str, start: str, end: str):
        return self._ohlcv(self._Market().equity(symbol), start, end, "1m")

    def universe(self) -> tuple[pd.DataFrame, list[str]]:
        ref = self._Reference()
        uni = ref.equity.list_by_exchange()
        time.sleep(DELAY_S)
        vn100 = list(ref.equity.list_by_group("VN100")["symbol"])
        return uni, vn100


# --------------------------------------------------------------------------- core
class Backfill:
    def __init__(self, source, daily_db=DAILY_DB, intra_db=INTRA_DB, delay=DELAY_S,
                 sleep=time.sleep, monotonic=time.monotonic, today=None, log=None,
                 limit_wait_s=1200, limit_max_wait_s=6 * 3600, retry_waits=(30, 60, 120)):
        self.src, self.delay, self._sleep, self._mono = source, delay, sleep, monotonic
        self._today = today
        self.limit_wait_s, self.limit_max_wait_s, self.retry_waits = limit_wait_s, limit_max_wait_s, retry_waits
        self.log = log or (lambda m: print(f"{now_vn():%Y-%m-%d %H:%M:%S} {m}", flush=True))
        for p in (daily_db, intra_db):
            if str(p) != ":memory:":
                Path(p).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(daily_db))
        self.idb = sqlite3.connect(str(intra_db))
        for c in (self.db, self.idb):
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("PRAGMA synchronous=NORMAL")
        self.db.executescript(SCHEMA_DAILY)
        self.idb.executescript(SCHEMA_INTRA)
        self.calls = 0
        self.max_calls = None
        self._last_call = None
        self._waited_for_limit = 0
        if self._meta("daily_batch") is None:
            self._set_meta("daily_batch", "bf-" + iso(self.end_date()).replace("-", ""))
            self._set_meta("price_basis", "adjusted, thousand VND, as returned by vnstock (floating=None)")
        self.batch = self._meta("daily_batch")

    # -- meta / dates
    def _meta(self, k):
        r = self.db.execute("SELECT value FROM meta WHERE key=?", (k,)).fetchone()
        return r[0] if r else None

    def _set_meta(self, k, v):
        self.db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (k, v))
        self.db.commit()

    def end_date(self) -> dt.date:
        return self._today or last_complete_session_date()

    # -- pacing and one guarded call
    def _pace(self):
        if self._last_call is not None:
            wait = self.delay - (self._mono() - self._last_call)
            if wait > 0:
                self._sleep(wait)
        self._last_call = self._mono()

    def _call(self, fn, *args):
        """Paced call with retry. Returns (df, meta) or raises StopRun / RuntimeError('transient:...')."""
        attempt = 0
        while True:
            if self.max_calls is not None and self.calls >= self.max_calls:
                raise MaxCalls()
            self._pace()
            self.calls += 1
            try:
                out = fn(*args)
                self._waited_for_limit = 0
                return out
            except KeyboardInterrupt:
                raise
            except Exception as e:  # noqa: BLE001 - classified below
                kind, code = classify(e), getattr(e, "code", type(e).__name__)
                if kind == "fatal":
                    raise StopRun(f"{code}: {str(e)[:200]}") from e
                if kind == "limit":
                    if self._waited_for_limit >= self.limit_max_wait_s:
                        raise StopRun(f"quota limit persisted: {code}") from e
                    self.log(f"QUOTA LIMIT ({code}); waiting {self.limit_wait_s // 60} min "
                             f"(total waited {self._waited_for_limit // 60} min)")
                    self._sleep(self.limit_wait_s)
                    self._waited_for_limit += self.limit_wait_s
                    continue
                if attempt < len(self.retry_waits):
                    self.log(f"transient error {code}; retry {attempt + 1}/{len(self.retry_waits)}")
                    self._sleep(self.retry_waits[attempt])
                    attempt += 1
                    continue
                raise RuntimeError(f"{code}: {str(e)[:200]}") from e

    # -- job bookkeeping
    def _cursor(self, kind, symbol):
        r = self.db.execute("SELECT MAX(win_end) FROM crawl_job WHERE kind=? AND symbol=? AND status='done'",
                            (kind, symbol)).fetchone()
        return parse(r[0]) if r and r[0] else None

    def _job(self, kind, symbol, ws, we, status, rows=0, code=None, msg=None, meta=None):
        self.db.execute(
            "INSERT INTO crawl_job(kind,symbol,win_start,win_end,status,rows,attempts,error_code,error_msg,"
            "requested_at,latency_ms,meta) VALUES(?,?,?,?,?,?,1,?,?,?,?,?) "
            "ON CONFLICT(kind,symbol,win_start,win_end) DO UPDATE SET status=excluded.status,rows=excluded.rows,"
            "attempts=attempts+1,error_code=excluded.error_code,error_msg=excluded.error_msg,"
            "requested_at=excluded.requested_at,latency_ms=excluded.latency_ms,meta=excluded.meta",
            (kind, symbol, ws, we, status, rows, code, msg, now_vn().isoformat(timespec="seconds"),
             (meta or {}).get("latency_ms"), json.dumps(meta or {}, ensure_ascii=False)))
        self.db.commit()

    # -- reference data
    def refs(self):
        uni, vn100 = self.src.universe()
        vn100s = set(vn100)
        snap = now_vn().isoformat(timespec="seconds")
        rows = []
        for r in uni.itertuples(index=False):
            ex = str(r.exchange)
            tier = 1 if (r.symbol in vn100s and ex == "HOSE") else TIER_OF_EXCHANGE.get(ex)
            if tier is None:
                self.log(f"skip {r.symbol}: unknown exchange {ex}")
                continue
            rows.append((r.symbol, ex, _s(getattr(r, "organ_name", None)), _s(getattr(r, "icb_code_lv2", None)),
                         int(r.symbol in vn100s), tier, snap))
        for s in INDEX_SYMBOLS:
            rows.append((s, "INDEX", s, "", 0, 0, snap))
        self.db.executemany("INSERT OR REPLACE INTO symbols VALUES(?,?,?,?,?,?,?)", rows)
        self.db.executemany("INSERT OR IGNORE INTO universe_snapshot VALUES(?,?,?,?)",
                            [(snap, r[0], r[1], r[4]) for r in rows])
        self.db.commit()
        self.log(f"refs: {len(rows)} symbols stored ({len(vn100s)} in VN100)")
        return len(rows)

    def symbols(self, tiers, only=None):
        q = "SELECT symbol, tier, exchange FROM symbols WHERE tier IN (%s)" % ",".join("?" * len(tiers))
        out = self.db.execute(q + " ORDER BY tier, symbol", list(tiers)).fetchall()
        return [r for r in out if (only is None or r[0] in only)]

    def pilot_symbols(self):
        picks = {0: list(INDEX_SYMBOLS)}
        have = {s: t for s, t, _ in self.symbols([0, 1, 2, 3, 4])}
        for t, names in PILOT_FIXED.items():
            picks[t] = [n for n in names if have.get(n) == t]
        import random
        rnd = random.Random(7)
        for t, label, n in ((2, "HOSE", 5), (3, "HNX", 5), (3, "UPCOM", 5)):
            pool = sorted(s for s, tt, ex in self.symbols([t]) if ex == label)
            picks.setdefault(t, [])
            picks[t] += rnd.sample(pool, min(n, len(pool)))
        return {s for v in picks.values() for s in v}

    # -- daily
    def do_daily(self, symbol, tier):
        """Equities: one window start..end. Indices (tier 0): the index source caps a call at ~1,000 rows,
        so they are fetched in INDEX_WINDOW_DAYS windows."""
        end = self.end_date()
        cur = self._cursor("daily", symbol)
        if tier == 4 and cur:
            return "skip"
        start = (cur + dt.timedelta(days=1)) if cur else parse(DAILY_START)
        status = "skip"
        while start <= end:
            stop = min(start + dt.timedelta(days=INDEX_WINDOW_DAYS - 1), end) if tier == 0 else end
            ws, we = iso(start), iso(stop)
            try:
                df, meta = self._call(self.src.daily, symbol, ws, we, tier == 0)
            except RuntimeError as e:
                self._job("daily", symbol, ws, we, "failed", 0, "transient", str(e))
                self.log(f"daily {symbol}: FAILED {e}")
                return "failed"
            n = self._store_daily(symbol, df, meta)
            self._job("daily", symbol, ws, we, "done", n, meta=meta)
            self.log(f"daily {symbol} tier{tier}: {n} rows {ws}..{we}")
            start = stop + dt.timedelta(days=1)
            status = "done"
        return status

    def _store_daily(self, symbol, df, meta):
        if df is None or len(df) == 0:
            return 0
        d = df["time"].dt.strftime("%Y-%m-%d")
        ra = now_vn().isoformat(timespec="seconds")
        src = meta.get("source")
        rows = [(symbol, a, self.batch, _f(o), _f(h), _f(l), _f(c), _i(v), src, ra)
                for a, o, h, l, c, v in zip(d, df["open"], df["high"], df["low"], df["close"], df["volume"])]
        self.db.executemany("INSERT OR IGNORE INTO daily_bars VALUES(?,?,?,?,?,?,?,?,?,?)", rows)
        self.db.commit()
        return len(rows)

    # -- 1m
    def do_minute(self, symbol, tier):
        end = self.end_date()
        cur = self._cursor("1m", symbol)
        if tier == 4 and cur:
            return "skip"
        start = (cur + dt.timedelta(days=1)) if cur else parse(INTRADAY_START)
        win = WIN_DAYS_INITIAL.get(tier, 160)
        status, total = "skip", 0
        while start <= end:
            stop = min(start + dt.timedelta(days=win - 1), end)
            ws, we = iso(start), iso(stop)
            try:
                df, meta = self._call(self.src.minute, symbol, ws, we)
            except RuntimeError as e:
                self._job("1m", symbol, ws, we, "failed", 0, "transient", str(e))
                self.log(f"1m {symbol}: FAILED {e}")
                return "failed"
            n = 0 if df is None else len(df)
            if (n >= TRUNC_ROWS or meta.get("truncated")) and win > WIN_MIN:
                win = max(WIN_MIN, win // 2)
                self.log(f"1m {symbol}: truncated at {n} rows; window -> {win}d")
                continue
            self._store_minute(symbol, df)
            self._job("1m", symbol, ws, we, "done", n, meta=meta)
            total += n
            days = (stop - start).days + 1
            if n > 0:
                win = int(min(WIN_MAX, max(WIN_MIN, TARGET_ROWS / (n / days))))
            else:
                win = min(WIN_MAX, win * 2)
            start = stop + dt.timedelta(days=1)
            status = "done"
        if status == "done":
            self.log(f"1m {symbol} tier{tier}: {total} rows")
        return status

    def _store_minute(self, symbol, df):
        if df is None or len(df) == 0:
            return
        ts = ((df["time"] - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(seconds=1)).astype("int64")
        rows = [(symbol, int(t), _f(o), _f(h), _f(l), _f(c), _i(v))
                for t, o, h, l, c, v in zip(ts, df["open"], df["high"], df["low"], df["close"], df["volume"])]
        self.idb.executemany("INSERT OR IGNORE INTO bars_1m VALUES(?,?,?,?,?,?,?)", rows)
        self.idb.commit()

    # -- orchestration
    def close(self):
        self.db.close()
        self.idb.close()

    def run(self, phases, tiers, only=None, max_calls=None):
        """Returns exit code: 0 ok, 2 fatal stop, 3 stopped by max_calls."""
        self.max_calls = None if max_calls is None else self.calls + max_calls
        syms = self.symbols(tiers, only)
        self.log(f"run phases={phases} tiers={tiers} symbols={len(syms)} delay={self.delay}s")
        try:
            for phase in phases:
                fn = self.do_daily if phase == "daily" else self.do_minute
                for symbol, tier, _ex in syms:
                    if phase == "1m" and tier == 0:
                        continue
                    fn(symbol, tier)
        except MaxCalls:
            self.log(f"max_calls={max_calls} reached; resume by running the same command again")
            return 3
        except StopRun as e:
            self.log(f"STOPPED: {e}")
            return 2
        self.log(f"finished; calls this run: {self.calls}")
        return 0

    def status(self):
        out = []
        q = ("SELECT j.kind, s.tier, j.status, COUNT(DISTINCT j.symbol), SUM(j.rows), COUNT(*) FROM crawl_job j "
             "LEFT JOIN symbols s ON s.symbol=j.symbol GROUP BY 1,2,3 ORDER BY 1,2,3")
        for r in self.db.execute(q):
            out.append(f"{r[0]:6} tier={r[1]} {r[2]:7} symbols={r[3]:5} rows={r[4] or 0:>10} jobs={r[5]}")
        out.append("symbols by tier: " + str(self.db.execute(
            "SELECT tier, COUNT(*) FROM symbols GROUP BY tier ORDER BY tier").fetchall()))
        out.append(f"daily_bars={self.db.execute('SELECT COUNT(*) FROM daily_bars').fetchone()[0]} "
                   f"bars_1m={self.idb.execute('SELECT COUNT(*) FROM bars_1m').fetchone()[0]}")
        return "\n".join(out)

    # -- validation
    def validate(self):
        q = self.db.execute
        lines = ["# Backfill validation report", f"generated {now_vn():%Y-%m-%d %H:%M}", ""]
        bad = q("SELECT COUNT(*) FROM daily_bars WHERE high < MAX(open,close,low) OR low > MIN(open,close,high) "
                "OR open<=0 OR high<=0 OR low<=0 OR close<=0 OR volume<0").fetchone()[0]
        lines.append(f"- daily rows violating OHLC/positivity/volume rules: **{bad}**")
        jumps = q("""SELECT symbol, d, ROUND(close/prev,3) FROM (
              SELECT symbol, d, close, LAG(close) OVER (PARTITION BY symbol ORDER BY d) prev FROM daily_bars
              WHERE batch=?) WHERE prev>0 AND (close/prev>1.5 OR close/prev<0.6) LIMIT 15""", (self.batch,)).fetchall()
        lines.append(f"- day-over-day close jumps beyond +50%/-40% (first 15): {jumps or 'none'}")
        idx = {r[0] for r in q("SELECT d FROM daily_bars WHERE symbol='VNINDEX' AND batch=?", (self.batch,))}
        if idx:
            miss = []
            for s, lo, hi, n in q("SELECT symbol, MIN(d), MAX(d), COUNT(*) FROM daily_bars WHERE batch=? "
                                  "AND symbol NOT IN (SELECT symbol FROM symbols WHERE tier=0) GROUP BY symbol",
                                  (self.batch,)).fetchall():
                exp = sum(1 for d in idx if lo <= d <= hi)
                if exp - n > 0:
                    miss.append((s, exp - n, exp))
            miss.sort(key=lambda x: -x[1])
            lines.append(f"- symbols with sessions missing vs VNINDEX calendar: {len(miss)} (top 10: {miss[:10]})")
        # identical series
        hs = {}
        for (s,) in q("SELECT DISTINCT symbol FROM daily_bars WHERE batch=?", (self.batch,)).fetchall():
            h = hashlib.sha1(repr(q("SELECT d, close FROM daily_bars WHERE symbol=? AND batch=? ORDER BY d",
                                    (s, self.batch)).fetchall()).encode()).hexdigest()
            hs.setdefault(h, []).append(s)
        same = [v for v in hs.values() if len(v) > 1]
        lines.append(f"- groups of symbols with IDENTICAL daily close series: **{same or 'none'}**")
        lines.append(self._validate_minute())
        lines.append("")
        lines.append("## Jobs")
        lines.append("```\n" + self.status() + "\n```")
        return "\n".join(lines)

    def _validate_minute(self):
        syms = [r[0] for r in self.idb.execute("SELECT DISTINCT symbol FROM bars_1m").fetchall()]
        ratios_v, ratios_c, first = [], [], {}
        for s in syms:
            agg = self.idb.execute(
                "SELECT date(ts,'unixepoch','+7 hours') d, SUM(volume), "
                "(SELECT close FROM bars_1m b2 WHERE b2.symbol=b.symbol AND "
                "date(b2.ts,'unixepoch','+7 hours')=date(b.ts,'unixepoch','+7 hours') ORDER BY b2.ts DESC LIMIT 1) "
                "FROM bars_1m b WHERE symbol=? GROUP BY d", (s,)).fetchall()
            first[s] = agg[0][0] if agg else None
            dmap = {r[0]: (r[1], r[2]) for r in self.db.execute(
                "SELECT d, volume, close FROM daily_bars WHERE symbol=? AND batch=?", (s, self.batch))}
            for d, v, c in agg:
                if d in dmap and dmap[d][0] and dmap[d][1]:
                    ratios_v.append(v / dmap[d][0])
                    ratios_c.append(c / dmap[d][1])
        if not ratios_v:
            return "- 1m vs daily: no overlapping symbol-days yet"
        s = pd.Series(ratios_v)
        c = pd.Series(ratios_c)
        return (f"- 1m vs daily over {len(s)} symbol-days: volume ratio median {s.median():.3f} "
                f"(p5 {s.quantile(.05):.3f}, p95 {s.quantile(.95):.3f}); last-1m-close / daily-close median "
                f"{c.median():.4f} (p5 {c.quantile(.05):.4f}, p95 {c.quantile(.95):.4f}); "
                f"earliest 1m day per symbol (sample): {dict(list(first.items())[:8])}")


def _s(x):
    return "" if x is None or pd.isna(x) else str(x)


def _f(x):
    return None if x is None or pd.isna(x) else float(x)


def _i(x):
    return None if x is None or pd.isna(x) else int(x)


def prevent_sleep():
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)  # CONTINUOUS | SYSTEM_REQUIRED


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["refs", "run", "status", "validate"])
    ap.add_argument("--phase", choices=["daily", "1m", "all"], default="all")
    ap.add_argument("--tiers", default="0,1,2,3,4")
    ap.add_argument("--symbols", default="", help="comma list; overrides selection within tiers")
    ap.add_argument("--pilot", action="store_true", help="24-symbol pilot set (+VNINDEX)")
    ap.add_argument("--max-calls", type=int, default=None)
    ap.add_argument("--delay", type=float, default=DELAY_S)
    args = ap.parse_args(argv)
    LOGS.mkdir(exist_ok=True)
    src = VnstockSource() if args.command in ("refs", "run") else None
    bf = Backfill(src, delay=args.delay)
    if args.command == "refs":
        bf.refs()
    elif args.command == "status":
        print(bf.status())
    elif args.command == "validate":
        report = bf.validate()
        (DATA / "validation_report.md").write_text(report, encoding="utf-8")
        print(report)
    else:
        prevent_sleep()
        only = set(filter(None, args.symbols.split(","))) or (bf.pilot_symbols() if args.pilot else None)
        phases = ["daily", "1m"] if args.phase == "all" else [args.phase]
        tiers = [int(t) for t in args.tiers.split(",")]
        return bf.run(phases, tiers, only, args.max_calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
