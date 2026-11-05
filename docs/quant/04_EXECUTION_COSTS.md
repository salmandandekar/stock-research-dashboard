# Quantitative Standards — Short-Term Execution, Fill and Cost Models (v1.3)

**Critical principle:** volatility and theoretical spread-adjusted movement do not establish profitable executable trades. This module defines research simulation only. No account-specific position size, leverage, short sales, auto-orders or brokerage credentials.

| ID | Mathematical specification | Guard |
|---|---|---|
| QF-T01 | For long q>0 shares: entry_cash=q×p_buy_exec+fees_buy; exit_cash=q×p_sell_exec-fees_sell; net_PnL=exit_cash-entry_cash+cash_dividends-funding; net_ROI=net_PnL/entry_cash | Buy fill from actual quote/ask-side order-book or conservative model; sell from bid-side; no dividend double count. Quote prices already include spread crossing. |
| QF-T02 | If starting from midpoint: estimated_buy=mid_entry + half_spread_entry + separately modeled buy_impact; estimated_sell=mid_exit - half_spread_exit - separately modeled sell_impact | Choose this OR quote-execution method. Do NOT subtract another full spread after filling at bid/ask. |
| QF-T03 | Mid-price move=(mid_exit/mid_entry)-1; model approximate net move=mid_move - all incremental cost_fraction | Ranking approximation only; exact cashflow-based net PnL is authoritative. |
| QF-T04 | Gross outcome expectancy E[gross return]=p_win×mean(gross_win) - p_loss×mean(abs(gross_loss)); net expectation=E[gross]-mean(full_roundtrip_cost_fraction) | Include zero/flat group when appropriate. If winners/losers already NET, do NOT subtract costs again. |
| QF-T05 | Probability-weighted opportunity E[PnL/signal]=p_fill×E[PnL|filled]+(1-p_fill)×PnL_if_unfilled | Conditional price and adverse selection differ when filled; no-fills recorded, not omitted from signal quality. |
| QF-T06 | Feasible q <= min(quote_depth_bound, time_slot_volume×participation_cap, platform research cap) | No hypothetical full-size fills of thin books; average daily dollar volume not instant depth. |
| QF-T07 | R multiple = net_trade_PnL / modeled_initial_risk_budget; ratio target_reward/downside_risk valid only for positive planned initial downside | Stop can gap; do not treat stop price as guaranteed realized exit. |
| QF-T08 | Overnight gap r_gap=(next_session_open/prior_close)-1 | Swing exit/stop sim at next EXECUTABLE quote or worse; never guarantee stop level after overnight gap. |
| QF-T09 | If target and stop both crossed within OHLC bar and no event sequence: AMBIGUOUS_EXECUTION | Use tick/quote sequence OR predetermined worst-case sensitivity; never infer winning first path. |
| QF-T10 | Total costs = commission + exchange/regulatory fees + spread_cost_IF_NOT_ALREADY_IN_QUOTES + market_impact + time_slippage + funding | Cost lines individually versioned, side-specific, session- and liquidity-dependent. Zero-commission never implies cost-free. |
| QF-T11 | Open long mark-to-market PnL = q×(declared_mark - average_entry) less hypothetical liquidation cost, with lot-based realized PnL separate | Last trade/midquote/bid not interchangeable. Unrealized midquote profit cannot be called executable profit. |
| QF-T12 | Return quantile and predicted gain/loss: report empirical conditional 5/50/95% quantiles plus sample and uncertainty, if justified by untouched test | Otherwise prediction unavailable; positive point estimate never means guaranteed return. |
| QF-T13 | Cost robustness evaluate C base, 2×base and 3×base; vary spread, latency, size and slippage separately | Do not scale fixed fees incorrectly or compound a cost already embedded in quoted fill. |
| QF-T14 | For hypothetical spread quoted bid=100.00 ask=100.20, immediate sell at bid after buy at ask yields return 100/100.2-1 ≈ -0.1996008% before fees | Assert the negative value even if midprice unchanged; prevents profit from crossing spread twice. |
| QF-T15 | Latency_t = fill_eligibility_timestamp - signal_timestamp; expiry_t < actual_available_timestamp => EXPIRED | "Enter now" prohibited from delayed or stale feed. Feature availability precedes decision, decision precedes fill. |
| QF-T16 | Net directional edge in basis points = estimated gross move bps - executable cost bps; economic qualification requires credible positive OOS net advantage with risk and uncertainty | Do not call +50bps target -70bps cost profitable. Rare severe losses can dominate. |
| QF-T17 | Fill PnL of partial order = SUM_lots(filled_shares_i×executed_price_i) - matched entry basis - each accrued cost | Unfilled remainder ignored for realized profit but counted in rejection/coverage; no naive whole-order fill. |
| QF-T18 | Market participation = shares_executed / eligible_contemporaneous_traded_volume; impact is price- and size-dependent | Constant slippage may be inadequate; different regime/market cap effects tested. |
| QF-T19 | Research signal expires at registered horizon cutoff and stops ranking after expiration or market halt. All alerts include source and generation times. | Session calendars include NYSE regular market, early close and DST. |
| QF-T20 | PnL is calculated at **executed** price; chart return at adjusted/historical close is **not** realized return. | Simulated fills always use raw contemporaneous, executable quote/trade price with corporate action adjustments handled in ledger. |

**Synthetic executable fixture:** buy 100 shares at USD 100.10 and sell at USD 101.20, USD 1 fee on each side. Entry cash = USD 10,011.00, exit cash = USD 10,119.00. Net PnL = USD 108.00. Net return on entry cash = 108/10011 = 0.01078813305 = **1.0788133%**. A model that subtracts spread again or uses 100.65 midpoint is wrong for this fixture.

**Negative expectancy fixture:** conditional gross wins +1.5% in 55% of filled cases, gross losses -2% in 45%, and mean roundtrip cost .15% -> net E=0.55×1.5%-0.45×2%-0.15%= **-0.225%**. The high win rate does not imply profit.

**Market-data critical limit:** Alpaca docs distinguish IEX single-venue live from SIP consolidated coverage. Free recent SIP history access and realtime subscription differ. A one-minute bar without quotations/queue data is not sufficient to certify executable limit fills.

**Sources:** https://docs.alpaca.markets/us/docs/market-data-faq ; https://github.com/mementum/backtrader/blob/master/backtrader/strategy.py ; https://www.sec.gov/about/reports-publications/investorpubsdaytipshtm

**Required error states:** NO_TRADE, NOT_VALIDATED, DATA_STALE, LIMITED_FEED, UNLICENSED_FEED, AMBIGUOUS_EXECUTION, EXPIRED, PARTIAL_FILL, MARKET_HALTED, INSUFFICIENT_DEPTH. Never convert such states to positive signals.
