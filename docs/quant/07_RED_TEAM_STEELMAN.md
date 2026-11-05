# Quantitative Adversarial Review — Calculation Safety and Steelman Loops (v1.3)
**Review date:** 2026-11-04. **Status:** design-level audit. Test cases are proposed, NOT executed. Human expert signoffs NOT performed.

## A. Socratic audit of the entire v1.2a requirements baseline
The merged baseline has source identity, SEC facts, valuation, strategy scoring, risk management, performance, backtest, intraday latency, cost awareness, legal safeguards, AI read-only and market-wide discovery. The missing element is **a normative, reproducible, complete arithmetic contract**. Terms like "profitability", "fair value", "expected return", "risk", "confidence", "margin" and "volatility" can be implemented several incompatible ways.

| Requirement family | Existing intent | Critical mathematical gap resolved in v1.3 |
|---|---|---|
| Company / SEC | source history and financial quality | YTD vs discrete quarters; statement signs; NI/EBIT/NOPAT; fair fiscal comparability; diluted shares |
| Market price | momentum and trends | raw vs split-adjusted vs dividend-adjusted vs total return; quote clocks, bid/ask and venue |
| Valuation | scenarios and discounted cash flows | FCFF vs FCFE discount basis, terminal growth stability, EV-to-equity bridge, reverse DCF root validation |
| Opportunity discovery | stock selection | distinguishing movement magnitude from positive conditional net expectancy |
| Execution | slippage and fees | quoted fill vs midpoint and spread double-count; next available execution, partial/unfilled, ambiguous OHLC paths |
| Strategy | historical tests and constraints | capital-constrained portfolio NAV vs arithmetic mean trade win, turnover and overnight gaps |
| Risk | downside and volatility | drawdown, VaR/ES tail, serial dependence, currency and horizon alignment |
| Statistical model | OOS confidence | multiple-testing log, clustered errors, probability calibration, uncertainty and simpler counterfactuals |
| AI | grounded explanation | numerical claims must reference immutable formula result and exact units, never compute or revise amounts without engine |
| Public website | research cards | time/venue/license status, distinction of cashflow outcomes from projections and not-yet-validated status |

## B. Repeated steelman loops — strongest design, strongest contradiction, correction
**Loop 1 — Deterministic mathematics.** The strongest case for financial automation is consistent arithmetic across hundreds of securities. Contradiction: invalid denominators, negative share equity and incompatible XBRL fiscal periods can create high-confidence nonsense. Correction: formula registry, typed metric contracts, reference vectors, accounting reconciliations and fail-closed statuses. **Exit:** all critical mathematical domain states have tests and documented formulas.

**Loop 2 — Executable economics.** The strongest case for intraday discovery is finding occasional short-lived, conditional opportunities. Contradiction: bid–ask spread, time delay, partial fills, stale quotes and queue competition can remove the edge. Correction: separate theoretical price return from actual filled cashflows and report strategy-level net edge at 1x/2x/3x cost. **Exit:** no high-return claim can bypass fill and liquidity modeling.

**Loop 3 — Valuation uncertainty.** The strongest case for fundamentals is buying good businesses with a valuation buffer. Contradiction: WACC, terminal growth, dilution, debt/cash and working capital assumptions can overwhelm the fair value. Correction: coherent FCFF-to-EV-to-equity equation; reverse DCF, scenario sensitivity, terminal-value share and exclusion when model invalid. **Exit:** valuation must show scenarios/assumptions instead of one authoritative price.

**Loop 4 — Statistical credibility.** Strongest case: a research strategy can be falsified on unseen data. Contradiction: selected best model out of hundreds, current survivors, repeated holdout access and cross-correlated names can fabricate positive significance. Correction: immutable experiment register, point-in-time history, fixed holdout, clustered inference, multiple-testing adjustment and simple reference baselines. **Exit:** no uncorrected significance or claim of alpha.

**Loop 5 — Decision utility.** Strongest case: automation reduces false positives and organizes attention. Contradiction: complex indicator suites may add no economic edge and can encourage unneeded trading. Correction: separate hypothesis of research efficiency, correct abstention, low-frequency alternative and No Trade. **Exit:** system can succeed with zero candidate stocks; false historical alpha is never a required product outcome.

**Final steelman verdict:** The document-set is now stronger and internally testable at a **design level**. No predictive profit, licensure, execution, human review, or engine passing tests is established.

