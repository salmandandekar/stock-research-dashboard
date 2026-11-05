# Quantitative Standards — SEC Financial Fundamentals (v1.3)

**Scope:** US-listed nonfinancial common shares. Banking, insurance, REITs and other special accounting industries require a specialist adapter. This document is a *specification*, not implemented validation.
**Raw source requirement:** XBRL taxonomy + concept, unit (USD, shares, USD/shares), period start/end, fiscal Q/FY, statement scope, form, accession, filed/accepted availability timestamps, amendment version and parsed fact snapshot. The latest SEC Company Facts number is not necessarily the number known in a historical backtest. "Frames" are approximated calendar periods and must be checked against exact fiscal dates.

| ID | Formula | Conditions and exceptions |
|---|---|---|
| QF-F01 | TTM(flow)=sum of four distinct fiscal-quarter flows. If only YTD cumulative: Q2=6moYTD-Q1YTD; Q3=9moYTD-6moYTD; Q4=Annual-9moYTD. | Same exact company and fiscal periods, reporting basis and currency, 52/53-week adjustments; do not add annual+quarter, and preserve revisions as available-at. |
| QF-F02 | Conventional YoY growth=(X_t/X_t-1)-1, and growth over years=(X_end/X_start)^(1/years)-1 | Only positive comparable bases. Zero/negative or sign crossings: NOT_MEANINGFUL; show absolute change instead. |
| QF-F03 | Gross margin=(revenue-COGS)/revenue; EBIT margin=operating_income/revenue; net margin=NI attributable to common/revenue | Revenue>0 and matched reporting periods. Sector deviations explicitly modeled. |
| QF-F04 | CFO-based free cash flow proxy=operating_cash_flow - positive_capex_outflow | Normalize XBRL sign once; do not double-negate capital expenditures. SBC, acquisitions, mandatory debt service not automatically deducted by this definition. |
| QF-F05 | NOPAT=EBIT × (1 - applicable normalized operating tax rate) | Marginal operating tax convention, not blindly tax expense/pretax profit when negative or exceptional. |
| QF-F06 | ROIC=NOPAT / mean(begin invested capital, end invested capital) | Capital>0, consistent treatment of operating NWC, goodwill, leases, excess cash and noncontrolling interests. |
| QF-F07 | ROE=NI_attributable_to_common / average common equity; ROA=NI/average total assets | Negative/zero equity => undefined or misleading; do not rank negative denominator as superior. |
| QF-F08 | Net debt=interest-bearing borrowings + defined debt-like leases - eligible excess cash | Restricted cash excluded; debt market/book-value proxy disclosed; no duplicated lease debt. |
| QF-F09 | Net debt/EBITDA=net debt/EBITDA_TTM; interest coverage=EBIT/interest expense | EBITDA<=0 makes conventional coverage multiple not meaningful; interest=0 is no-expense state, not an exploitable infinity. |
| QF-F10 | Current ratio=current assets/current liabilities; quick ratio=(cash+marketable securities+net receivables)/current liabilities | Liabilities>0, cash classifications valid, financial industry separate. |
| QF-F11 | CFO/NI quality proxy=CFO/NI (only when NI>0); total accruals=(NI-CFO)/average assets | Do not treat one unusual cash cycle as recurring; align periods. |
| QF-F12 | Dilution growth=split-adjusted comparable diluted share count_t/share count_prior - 1 | End-of-period shares vs diluted weighted average shares are not substitutes; convert share classes/convertibles explicitly. |
| QF-F13 | EPS_basic=(NI - preferred_claims) / weighted_average_basic_shares. Diluted EPS=(appropriately adjusted diluted numerator)/(weighted diluted shares). | Do not divide TTM NI by single end-date shares or sum unadjusted quarterly EPS across a split. |
| QF-F14 | Capex intensity=capex/revenue; FCF margin=FCF/revenue; working capital change=period ending noncash NWC - beginning noncash NWC | Guards on revenue>0 and fiscal alignment; require definition of noncash working capital. |
| QF-F15 | Accounting invariants: assets≈liabilities+equity; beginning_cash+net_cash_change≈ending_cash after FX/restricted cash and presentation differences | Tolerances and permitted bridges defined, never overwrite mismatches. |
| QF-F16 | Peer percentile=(count(x_peer<x_i)+0.5 count(equal))/N; reverse for smaller-is-better | Peer membership and N historically available, sector-specific; training-only winsorization, disclose omitted peers. |
| QF-F17 | Factor score=sum(weights × normalized eligible factor value), sum(weights)=1 | Research priority only, NOT profitable-trade probability; refuse missing material factor rather than reweight opportunistically. |
| QF-F18 | Cash flow reinvestment=capex - D&A + change in noncash operating working capital; reinvestment rate=reinvestment/NOPAT | NOPAT<=0 => undefined; avoid real estate/banking model misapplication; capex/depreciation cannot be treated as equal. |
| QF-F19 | Balance sheet leverage=current and long-term debt / equity or assets (explicit denominator); liquidity runway=available cash / expected cash burn | Negative shareholder equity invalidates simplistic debt-to-equity comparison; forecast cash burn uncertain. |
| QF-F20 | Normalized earnings=reported GAAP/IFRS amount + approved disclosed adjustments (with signs) | Every adjustment needs source and rationale; show reported and adjusted. Reject inconsistent period-to-period recurring expense exclusions. |

**GAAP / non-GAAP distinction:** Free cash flow does not have a uniform standardized definition. SEC guidance requires reconciliation/explanation when a filer presents this measure and warns against inferring it is freely distributable. The application must not claim EBITDA is cash flow or label adjusted operating cash flow as GAAP.

**Company identity and timing:** Map ticker and share class to permanent IDs and CIK effective dates; preserve delisting, merger, split and amendment history. SEC API records may be updated or corrected. A historical metric must read a version **available then**. For annual and quarterly records, record statement inception date, period end and actual dissemination timestamp separately.

**Research sources:**
- SEC Company Facts, filing dates and units: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC non-GAAP C&DI: https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations/non-gaap-financial-measures
- CFA Financial Analysis Techniques: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/financial-analysis-techniques
- CFA Financial Statement Integration: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/integration-financial-statement-analysis-techniques

**Mandatory tests:** Annual YTD/Q4 extraction, 53-week report, two 10-K amendments with different accepted dates, renamed XBRL concept, different currency, negative earnings, zero equity, stock split before and after diluted EPS, negative CAPEX XBRL sign, disallowed adjusted EBITDA, stale debt and missing NCI.
