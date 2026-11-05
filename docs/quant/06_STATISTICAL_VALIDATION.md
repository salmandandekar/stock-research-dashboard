# Quantitative Standards — Statistical Validation, Probability and Model Risk (v1.3)

**Thesis:** Correct accounting and profitable-looking charts are insufficient. Only strictly out-of-sample evidence after costs can support a *conditional* claim of historical net edge. No measured alpha is assumed.

| ID | Calculated measure and formula | Required controls |
|---|---|---|
| QF-S01 | Null H0: E[net return or PnL per qualified *realizable* event] <= 0; stronger incremental H0: E[net edge over preregistered matched simple baseline] <= 0 | Define precise event unit, horizon, actual fill policy, price adjustment, trade size/capacity, market universe and risk. Separate effect size from p-value. |
| QF-S02 | Naive mean standard error = sample_sd(x)/sqrt(n) **only for independent data** | Use trading-day/issuer/event clustered standard errors, time-block bootstrap or Newey–West/HAC when appropriate. Document cluster assumptions and lag/block length. |
| QF-S03 | Bootstrap interval for parameter theta: [empirical quantile alpha/2, empirical quantile 1-alpha/2] of theta from block resamples | Predefine resampling units; present effective #clusters and percentile/BCa/studentized choice, seed and iterations; ordinary independent trade bootstrap disallowed for overlapping same-day positions. |
| QF-S04 | Binary event Brier = mean((p_i-y_i)^2) for y∈{0,1} and p∈[0,1]; binary logloss = -mean(y ln p +(1-y)ln(1-p)) with numerical epsilon guard | Probability must define event, decision timestamp, H, and conditional tradability; probability model calibrated **out-of-sample**; show calibration plot, Brier vs base-rate forecast, confidence and sample. |
| QF-S05 | Net expectancy = mean(realized_net_PnL or correctly normalized return) of executed eligible observations; report bootstrap interval and negative 5% tail | Profitability can't be inferred from price-movement magnitude, net score or high win rate. Include NO_TRADE/NO_FILL separately. |
| QF-S06 | Cost stress: recompute full simulator at baseline, 2x and 3x variable cost (spreads, latency, impact, fees where scalable) | Quoted spread already embedded in fills must not be subtracted again. If 2x wipes edge, mark fragile; stress gaps and partial fills separately. |
| QF-S07 | Walk-forward: chronological train-validation-test and locked final holdout. For overlapping H-event labels, purge train events whose `end` intersects validation start; embargo additional period as defined | Every raw source `available_at <= decision_at`. Optimize only on train/validation. Never reuse final holdout to select parameters. |
| QF-S08 | Trial register records all tested variants, features, weights, thresholds, losses and compute date. Where appropriate compute Deflated Sharpe Ratio (DSR), Probability of Backtest Overfitting (PBO) or multiple-test control | These methods have assumptions and do NOT certify a trading edge. Do not run 1,000 trials then report winner's nominal p<0.05. |
| QF-S09 | Probability calibration: report reliability bins (empirical frequency vs predicted confidence) and Brier/logloss; forecast value tested against constant base rate and simple model | A research "confidence" label cannot be marketed as chance of profit without forecast-calibration evidence. |
| QF-S10 | Tail risk: VaR/ES, max drawdown, event-loss concentration, skew/kurtosis and gap scenarios across training and held-out data | 95% wins can still have negative expected returns because 5% outsized losses. |
| QF-S11 | Regime robustness: prespecified subsamples by time, volume, volatility, market direction, earnings/news events, cap size and sector | An effect driven by one exceptional year or crowded sector must not be presented as generally transferable. |
| QF-S12 | Nested experiment: strategy developer registers proposed filters and multiple comparison correction ahead of data; independent reviewer evaluates untouched holdout | Thresholds must be frozen and checksums saved. Record use of external foundation/model priors. |
| QF-S13 | Cross-sectional ranking comparison: rank correlation and top-decile realized **after-cost** outcomes versus sector/size/volatility-matched baselines | Evaluate sorted portfolios with execution capacity and overlapping dates; no claims from retrospective high-low screenshots. |
| QF-S14 | Prospective paper log: strategy/version, signal time, available_at, fill model, actual later quotes, expiry, no-fill, cancellation, manual override and realized outcome | Minimum 60 sessions and 200 sufficiently independent outcomes is *planning threshold*, not statistical power proof; do not generate trades to hit minimum. |
| QF-S15 | Operational drift: moving net PnL per signal, costs, fill rate, data coverage, forecast calibration, rank volatility, downside events, missingness | Register warning/suspend thresholds before deployment; preserve old scores and loss days. |
| QF-S16 | Benchmark/counterfactual: cash/no-trade, low-turnover EOD strategy, sector-matched signals, matched-liquidity/volatility random strategy and broad market portfolio | Same dates, stock universe, cost assumptions, executable clock, and capital constraints; prefer simpler strategy when advanced model cannot show economically relevant increment. |
| QF-S17 | Confidence intervals around Sharpe/return account for skew, kurtosis and serial dependence; expose sample/assumption | A large daily Sharpe from one unusually profitable date is not proof. Naive sqrt(252) may overstate Sharpe when serial correlation exists. |
| QF-S18 | Cross-validation grouping must keep correlated share classes, event clusters and multiple symbols from same issuer out of conflicting folds as appropriate | Same earnings event leaking across train and validation produces spurious model quality. |
| QF-S19 | For a claim "beats S&P 500", compare **portfolio** TWR with S&P 500 total-return benchmark over identical full calendar, including idle cash and realistic costs | High median per-trade return with sparse exposure is not necessarily benchmark outperformance. |
| QF-S20 | Every published model status `EXPLORATORY | UNVALIDATED | HISTORICALLY_VALIDATED | PAPER_TRACKING | SUSPENDED` has explicit evidence gate and expiry | A historically validated claim cannot be treated as a live predictable profit guarantee. |

**Key steelman insight:** The product may still provide value if predictive alpha is absent, by preventing mathematically invalid trades, making risks and assumptions visible, reducing research time and tracking "No Trade" days. A false 80% success probability is less useful than an accurate lack-of-evidence label.

**Gold counterexample:** gross wins +1.5% (55% of filled cases), gross losses -2% (45%), mean trading costs 0.15% of entry notional => expected **net = -0.225% per filled trade**. This cannot be called profitable even though win rate is greater than half.

**Statistical source references:**
- Andrew Lo, *The Statistics of Sharpe Ratios*: https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios
- Bailey et al., *The Probability of Backtest Overfitting*: https://escholarship.org/uc/item/4w1110bb
- Bailey and Lopez de Prado, *The Deflated Sharpe Ratio*: https://doi.org/10.3905/jpm.2014.40.5.094
- Harvey, Liu and Zhu, cross-section of expected returns: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2513152
- Proper Scoring Rules 2026 review: https://doi.org/10.1146/annurev-statistics-042424-050626
- Kenneth French factors: https://mba.tuck.dartmouth.edu/pages/faculty/Ken.french/Data_Library/f-f_factors.html

**Mandatory statistical stop:** If sample/regime/cost evidence is inadequate, model status = UNVALIDATED or SUSPENDED. If low-level risks, source license or PIT integrity are unknown, NO_TRADE rather than suggested purchase. No "optimal" or "best returns" claim can follow from an uncorrected historical search.
