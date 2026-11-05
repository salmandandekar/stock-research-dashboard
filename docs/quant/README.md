# QFCS v1.3 — Mathematical Specification Index and Engineering Release Checklist

**Design status:** Acceptable for staged implementation only. Calculation software, stock-selection predictive value, source licensing, and live execution have **not** been proven.

## Modules and inventory
| File | Domain | Formula IDs | Count |
|---|---|---|---:|
| [01_MARKET_MATH.md](01_MARKET_MATH.md) | price, quotes, technical measures, corporate actions | QF-M01..M20 | 20 |
| [02_FUNDAMENTALS.md](02_FUNDAMENTALS.md) | SEC financial periods, ratios, cash flow, dilution | QF-F01..F20 | 20 |
| [03_VALUATION.md](03_VALUATION.md) | DCF, WACC, cash/claims bridge, reverse DCF | QF-V01..V16 | 16 |
| [04_EXECUTION_COSTS.md](04_EXECUTION_COSTS.md) | bid/ask, realized PnL, costs, fills and gaps | QF-T01..T20 | 20 |
| [05_PORTFOLIO_RISK.md](05_PORTFOLIO_RISK.md) | TWR/MWR, NAV, benchmark, risk/tail/attribution | QF-B01..B20 | 20 |
| [06_STATISTICAL_VALIDATION.md](06_STATISTICAL_VALIDATION.md) | cross-validation, calibration, alpha, uncertainty | QF-S01..S20 | 20 |
| [07_RED_TEAM_STEELMAN.md](07_RED_TEAM_STEELMAN.md) | entire approved-requirements crosswalk and 5 strengthening loops | QA-01..QA-50 | 50 scenarios |

**Total:** 116 formula contracts and 50 adversarial scenarios; 40 synthetic golden spec examples in [quant_vectors_A.json](../../tests/specs/quant_vectors_A.json) and [quant_vectors_B.json](../../tests/specs/quant_vectors_B.json).

## Source-based rationale
- CFA financial statement, DCF, multiples and performance methods define widely used financial analysis conventions.
- SEC EDGAR makes free filing/XBRL facts available, but units, dates and amendments require careful reconciliation.
- Lo (2002) shows Sharpe-ratio annualization can be invalid under return autocorrelation.
- Bailey, Lopez de Prado and others show selecting the best among many historical trials overstates evidence; factor-mining studies warn against naive significance claims.
- GIPS stresses proper treatment of external cashflows and geometric chaining for time-weighted performance.
- Market data providers distinguish partial exchange feeds, delayed consolidated feeds, and authorized real-time entitlements.

## Formal formula contract template
Each domain implementation must expose:
```text
formula_id, version, strategy_id, security_id, unit, currency, input_source_ids,
source_licenses, input_available_at, market_session_id, window_definition,
adjustment_type, calculation_policy_sha, numerical_precision_and_rounding,
input_values_or_snapshot_refs, denominator_checks, missing_policy,
output_value_or_explicit_error_state, model_confidence_or_data_quality,
reference_test_case_ids, implementation_sha
```
No output can be silently imputed as 0, ranked when critical inputs are absent, or republished retroactively.

## Mandatory release gates
- **QFG-0 documentation:** Full formula inventory, guards, supporting sources and adversarial review. **Satisfied at specification level only.**
- **QFG-1 independent math:** Implement every released formula as deterministic code with correct units and availability times. All 116 formulas require tests before claiming complete support; unimplemented formula IDs disabled. Test each invalid/edge case, regression and independent oracle. **Pending.**
- **QFG-2 accounting and data:** Reconcile SEC periods, amendments, sign conventions, company identity, splits/dividends and appropriate vendor licenses. **Pending.**
- **QFG-3 execution simulator:** Prove quote/depth, spread/slippage, delay, stop gaps, partial/unfilled and execution ambiguity; no impossible PnL. **Pending.**
- **QFG-4 statistical credibility:** Point-in-time walk-forward holdout, transaction costs, experiment register, correlated-signal inference, risk-adjusted baselines and uncertainty. **Pending.**
- **QFG-5 prospective evidence and humans:** Paper-only forward observation, losses and no-trade counts, independent quantitative reviewer and data/security/legal review before wider use. **Pending.**

## Suggested implementation order
1. Schema/provenance and EDGAR PIT normalizer; golden-vector harness and registry.
2. Market and financial ratio calculators (pure functions).
3. DCF/valuation scenarios with independent arithmetic reconciliation.
4. Conservative long-only swing fill model and capital ledger.
5. Risk/performance reporting with correct cashflow, daily-return and benchmark math.
6. Holdout, cluster/bootstrap validation and factor baselines.
7. Optional licensed intraday feed and controlled paper-only monitoring.
8. AI explanations *downstream* of deterministic, verified numbers; AI does not evaluate formulas or issue trades.

**What "best results" means:** lowest avoidable calculation error, strongest evidence quality, least false confidence, transparent downside and fewer unjustified trade suggestions. No mathematical design can guarantee exceptional investment returns.

## Key references
- https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation
- https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/market-based-valuation-price-enterprise-value-multiples
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations/non-gaap-financial-measures
- https://www.gipsstandards.org/standards/gips-standards-for-firms/gips-standards-handbook-for-firms/
- https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios
- https://escholarship.org/uc/item/4w1110bb
- https://doi.org/10.3905/jpm.2014.40.5.094
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2513152
- https://docs.alpaca.markets/us/docs/market-data-faq
