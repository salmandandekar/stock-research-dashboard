# Quantitative Standards — Valuation, Implied Expectations and Scenarios (v1.3)

**Mathematical consistency first.** A company's operational value, debt claims and current diluted share count are different objects. All value estimates are scenario outputs, not externally verified stock-price targets.

| ID | Formula | Guard and anti-double-count |
|---|---|---|
| QF-V01 | Cost of common equity under CAPM k_e = r_f + beta × ERP | All inputs annually compounded/consistent, same currency and economic period; beta computed from as-of aligned market returns. CAPM is a model with limitations. |
| QF-V02 | WACC = (E/V)k_e + (D/V)k_d(1-T) + (P/V)k_p; V=E+D+P | Market values of equity/debt/preferred where feasible; marginal tax shield only if economic; leased debt/cash treatment consistent. |
| QF-V03 | FCFF = EBIT(1-T)+D&A - capital_expenditure - increase_in_non_cash_operating_NWC | All measures same period/currency, T marginal normalized operating rate. FCFF is before debt financing. CFO+after_tax_interest-CAPEX alternative may be used only with reconciled accounting basis. |
| QF-V04 | EV = SUM(t=1..N, FCFF_t/(1+WACC)^t) + terminal_value_N/(1+WACC)^N | Explicit annual discount dates, annual WACC, terminal value only once. Midyear convention separately versioned. |
| QF-V05 | Gordon terminal value_N = FCFF_N × (1+g)/(WACC-g) | Only if WACC>g, FCFF in steady state and normalized sustainable growth/reinvestment. Invalid otherwise. |
| QF-V06 | Common equity value = EV + excess_cash + nonoperating_assets - market_debt - preferred_claims - NCI - debt_like_lease_liabilities_not_already_in_EV - other_claims | Reconcile all bridge items to FCFF treatment. No debt/cash/lease double count. Negative equity value possible model output but not executable negative stock price. |
| QF-V07 | Fair value per share = equity_value/current_economic_diluted_shares | Share count>0; account for in-the-money options, convertible and class claims without double counting. |
| QF-V08 | Potential upside = value_per_share / quoted_price - 1; margin_of_safety = (value_per_share - quoted_price) / value_per_share | These are **different denominators**. If intrinsic value <=0, conventional margin of safety undefined. |
| QF-V09 | EV/EBITDA = enterprise_value/positive EBITDA_TTM; EV/sales=EV/revenue; P/E=price/positive diluted EPS_TTM; P/FCF=market_cap/positive annual FCF | Negative/zero denominators must be flagged "not meaningful"; don't turn negative P/E into cheap ranking. Enterprise multiples cannot use common-equity market cap as EV. |
| QF-V10 | Reverse-DCF implied parameter theta* solves DCF(theta*, fixed other assumptions)=current total equity market cap | Fix which single parameter is solved (growth/margin/reinvestment/discount rate); disclose bounds, existence, monotonicity and all valid roots. No root => UNKNOWN. |
| QF-V11 | Bear/base/bull value: separately model sales × operating margins, reinvestment, taxes, reinvested capital, WACC and terminal; no automatically summed expectation unless documented scenario probabilities. | Probabilities must be calibrated, nonnegative, sum=1. Otherwise show scenario range, not a fictitious weighted fair value. |
| QF-V12 | Terminal-value dominance = present_value(terminal_value)/EV; local sensitivity delta V ≈ [V(x+h)-V(x-h)]/(2h) | State sensitivity variable, step h, units and nonlinear instability near WACC=g. |
| QF-V13 | Normalized revenue_t = revenue_0×PRODUCT(1+growth_i); EBIT_t=revenue_t×op_margin_t; NOPAT_t=EBIT_t×(1-T_t); FCFF_t=NOPAT_t-reinvestment_t | Economic dependency prevents unrelated optimistic profit-margin and cash-flow assumptions; scenarios must balance. |
| QF-V14 | Growth-consistent perpetual economics approximately g = reinvestment_rate×incremental_ROIC for stable drivers | Only if assumptions fit economic business model; not universal identity; sanity and sensitivity check. |
| QF-V15 | FCFE equity valuation = SUM(FCFE_t/(1+k_e)^t) + TV_equity_N/(1+k_e)^N | Discount at equity cost, not WACC; FCFE after debt cashflows, so do NOT subtract debt from value again. |
| QF-V16 | Justified valuation and peer comparisons should use same trailing/forward period, accounting and equity/enterprise denominator | PIT analyst estimates require provider rights; sector and size comparability; no forward earnings available only ex post. |

**Reference deterministic valuation fixture (synthetic USD millions):** FCFF years 1–3 = 100, 110, 121; WACC = 10%; terminal growth = 3%; present value operating EV = 1610.38961038961. Bridge adds excess cash 50 and subtracts debt 300, giving equity 1360.38961038961; with 50 million diluted shares, value/share = 27.20779220779 USD. Note: inputs represent a *toy model*, not an assessment of any security. A model using WACC=8.75% from separate fixture should NOT be mixed with this 10% discount scenario.

**Separate WACC fixture:** E weight 80%, D weight 20%, k_e=10%, k_d=5%, corporate tax=25%. WACC=0.0875 = 8.75%.

**Adversarial gate examples:** WACC 2%, terminal g 3%; terminal g = WACC; negative normalized FCFF; debt already netted from operating enterprise; 100 million stock options ignored; EBITDA<0; negative earnings yielding misleading P/E; reverse DCF with no root; 1 dollar retained cash needed to operate treated as excess; 50% terminal value sensitivity from a 10bp g change.

**References:** CFA Institute Free Cash Flow Valuation (2026): https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation ; CFA Market-Based Multiples (2026): https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/market-based-valuation-price-enterprise-value-multiples .

**Release gate:** An upside estimate alone is NOT a buy or trade signal. It must be independently gated by data quality, uncertainty, balance-sheet risk, value sensitivity and the user's research horizon. Banks, REITs and insurers require specialist reviewed valuation logic or abstain.
