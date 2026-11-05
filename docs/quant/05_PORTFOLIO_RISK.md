# Quantitative Standards — Portfolio Performance, Attribution and Risk (v1.3)

**Interpretation:** Individual trade returns, a simulated capital-constrained strategy's returns, and an investor's own portfolio returns are different measures. Personal account balances are not allowed on public Pages.

| ID | Required equation/contract | Guard |
|---|---|---|
| QF-B01 | For **period-end** external net cashflow only, subperiod r=(NAV_end - external_flow_end)/NAV_start - 1. With cashflows **inside** period, revalue at each flow and chain time-weighted return TWR=PRODUCT(1+r_j)-1 | External deposits are not performance. Never use period-end formula for arbitrary intraperiod deposits. |
| QF-B02 | CAGR=(end_wealth/start_wealth)^(365.25/calendar_days)-1 for coherent cashflow-adjusted positive wealth series | Portfolio inflows require TWR, or money-weighted XIRR reported separately. Years and calendar basis explicit. |
| QF-B03 | XIRR solves SUM_i(CF_i/(1+r)^((date_i-date0)/365.25))=0 with external contribution sign defined | May have multiple/no roots; reject incomparable portfolios and nonconvergent roots. |
| QF-B04 | Daily Sharpe = mean(r_strategy-rf_daily)/sample_sd(r_strategy-rf_daily)×sqrt(252) | iid annualization simplification; serial correlation requires separate adjustment, possible HAC/Lo method. sd=0 is undefined, not ∞. |
| QF-B05 | Sortino = (mean(r_daily)-target_daily)/sqrt(mean(min(0,r_daily-target_daily)^2))×sqrt(252) | Defines *full-sample* downside deviation; identify target return and frequency, sd=0 => undefined. |
| QF-B06 | Drawdown_t=1-NAV_t/max_{s<=t}NAV_s; MDD=max(drawdown_t); duration counts trading sessions underwater, right-censor current | Include open periods, dividends, borrow if permitted, fees and cash. Stop prices do not cap realized drawdown. |
| QF-B07 | Historical return VaR95= -quantile_0.05(r_t); empirical ES95=-mean(lowest 5% left-tail returns), with tie/fractional-tail convention registered | Return or USD units, rolling window and minimum sample specified. These are risk estimates, not worst possible losses. |
| QF-B08 | Win rate = wins/(wins+losses), flats/unfilled explicitly counted separately. Profit factor = sum(positive_net_PnL)/abs(sum(negative_net_PnL)) | Zero losses makes profit factor undefined; never infinity or "guaranteed". |
| QF-B09 | Two-sided notional turnover=sum(abs(executed_trade_notional))/average_NAV, alternatively one-way turnover=min(buys,sells)/average_NAV | Different convention must be identified. No ROI from average trade unless capital occupancy modeled. |
| QF-B10 | Tracking error = sample_sd(r_strategy-r_benchmark)×sqrt(252); information ratio=mean(active_return)/sample_sd(active_return)×sqrt(252) | Daily return calendars matched, benchmark total returns and costs comparable; autocorrelation caveat. |
| QF-B11 | Alpha from regression (r_strategy-rf)=alpha+beta(r_market-rf)+error; report estimate, p-value/CI with dependence-aware SE | No claim of causal alpha or skill from significant intercept alone. Consistent daily vs annual units. |
| QF-B12 | NAV_t = cash_t + SUM_i(shares_i×mark_price_i)+receivables-payables-accrued_fees | Correct share splits, dividends, executions, transaction fees, unsettled amounts and restricted cash; no overdrawn cash unless financing explicitly modeled. |
| QF-B13 | Average net expectancy per executed trade = SUM_i(net_PnL_i)/n_filled; per signal includes no fills/abstentions by documented policy | Not a portfolio return. Cannot multiply mean per-trade ROI by #trades/year to infer compounded CAGR. |
| QF-B14 | Excess portfolio factor exposures: time-series model of market, size, value, profitability, momentum and other preregistered factors | As-of factor vintage, matched dates, full covariance; unexplained beta exposures do not establish independent stock-picking edge. |
| QF-B15 | For overlapping intraday/swing signals, calculate daily **capital constrained portfolio NAV** first; use NAV returns for annualized risk | Trades sharing event/time/sector not independent. Avoid sqrt(number_of_trades) Sharpe calculation. |
| QF-B16 | Payoff ratio=mean(positive_net_PnL)/abs(mean(negative_net_PnL)); average holding time and capital utilization are separate metrics | Reject denominator 0 and tiny sample; don't confuse gross and net profit distributions. |
| QF-B17 | Conditional exposures: fraction of capital in sector/issuer and rolling covariance / correlation at portfolio mark time | Market concentration warnings across technology-heavy candidates; no portfolio personalization on public research site. |
| QF-B18 | Stress scenarios: shock portfolio revalue with registered price, vol, spread, correlation and overnight gap assumptions; stress PnL=stressed_NAV-current_NAV | Scenario assumptions not predicted likelihood or guaranteed stress boundary. |
| QF-B19 | Downside quantile in USD = risk_quantile_return × time-consistent exposure notional; define whether compounded returns | Avoid treating 1-day VaR as 5-day VaR by naive sqrt without distribution/serial assumptions. |
| QF-B20 | Portfolio benchmark total-return sequence must match daily timestamps, currency, reinvested distributions and cash conventions | Zero-trade reference includes cash risk-free (if known), not automatically zero economic opportunity cost. |

**Synthetic NAV fixture:** values 100→110→99→120→90→115 (no deposits/withdrawals), max drawdown magnitude = (120-90)/120 = **25%**. A final-period recovery does not erase historical MDD.
**Synthetic TWR fixture:** first period +10%, second -5%, compounded = 1.10×0.95-1 = **+4.5%**, not +5%.
**Dividend fixture:** unadjusted price 100→105, one cash dividend of 1 per original-share unit => holding total return **6%**, price-only 5%. If adjusted total-return price series already includes the dividend, do NOT add the dividend again.

**Benchmark controls:** cash/no-trade, total-return broad market, sector/time matched and size/factor matched; same tradable universe, evaluation clock, fees, liquidity assumptions and risk-free source. Report absolute and benchmark-relative results; preserve all losing outcomes and delistings.

**References:** CFA portfolio performance https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation ; GIPS handbook https://www.gipsstandards.org/standards/gips-standards-for-firms/gips-standards-handbook-for-firms/ ; Andrew Lo, Statistics of Sharpe Ratios https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios ; CFA expected shortfall https://www.cfainstitute.org/sites/default/files/-/media/documents/book/rf-lit-review/2009/rflr-v4-n1-1-pdf.pdf

**Review bar:** Show trade PnL and portfolio NAV side by side; a seemingly profitable list of "top trades" without capital budget, trading costs, unfilled orders and no-trade days is NOT an acceptable performance result.