## C. High-severity attack cases and required deterministic defenses
| Test ID | Attack / adversarial input | Affected formula | Expected safe outcome |
|---|---|---|---|
| QA-01 | Split 2:1 misread as stock down 50% | M02/M20 | Corporate action reconciles share basis; abnormal loss blocked |
| QA-02 | Dividend-adjusted price plus cash dividend added twice | M02 | DOUBLE_COUNT_BLOCKED |
| QA-03 | Backtest uses restated 10-K before amended filing available | F01/F15/S07 | LOOKAHEAD_BLOCKED |
| QA-04 | 9-month YTD added to annual total as if quarter | F01 | Wrong quarter calculation rejected |
| QA-05 | Cash flow CAPEX extracted with negative XBRL sign and subtracted twice | F04/V03 | FCF reconciles once; reject sign ambiguity |
| QA-06 | Earnings crosses negative to positive and displays +900% growth | F02 | NOT_MEANINGFUL ratio; absolute change displayed |
| QA-07 | Negative equity yields huge negative ROE treated best-ranked | F07 | NOT_MEANINGFUL/flag |
| QA-08 | FCFF model uses cost of equity instead of WACC | V02/V04 | Model type/basis mismatch blocked |
| QA-09 | FCFE model discounts at WACC and deducts debt again | V15 | Model type/basis mismatch blocked |
| QA-10 | Terminal growth >= WACC | V05 | INVALID_TERMINAL_GROWTH |
| QA-11 | FCFF cashflow double counted at N+1 and in terminal | V04/V05 | Cashflow-period identity check fails |
| QA-12 | Excess cash counted inside and outside operating FCFF | V06 | Equity bridge reconciliation fails |
| QA-13 | Options dilution ignored in per-share value | V07 | Full diluted shares needed or evidence missing |
| QA-14 | EBITDA negative yields "cheap" EV/EBITDA | V09 | NOT_MEANINGFUL |
| QA-15 | Reverse DCF with no plausible root emits unsupported implied growth | V10 | NO_ROOT |
| QA-16 | Marketable buy at ask, simulated sell at bid, plus spread charged again | T01/T02/T10 | Double-cost invariant fails |
| QA-17 | Buy at candle bottom after candle close and exit at same candle top | T09/S07 | IMPOSSIBLE_LOOKAHEAD |
| QA-18 | Stop and profit target both hit in minute candle; choose profitable one | T09 | AMBIGUOUS_EXECUTION |
| QA-19 | Stop $90 but next executable opening bid $70 | T08 | Cannot credit $90 sale |
| QA-20 | Limit order filled at touch without queue/depth | T05/T17 | Partial/unfilled or conservative model |
| QA-21 | Gross price +0.3%; all-in costs +0.5% | T03/T04 | Negative net; NO_TRADE |
| QA-22 | 55% gross win +1.5%, loss -2%, costs .15% | T04 | -0.225% expectancy; NO_TRADE |
| QA-23 | 96% wins with 4% catastrophic losses | T04/B07 | Tail risk and expectancy gate prevent forced promotion |
| QA-24 | 50 near-identical tech names counted as 50 independent observations | S02/S03 | Clustered inference, not naive n |
| QA-25 | Optimize weights using final holdout | S06/S07 | Test contamination recorded; evidence disqualified |
| QA-26 | Repeatedly test hundreds of configurations and report best nominal p-value | S08 | Multiple-testing disclosure and correction |
| QA-27 | Portfolio deposits treated as investment return | B01/B03 | Cash-flow-adjusted return required |
| QA-28 | Sum +10% and -5% returns as +5% | M04/B01 | Exact geometric +4.5% |
| QA-29 | Average individual trade return used as compound capital growth | B13/B15 | Require capital constrained NAV trajectory |
| QA-30 | Annualize serial-correlated intraday trade Sharpe via sqrt(252 trades) | B04/B15 | Dependence-aware time-based returns |
| QA-31 | 3 data points yield precise 95% VaR/ES forecast | B07 | INSUFFICIENT_TAIL_SAMPLE |
| QA-32 | VaR is claimed maximum possible loss | B07 | Prohibit that claim; stress gaps beyond sample |
| QA-33 | Zero losses => "infinite profit factor" | B08 | UNDEFINED_PROFIT_FACTOR |
| QA-34 | Risk free 90-day Treasury discount yield used as effective annual | M18/B04 | CONVERSION_REQUIRED |
| QA-35 | Ranks use sectors from current 2026 classification in 2020 simulation | F16/S07 | PIT peer classification required |
| QA-36 | Current ticker reused for different historical issuer | F01/M02 | Permanent effective-date security identity required |
| QA-37 | Unlicensed quote information published on public Pages | M15/T15 | Publication gate denies |
| QA-38 | Feed only IEX venue but labeled consolidated SIP | M19/T15 | LIMITED_FEED; no real-time full-market claim |
| QA-39 | Calculated data source fetched now although only available tomorrow | S07 | LOOKAHEAD_BLOCKED |
| QA-40 | AI writes a "95% chance of win" from a 95-point factor score | S04/F17 | Probability absent until calibration and proof |
| QA-41 | Closed NYSE holiday session marked stale when no bar | M05 | Calendar-aware no new session; no false signal |
| QA-42 | Earnings release time used as day start in 2020 retrospective | F01/S07 | Actual dissemination timestamp required |
| QA-43 | 1.5% projected gain for 100M shares without depth | T06/T18 | Capacity and impact fail |
| QA-44 | Negative/zero invested capital shown as ROIC 5000% | F06 | NOT_MEANINGFUL/flag |
| QA-45 | USD billions vs USD millions mixed in EV | V06 | Currency and unit scaling check rejects |
| QA-46 | Borrowing costs omitted from short or leveraged scenario | T10 | Scenario out-of-scope research only |
| QA-47 | Same symbol appears as multiple share classes in universe | F12/S07 | Stable identity and deduplication |
| QA-48 | Negative/zero FCF used as ordinary positive P/FCF | V09 | NOT_MEANINGFUL |
| QA-49 | A dividend paid during holding included both via reinvested price and ledger | M02/B12 | Dividend accounting mismatch blocked |
| QA-50 | Profitable same-week signals force daily recommendations | S09 | Zero-candidate day is valid; no quota |

## D. Residual risk and independent human review
All QA scenarios above remain **UNEXECUTED**. All formulas are **UNIMPLEMENTED** until linked source code and CI assertions are present. A mathematically correct engine may still lose capital. Validation thresholds must be preregistered and reviewed by an independent qualified quantitative analyst; the user is not required to take trades.
Pending real human reviews: accountant/financial-statement expert, quant researcher, market-data microstructure specialist, security engineer, product reviewer and legal adviser for intended distribution. Never present role-play review as actual approval.

**Release design exit criteria:** 100% of QF formulas in six modules have names, units, guards and provenance; every high-severity QA scenario maps to a code test before release; no strategy that has not passed after-cost OOS and prospective gates is labeled profitable. The design passes; the software does not yet.
