"""Tests for scripts/backfill/backfill.py using a fake source (no network, no vnstock).

Run: & "$HOME\\.venv\\Scripts\\python.exe" -m unittest discover -s tests -v
"""
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "backfill"))
import backfill as bf  # noqa: E402

TODAY = dt.date(2026, 11, 5)


class VnError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def make_df(rows):
    return pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])


def day_df(start, end):
    days = pd.bdate_range(start, end, tz="Asia/Ho_Chi_Minh") + pd.Timedelta(hours=7)
    return make_df([(t, 10.0, 11.0, 9.0, 10.5, 1000) for t in days])


class FakeSource:
    """Minute source with a fixed density of bars per calendar day; enforces a 20,000-row cap."""

    def __init__(self, per_day=100, errors=None):
        self.per_day, self.errors, self.calls = per_day, list(errors or []), []

    def _maybe_raise(self):
        if self.errors:
            e = self.errors.pop(0)
            if e:
                raise VnError(e)

    def daily(self, symbol, start, end, is_index=False):
        self.calls.append(("daily", symbol, start, end))
        self._maybe_raise()
        return day_df(start, end), {"source": "fake", "truncated": False}

    def minute(self, symbol, start, end):
        self.calls.append(("1m", symbol, start, end))
        self._maybe_raise()
        n_days = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1
        n = min(self.per_day * n_days, 20_000)
        base = pd.Timestamp(start, tz="Asia/Ho_Chi_Minh") + pd.Timedelta(hours=9)
        times = [base + pd.Timedelta(minutes=i) for i in range(n)]
        df = make_df([(t, 10.0, 11.0, 9.0, 10.5, 10) for t in times])
        return df, {"source": "fake", "truncated": self.per_day * n_days > 20_000}


OPEN = []


def new_bf(src, tmp, **kw):
    kw.setdefault("sleep", lambda s: None)
    kw.setdefault("today", TODAY)
    kw.setdefault("log", lambda m: None)
    b = bf.Backfill(src, daily_db=Path(tmp) / "d.sqlite", intra_db=Path(tmp) / "i.sqlite", **kw)
    OPEN.append(b)
    return b


def add_symbol(b, symbol, tier, exchange="HOSE"):
    b.db.execute("INSERT OR REPLACE INTO symbols VALUES(?,?,?,?,?,?,?)", (symbol, exchange, symbol, "", 0, tier, "t"))
    b.db.commit()


class BackfillTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        while OPEN:
            OPEN.pop().close()           # Windows cannot delete a SQLite file that is still open
        self._tmp.cleanup()

    def count(self, b, table, conn="db"):
        return getattr(b, conn).execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def test_rerun_does_not_duplicate_bars_or_refetch(self):
        src = FakeSource()
        b = new_bf(src, self.tmp)
        add_symbol(b, "AAA", 2)
        b.run(["daily"], [2])
        first = self.count(b, "daily_bars")
        self.assertGreater(first, 1000)
        calls_after_first = len(src.calls)
        b.run(["daily"], [2])                       # cursor is at end date -> nothing to fetch
        self.assertEqual(len(src.calls), calls_after_first)
        self.assertEqual(self.count(b, "daily_bars"), first)

    def test_duplicate_insert_is_ignored(self):
        b = new_bf(FakeSource(), self.tmp)
        df = day_df("2024-01-01", "2024-01-31")
        b._store_daily("AAA", df, {"source": "x"})
        b._store_daily("AAA", df, {"source": "x"})
        self.assertEqual(self.count(b, "daily_bars"), len(df))

    def test_truncated_window_is_split_not_stored(self):
        src = FakeSource(per_day=500)               # 500/day: an 80-day window would need 40,000 > cap
        b = new_bf(src, self.tmp)
        add_symbol(b, "AAA", 1)
        b.do_minute("AAA", 1)
        stored = self.count(b, "bars_1m", "idb")
        jobs = b.db.execute("SELECT win_start, win_end, rows FROM crawl_job WHERE kind='1m' ORDER BY win_start").fetchall()
        self.assertTrue(all(r[2] < bf.TRUNC_ROWS for r in jobs), "a truncated window must never be marked done")
        self.assertEqual(stored, sum(r[2] for r in jobs))
        # windows must be contiguous with no gap or overlap
        for prev, nxt in zip(jobs, jobs[1:]):
            self.assertEqual(dt.date.fromisoformat(prev[1]) + dt.timedelta(days=1), dt.date.fromisoformat(nxt[0]))
        self.assertEqual(jobs[-1][1], TODAY.isoformat())

    def test_empty_windows_widen_and_complete(self):
        src = FakeSource(per_day=0)
        b = new_bf(src, self.tmp)
        add_symbol(b, "THIN", 3, "UPCOM")
        self.assertEqual(b.do_minute("THIN", 3), "done")
        self.assertLessEqual(len(src.calls), 6)     # 480-day then 800-day windows, not hundreds of calls

    def test_resume_continues_after_last_done_window(self):
        src = FakeSource(per_day=100)
        b = new_bf(src, self.tmp)
        add_symbol(b, "AAA", 1)
        self.assertEqual(b.run(["1m"], [1], max_calls=2), 3)
        self.assertEqual(b.calls, 2)
        done = b.db.execute("SELECT MAX(win_end) FROM crawl_job WHERE status='done'").fetchone()[0]
        self.assertLess(done, TODAY.isoformat())
        src2 = FakeSource(per_day=100)
        b2 = new_bf(src2, self.tmp)
        b2.run(["1m"], [1])
        first_call_start = src2.calls[0][2]
        self.assertEqual(first_call_start, (dt.date.fromisoformat(done) + dt.timedelta(days=1)).isoformat())

    def test_quota_limit_waits_then_continues(self):
        waits = []
        src = FakeSource(errors=["VNSTOCK_AUTH_DAILY_LIMIT", None])
        b = new_bf(src, self.tmp, sleep=waits.append, delay=0)
        add_symbol(b, "AAA", 2)
        self.assertEqual(b.do_daily("AAA", 2), "done")
        self.assertIn(b.limit_wait_s, waits)

    def test_quota_limit_forever_stops_the_run(self):
        src = FakeSource(errors=["VNSTOCK_AUTH_DAILY_LIMIT"] * 50)
        b = new_bf(src, self.tmp, limit_max_wait_s=3600)
        add_symbol(b, "AAA", 2)
        self.assertEqual(b.run(["daily"], [2]), 2)
        self.assertEqual(self.count(b, "daily_bars"), 0)

    def test_fatal_error_stops_run(self):
        for code in ("VNSTOCK_RELEASE_EXPIRED", "VNSTOCK_TIER_ROUTE", "VNSTOCK_AUTH_CREDENTIAL_INVALID"):
            with tempfile.TemporaryDirectory() as t:
                b = new_bf(FakeSource(errors=[code]), t)
                add_symbol(b, "AAA", 2)
                add_symbol(b, "BBB", 2)
                self.assertEqual(b.run(["daily"], [2]), 2, code)
                self.assertEqual(self.count(b, "crawl_job"), 0, "no job may be recorded as done after a fatal stop")
                OPEN.pop().close()

    def test_transient_error_fails_symbol_and_moves_on(self):
        src = FakeSource(errors=["NETWORK"] * 4)    # 1 try + 3 retries all fail for the first symbol
        b = new_bf(src, self.tmp)
        add_symbol(b, "AAA", 2)
        add_symbol(b, "BBB", 2)
        self.assertEqual(b.run(["daily"], [2]), 0)
        st = dict(b.db.execute("SELECT symbol, status FROM crawl_job").fetchall())
        self.assertEqual(st, {"AAA": "failed", "BBB": "done"})
        b.run(["daily"], [2])                        # a later run retries the failed symbol
        st = dict(b.db.execute("SELECT symbol, status FROM crawl_job WHERE status='done'").fetchall())
        self.assertEqual(set(st), {"AAA", "BBB"})

    def test_pacing_enforces_delay_between_calls(self):
        waits, clock = [], [0.0]
        b = new_bf(FakeSource(), self.tmp, delay=10, sleep=lambda s: (waits.append(s), clock.__setitem__(0, clock[0] + s)),
                   monotonic=lambda: clock[0])
        add_symbol(b, "AAA", 2)
        add_symbol(b, "BBB", 2)
        b.run(["daily"], [2])
        self.assertEqual(waits, [10])                # first call immediate, second waits the full delay

    def test_delisted_symbol_is_fetched_once(self):
        src = FakeSource()
        b = new_bf(src, self.tmp)
        add_symbol(b, "OLD", 4, "DELISTED")
        b.run(["daily"], [4])
        n = len(src.calls)
        b.run(["daily"], [4])
        self.assertEqual(len(src.calls), n)

    def test_index_is_fetched_in_contiguous_windows(self):
        src = FakeSource()
        b = new_bf(src, self.tmp)
        add_symbol(b, "VNINDEX", 0, "INDEX")
        self.assertEqual(b.do_daily("VNINDEX", 0), "done")
        wins = [(c[2], c[3]) for c in src.calls if c[0] == "daily"]
        self.assertGreater(len(wins), 3)
        self.assertEqual(wins[0][0], bf.DAILY_START)
        self.assertEqual(wins[-1][1], TODAY.isoformat())
        for (a, z), (a2, _) in zip(wins, wins[1:]):
            self.assertEqual(dt.date.fromisoformat(z) + dt.timedelta(days=1), dt.date.fromisoformat(a2))
        for a, z in wins:
            self.assertLessEqual((dt.date.fromisoformat(z) - dt.date.fromisoformat(a)).days + 1, bf.INDEX_WINDOW_DAYS)

    def test_equity_daily_is_a_single_call(self):
        src = FakeSource()
        b = new_bf(src, self.tmp)
        add_symbol(b, "AAA", 2)
        b.do_daily("AAA", 2)
        self.assertEqual(len([c for c in src.calls if c[0] == "daily"]), 1)

    def test_last_complete_session_date(self):
        tz = bf.VN_TZ
        self.assertEqual(bf.last_complete_session_date(dt.datetime(2026, 11, 5, 10, 0, tzinfo=tz)), dt.date(2026, 11, 4))
        self.assertEqual(bf.last_complete_session_date(dt.datetime(2026, 11, 5, 16, 0, tzinfo=tz)), dt.date(2026, 11, 5))

    def test_classify(self):
        self.assertEqual(bf.classify(VnError("VNSTOCK_AUTH_HOURLY_LIMIT")), "limit")
        self.assertEqual(bf.classify(VnError("VNSTOCK_RELEASE_EXPIRED")), "fatal")
        self.assertEqual(bf.classify(ConnectionError("x")), "transient")


if __name__ == "__main__":
    unittest.main()
