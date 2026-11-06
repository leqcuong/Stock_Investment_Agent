# Fit note — Graham, *The Intelligent Investor* (rev. ed., Zweig commentary)

Source file: `research/The Intelligent Investor - BENJAMIN GRAHAM.pdf` (641 pp.).
Read for this note: front matter and contents, Introduction, Ch. 14, Ch. 15 (screening and net-current-asset sections), Ch. 8 (Mr. Market), and searches for forecasting/technical passages. **Not read in full.** Page numbers below are book pages from the contents list.

## Verdict by track

| Track | Fit | Use |
| --- | --- | --- |
| R07 Vietnamese financials | **High** | Source of a screening catalog (below) and EPS-quality warnings (Ch. 12). |
| R06 Technical features / baseline | Low, opposing | Introduction (p. 2) rejects chart/momentum rules. Use only as an optional *value/quality comparator*. It is a 1973 US text, so it does **not** count toward R06's "≥ 8 Vietnam-relevant papers". |
| R08 ML methodology | Low | Only the principle of simple, pre-stated criteria. Ch. 15 also shows an equal-weight test that lagged the cap-weighted index. |
| R10 Risk sizing / accounting | Very low | Ch. 4 is asset allocation (stock/bond split), not per-position sizing or return accounting. "Margin of safety" (Ch. 20) is a concept only. |
| R01–R05, R09, R11 | None | |

## Screening catalog from Ch. 14 / Ch. 15 → R07 metric catalog input

Graham's thresholds are US, 1970s and for industrial/utility companies. They are **reference formulas, not Vietnam-calibrated limits**. Banks, securities firms and insurers need their own treatment (R07 question 4).

"Data now" means what the project holds or is known to expose. It is not a test of vnstock fundamentals output, which nobody has probed yet.

| # | Graham criterion (defensive, Ch. 14) | Inputs | Data now |
| --- | --- | --- | --- |
| 1 | Adequate size (sales ≥ US$100M industrial) | revenue | Revenue available, but needs a VND threshold chosen from VN data (R06 Q3 / R07). |
| 2a | Current ratio ≥ 2 | current assets, current liabilities | Balance sheet, last periods only. |
| 2b | Long-term debt ≤ net working capital | long-term debt, current assets − current liabilities | Balance sheet, last periods only. |
| 3 | Positive earnings in each of 10 years | annual net income × 10 | **Not computable**: about 8 periods exposed. |
| 4 | Dividends uninterrupted 20 years | dividend history × 20 | **Not computable**: depth unknown; corporate actions are not crawled yet. |
| 5 | EPS growth ≥ 1/3 over 10 years (3-yr averages) | EPS × 10 years | **Not computable** (same depth limit). |
| 6 | Price ≤ 15 × 3-year average EPS | price, EPS × 3 years | Price yes. Needs ≥ 12 quarters, but only about 8 are exposed, so use TTM P/E instead and label it. |
| 7 | Price ≤ 1.5 × book value; P/E × P/B ≤ 22.5 | price, equity, shares | Possible. Treat shares-outstanding and EPS basis as an R07 trap (dilution, unit). |

Enterprising screen (Ch. 15, p. 385–386): current ratio ≥ 1.5, debt ≤ 110% of net current assets, no deficit in 5 years, some dividend, EPS above 5 years earlier, price < 120% of net tangible assets, plus low P/E (≤ 9 in 1970). Same depth problem for the 5-year tests.

Net-current-asset ("net-net") stocks (Ch. 15, p. 390–391): price below current assets minus **all** liabilities, fixed assets counted as zero. Computable from one balance sheet. Graham notes the strategy worked in 1923–57 except 1930–32, and needs a diversified basket. Zweig's footnote warns that very low-priced stocks cost a lot to trade and often fail, which matters for a thin, price-limited market.

## Cautions for use

1. **Display only.** Any score built from this is a Phase 1 financial summary (A06/A07), not a model feature, unless R07 establishes publication dates (§8.2).
2. **Look-ahead.** The quarter-end date is not the publication date. `Fundamental.equity.filing` (source CAFEF) may carry filing dates. That is **unverified**, and R02 recorded no statement publication dates for the Community tier. R07 should test it before anyone relies on either claim.
3. **Valuation on distorted bases.** Use cumulative-vs-standalone, consolidated-vs-parent and negative-base rules from the R07 spec; return `N/A` with a reason code.
4. **Price basis.** Our stored prices are split-adjusted and in thousand VND. Book value per share and EPS from statements must be put on the same share basis before P/B or P/E.

## Suggested next use

Hand this note to the R07 agent as an input, with the instruction to (a) probe what `Fundamental.equity.*` really returns for 10 sample tickers (depth, units, consolidated flag, dates), then (b) mark each row above computable, partial or impossible.
