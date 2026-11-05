# Swing Trade Scenarios: Rubber Duck and Red Team

## Purpose
Watch LUNR, MNSO, GRRR, URG, LTRX, LCID, NOK and FLNA in addition to the original five. Show *conditional* entry/invalidation/target prices for a research scenario, not validated trading instructions.

## Rubber-duck calculation
Given the last 21+ completed split-consistent RAW daily OHLCV sessions:
- ATR14 = Wilder smoothing of true range, where TR = max(H-L, abs(H-previous_close), abs(L-previous_close)).
- H20 = highest high of the last 20 fully completed daily sessions.
- Conditional entry = one cent above H20, rounded up to a cent.
- Stop scenario = entry minus 1.5 ATR14, rounded down to a cent.
- R = entry - stop. Hypothetical take-profit prices = entry + 2R, entry + 3R.
- Skip if opening market price is higher than entry + 0.5 ATR14. Recalculate after each completed session.
- Historical regime, commission, spread, slippage, earnings and overnight gaps are NOT validated here. A stop cannot guarantee a fill.
- Default abstention: price below USD 5, 20-session daily dollar-turnover proxy below USD 2 million, stop distance above 15% of entry, invalid data, recent split, or stale data.
- 1–5 subsequent trading sessions is the *research horizon*; a real trading signal would also require intraday quotes, a licensed venue feed, and a validated edge.

Synthetic 35-session illustration: close USD 10.00, high USD 10.50, low USD 9.50, volume 300,000/day. ATR=1.00, H20=10.50, conditional entry=10.51, stop=9.01, 2R target=13.51, 3R target=15.01, gap-skip threshold=11.01. This arithmetic is not evidence of successful trades.

## Identity and market exceptions
- NASDAQ LUNR is Intuitive Machines; TSX LUNR is an unrelated company. Source/exchange must be explicit.
- FLNA is Filana Therapeutics, formerly SAVA (March 11, 2026 symbol change). The company also disclosed Nasdaq minimum-bid noncompliance in September 2026.
- URG and FLNA were below USD 1 on November 4, 2026. Both remain visible but fail the default USD 5 research floor.
- MNSO and NOK are ADRs; issuer/market listing must be preserved. Do not confuse ADR share ratios with primary-listed shares.

## Red-team attack tests
| Case | Attack | Required behavior |
|---|---|---|
| TP-01 | LUNR confused with TSX stock | Reject false identity |
| TP-02 | FLNA alias SAVA causes corporate-action mismatch | Use effective-date identity |
| TP-03 | FLNA/URG penny-stock risk hidden | Visible exclusion, no default dollar levels |
| TP-04 | Future intraday high used as completed bar | Exclude unclosed session |
| TP-05 | Last 20-day high computed with future session | Reject look-ahead |
| TP-06 | Split in past 21 days | Block scenario |
| TP-07 | ATR zero/missing/NaN | Abstain |
| TP-08 | High lower than close or low higher than close | Reject malformed OHLC |
| TP-09 | Thin market: ADV looks fine but spread is wide | Never certify executable edge |
| TP-10 | Price gaps above entry+0.5ATR | Skip breakout rather than chase |
| TP-11 | Overnight stop gap below stop | Do not pretend stop is guaranteed |
| TP-12 | ATR distance more than 15% of entry | Abstain |
| TP-13 | Arbitrary 2R/3R presented as forecast | Label research-only and unvalidated |
| TP-14 | Market-data vendor prohibits redistribution | Keep public price levels blank |
| TP-15 | Browser calculator uploads broker inputs | No network request or storage |
| TP-16 | Existing technical 200-day history absent | Keep symbol visible, independent plan status |
| TP-17 | Public website shows unauthorized exact levels in HTML | Integration test rejects leakage |
| TP-18 | 20-day volume treated as current order-book depth | Label liquidity proxy, not execution proof |
| TP-19 | Stale source data generates active trade instruction | Expire plan, no live indication |
| TP-20 | Price changes tomorrow but target remains static | Recalculate levels after completed close |

## First implementation
- Public GitHub Pages: show all 13 symbols, screening/abstention statuses, a calculation policy and a browser-only tool from *user supplied broker price/ATR/volume*.
- Personal local report: run python private_trade_report.py; outputs a gitignored private_reports CSV with exact conditional price levels and a research-only label. Never upload personal output as Pages artifact or Git commit.
- Do not publish Yahoo/YFinance market quotes or derived numerical levels without verifying redistribution rights. Yahoo's official help states the information cannot be redistributed.
- No user-account connection, no automatic broker orders, and no claim of profitable after-cost expectancy.

## Sources
- Yahoo data restrictions: https://help.yahoo.com/kb/SLN2310.html
- Filana SEC filing and Nasdaq minimum price notice: https://www.sec.gov/Archives/edgar/data/1069530/000143774926030751/sava20260918_8k.htm
- Filana ticker change: https://www.sec.gov/Archives/edgar/data/1069530/000143774926007422/ex_930540.htm
- Existing approved quant/01_MARKET_MATH.md and quant/04_EXECUTION_COSTS.md.
