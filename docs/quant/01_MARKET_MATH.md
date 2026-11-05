# Quantitative Standards — Contracts and Market Calculations (QFCS v1.3)
Date: 2026-11-04. Normative design; neither executable implementation nor tested investment alpha.
Applies to all current stock-intelligence versions v1.0–v1.2a.
**Every formula requires:** ID and version, input identifiers, data source, allowed license/use, units/currency, dates (market/available/fetched), time zone, frequency/window, adjustment basis, precision, denominator policy, absent-data behavior, sector applicability, confidence, code SHA, exact test vector, and provenance. Version calculations. Never silently change past results.

**Conventions:** returns are fractional (0.01 = 1%); bps = fraction × 10,000; currency amounts use Decimal/fixed point; sample standard deviation uses ddof=1; UTC event order; exchange IANA local calendar; all signal inputs available before decision. No future-restated data.

| ID | Required equation or numerical definition | Critical guards |
|---|---|---|
| QF-M01 | Price return r = P(t)/P(t-1) - 1 | P(t-1)>0; price-only, not dividend total return |
| QF-M02 | Holding total return = (P1_same_share_units + cash_dividends_same_units - P0_same_units)/P0_same_units | Split adjustments consistent; NEVER dividend twice on a dividend-adjusted series; distinguish cash dividend and reinvestment |
| QF-M03 | log return = ln(1+r) | requires r>-1; not a simple percent profit |
| QF-M04 | Cumulative simple return = PRODUCT(1+r_t)-1 | geometric chaining, not sum of percentage returns |
| QF-M05 | Session return volatility = sample_sd(returns) × sqrt(252) | scaling descriptive, not always valid confidence measure with serial correlation |
| QF-M06 | SMA(n) = SUM(P_t-i, i=0..n-1)/n | exactly n valid completed points |
| QF-M07 | EMA_t = alpha P_t+(1-alpha) EMA_(t-1), alpha=2/(n+1) | seed at initial n-point SMA; disclose warm-up |
| QF-M08 | Momentum(h) = P_t/P_(t-h)-1; relative momentum = (1+R_stock)/(1+R_benchmark)-1 | same horizon and total-return convention; 63/126/252 session examples |
| QF-M09 | True range = max(H-L, abs(H-Cprev), abs(L-Cprev)); ATR(n) Wilder smoother alpha=1/n | previous close and adjustment semantics must match |
| QF-M10 | RSI = 100-100/(1+Wilder_avg_up/Wilder_avg_down) | both 0 => 50; only up => 100; only down => 0; seed and n documented |
| QF-M11 | Drawdown_t=1-V_t/max(V_s for s<=t); max drawdown=max_t Drawdown_t | wealth series must include dividends/costs if used for actual portfolio risk; drawdown is positive magnitude |
| QF-M12 | Relative intraday volume = cumulative volume until minute m today / median prior d sessions volume until *same minute m* | align session/DST/early-close; do NOT compare 10-min volume with full-day ADV |
| QF-M13 | VWAP = SUM(trade_price × traded_shares) / SUM(traded_shares) | exact trades, valid venue and trade flags; OHLC typical price is only a proxy |
| QF-M14 | Dollar ADV(n) = mean of daily traded notional (sum trade price × shares), alternatively mean(close × shares) explicitly labeled proxy | n completed sessions, corporate actions and feed coverage |
| QF-M15 | Midquote=(bid+ask)/2; spread_bps=10,000(ask-bid)/mid; half-spread=(ask-bid)/(2mid) | ask>=bid>0, quote not stale, depth and venue known |
| QF-M16 | Gap_t=Open_t/Close_(t-1)-1; range=(High-Low)/Open | split consistent, regular vs extended hours separate |
| QF-M17 | Beta = cov(stock_excess_returns,market_excess_returns)/var(market_excess_returns) | matched dates; variance>0; choose benchmark, risk-free convention and window |
| QF-M18 | If y is EFFECTIVE annual yield, rf_day=(1+y)^(1/365.25)-1 | Treasury bill bank-discount yield is NOT an effective yield; convert using maturity/day count first |
| QF-M19 | Log-spread, liquidity imbalance, stock-v-sector return must explicitly identify whether quotes/trades are SIP/IEX or other venues | no market-wide claims from limited venue coverage |
| QF-M20 | Total-return factor and split-only factor must be independent from raw executable OHLC prices | never fill trades on restated adjusted price; record corporate-action event and effective date |

Mandatory negative tests: split at 2:1, ex-dividend day, 15-minute delayed feed, crossed market, zero shares, missing historical bar, holiday and time-zone crossover, reverse split, stale VWAP, tied peer values.

**Source register:** SEC XBRL APIs https://www.sec.gov/search-filings/edgar-application-programming-interfaces ; Alpaca feed semantics https://docs.alpaca.markets/us/docs/market-data-faq ; CFA performance https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation ; Lo on autocorrelation https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios

**Release rule:** No formula output can become a research candidate unless inputs, timing, adjustment, data rights, tests and applicability are validated. Missing data means NO_TRADE or INSUFFICIENT_EVIDENCE, not zero.
