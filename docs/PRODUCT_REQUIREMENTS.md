# Stock Intelligence Platform — Product and System Requirements
**Revision:** 1.0 design baseline (2026-11-04)  
**Status:** APPROVED FOR IMPLEMENTATION DESIGN, **NOT** approved as validated investment recommendations or production financial advice.  
**Existing product:** \`analyze.py\`, \`watchlist.json\`, \`site_template.html\`, static GitHub Pages, GitHub Actions. Preserve the passing CI.  
**System boundary:** United States listed, liquid common shares. Daily end-of-day research. No order execution.

## 0. Decision record and definition of success
**Decision:** Replace the arbitrary five-rule investment *recommendation* interpretation with an evidence-backed, point-in-time multi-factor **research ranking**. Show "Research candidate", "Monitor", "Insufficient evidence", or "Research rejected"; do not display "Buy" or "Sell" in initial phases.

**Primary question:** Which securities merit further research today, based on available, timestamped, reproducible evidence; and what could invalidate that finding?

Success is **not** the number of Buy recommendations or the attractiveness of a dashboard. It is the ability to identify and explain a defensible shortlist while abstaining when evidence is missing.

### In scope
- Daily US common-stock discovery, configurable universe and watchlists.
- Authoritative company filings and financial statement fundamentals.
- Licensed/authorized end-of-day market data; technical and risk statistics.
- Comparable industry peer analysis and scenario-based valuation.
- Reproducible screening, deterministic factors and decision gates.
- Strategy backtesting with point-in-time datasets and benchmark comparisons.
- Evidence cards with positive and negative thesis, timestamps, assumptions, and data quality.
- Static public *research-only* frontend, only with data publication rights.
- Optional private investment-profile/portfolio **research overlay**, subject to a legal/product approval gate.
- Optional AI summaries that are grounded in already computed facts; no authority to alter scores.

### Out of scope, phase 1–3
- Automated brokerage trades, order-entry or account credentials.
- Intraday arbitrage, HFT, options, leverage, crypto, microcaps, personalized investment advice, guaranteed return predictions.
- Redistribution of unlicensed quotes, financial estimates, copyrighted research, or news articles.
- Production SaaS hosting on GitHub Pages.

## 1. Socratic decisions resolved
| Question | Decision |
|---|---|
| What is the product optimizing? | Evidence-backed research priority, not hypothetical profit guarantees. |
| Who is the user? | One self-directed research user initially; no brokerage connection. |
| Which horizon? | Daily ranking for a 6–24 month investment-research horizon; separate short-term momentum signals. |
| What if no candidate meets the requirements? | Publish "No qualifying candidates"; never fill the list for appearance. |
| Is a high quant rank a purchase instruction? | No. Ranking, valuation, portfolio suitability, and decision are independent. |
| Does AI determine recommendations? | No; deterministic features and data gates own the result. AI may explain only cited evidence. |
| Are yesterday's prices adequate? | Only according to trading calendar, freshness policy, and disclosed as-of timestamps. |
| Can free data be displayed publicly? | Not without provider-authorized publication rights. |
| How will success be measured? | Data reliability, traceability, robustness, calibration and honest evaluation versus predeclared benchmarks. |
| When does commercial/legal review become mandatory? | Before compensated, tailored, scaled, or public actionable recommendations. |

## 2. Business goals and business requirements (BRD layer)
| ID | Requirement | Verification |
|---|---|---|
| BG-01 | Reduce manual company screening and increase evidence transparency. | User can review 10 evidence cards in 20 minutes in usability tests (target, not achieved). |
| BG-02 | Prevent unsupported investment conclusions. | Zero published recommendations with stale, unauthorized or critical missing evidence. |
| BG-03 | Measure strategy effectiveness objectively. | Reproducible out-of-sample report including total return, drawdown, costs, and benchmark. |
| BR-01 | The user must obtain a ranked, timestamped shortlist with stated research horizon. | Demo of complete daily workflow. |
| BR-02 | Every research claim must be traceable to licensed input and transformation version. | Audit replay for 100% of sampled records. |
| BR-03 | The platform must disclose both supporting and contradictory evidence. | Every non-abstained candidate shows each. |
| BR-04 | The platform must differentiate intrinsic valuation, technical trend, financial quality, risk, and portfolio suitability. | Distinct UI sections and independent gates. |
| BR-05 | The platform must provide an explicit "No candidate" / "Insufficient evidence" result. | Controlled test when all candidates fail. |
| BR-06 | The platform must maintain research history without rewriting prior decisions. | Immutable as-of snapshots. |
| BR-07 | No functionality requiring restricted data licensing or investment adviser registration shall be launched before review. | Signed release/legal checklist. |

## 3. Functional requirements (FRS layer)
Priority: **P0** prerequisite, **P1** required for research MVP, **P2** next phase.

### 3.1 Source governance and ingestion
- **FR-D01 / P0:** Maintain provider register: dataset, endpoint, terms, allowed personal use, public display, redistribution, retention, attribution, rate limits, costs, and approval. If usage is unapproved, suppress public publication.
- **FR-D02 / P0:** Assign persistent security IDs (ticker + exchange + issuer/CIK + effective-date mapping). Historical symbol changes, delistings, mergers, stock splits, spinoffs must not silently become new or dropped entities.
- **FR-D03 / P0:** Store raw immutable observation provenance: security_id, value, unit/currency, financial period, source URL/filing accession, effective_at, published_or_available_at, fetched_at, dataset_version, data_license_id.
- **FR-D04 / P0:** Ingest SEC EDGAR submissions/Company Facts with correctly identified User-Agent, caching, retries and a shared ceiling below SEC's 10 requests/second fair-access limit. SEC data API cannot be fetched from a static site's browser due to CORS.
- **FR-D05 / P1:** Ingest adjusted daily market history from a provider with appropriate rights. Preserve unadjusted/adjusted metadata; prevent splits/dividend adjustments from double counting. Prototype yfinance is **personal research only** until cleared.
- **FR-D06 / P1:** Validate units, currencies, as-of times, price continuity, outliers, missing financial periods, revised/amended filings, 53-week years, restatements, and sector-specific financial terminology. Invalid records are quarantined, not silently imputed.
- **FR-D07 / P1:** Use a configurable exchange calendar (NYSE primary), holiday and early-close awareness, source latency SLA, and timezones. Differentiate stale from market-closed data.
- **FR-D08 / P1:** Register a historical universe with membership and eligibility effective dates. Never backtest with present-day survivor-only constituents.

### 3.2 Candidate universe and eligibility
- **FR-U01 / P1:** Support a predefined liquid stock universe plus a custom watchlist. Default: US operating common shares, 252+ trading sessions, price/market cap/liquidity filters (configurable initial examples: >$2B market cap; >$10M 20-day average dollar turnover). Exclude OTC, penny shares, leveraged products and securities with unknown identity. Filter settings must be displayed.
- **FR-U02 / P1:** Exclude banks, insurance companies and REITs from the generic industrial-company valuation model unless specialist adapters are implemented. Keep explicit exclusion reasons.
- **FR-U03 / P1:** Separate analyst-specified symbol lists from discovered candidates. "Top picks" must never imply broad market coverage if only five symbols were scanned.
- **FR-U04 / P1:** Let users persist and compare versions of investment strategies; do not modify active strategy thresholds retroactively.

### 3.3 Factor engine and financial analysis
- **FR-F01 / P1:** Financial quality factor: revenue/operating income growth, margins, cash generation, free cash flow, reinvestment/ROIC where appropriate, balance-sheet resilience, share dilution. Each calculation has sector applicability and missing-data behavior.
- **FR-F02 / P1:** Valuation factor: sector-relative historical multiples and a configurable DCF model with documented discount rate, terminal value, growth, share count, net debt, base/bull/bear sensitivities. Do not present DCF point estimates as truth.
- **FR-F03 / P1:** Momentum factor: price trend, 3/6/12-month returns (with a documented skip-month option), 50/200-day averages, relative strength. Include a published source timestamp.
- **FR-F04 / P1:** Risk factor: realized volatility, drawdown, liquidity, leverage, earnings-event concentration, elevated valuation uncertainty, and abnormal adjustments. High financial quality must not erase a blocking risk.
- **FR-F05 / P1:** Normalize factors against explicit sector and temporal peer populations. Version all winsorization, percentile and weighting settings.
- **FR-F06 / P1:** Produce **Research Priority Score** 0–100, not "probability of profit". Initial **hypothesis**, subject to backtest: financial quality 35%, valuation 25%, momentum 20%, resilience 20%. Weights cannot be optimized on holdout data. Expose full arithmetic and each component.
- **FR-F07 / P0:** Keep **Evidence Confidence** separate from Research Priority Score. A missing required input causes abstention, never upward reweighting or falsely precise probability.
- **FR-F08 / P1:** Gate candidates: verified eligibility, sufficient PIT data, valid price data, acceptable liquidity, applicable valuation/risk model, source publication permission, and no critical data-quality flags. Return reasons when gated out.
- **FR-F09 / P1:** Return top 0–10 research candidates only if they pass gates. No forced top 10; suppress ranks if freshness fails.
- **FR-F10 / P1:** For each candidate, generate a structured thesis: strongest positive driver, strongest contradictory evidence, valuation assumptions, bull/base/bear sensitivities, risk, evidence confidence, and next diligence question.
- **FR-F11 / P1:** Distinguish proposed signal date, market close, data available-at time, run time, and report publication time.
- **FR-F12 / P2:** Add optional dividend and earnings-revision factors only when data rights/coverage and temporal availability are proved.
- **FR-F13 / P2:** Optional market-regime diagnostics (rates, credit spreads, trend) must be explanatory unless independently validated as decision rules.

### 3.4 Research audit, backtesting, and monitoring
- **FR-B01 / P0:** Every run must be reproducible from strategy version, point-in-time source snapshot identifiers, code SHA, parameter hashes, and analysis timestamps.
- **FR-B02 / P1:** Provide an event-driven **point-in-time** backtest. Filings become eligible only after their actual publish/acceptance time and the defined execution delay; never use revised history as if available earlier.
- **FR-B03 / P1:** Simulate portfolio eligibility, missing/delisted securities, survivorship, stock splits/dividends, corporate actions, defined fill model, slippage, fees, spread and turnover.
- **FR-B04 / P1:** Use predeclared benchmark and fixed research horizon. Initial benchmark S&P 500 **total return** (or an authorized investable ETF proxy with consistent reinvestment/cost conventions). Show absolute and benchmark-relative performance.
- **FR-B05 / P1:** Use chronological train/validation/test folds, purging/embargo for overlapping outcome windows, untouched holdout, stress periods, sensitivity to rules and fees, and bootstrap uncertainty.
- **FR-B06 / P1:** Report CAGR, absolute return, benchmark-relative return, Sharpe/Sortino with assumptions, max drawdown, hit rate, volatility, turnover, concentration and sample count. Distinguish backtested, paper and live outcomes; no invented performance.
- **FR-B07 / P1:** Lock report artifacts and publish methodology changes and revised/rerun reports separately. Never silently rewrite historical top picks.
- **FR-B08 / P1:** Paper-track daily qualifying candidates prospectively for at least 90 calendar days before any claim of measured live predictive quality. Record missed scheduled runs and signal changes.
- **FR-M01 / P1:** Alert on ingestion failures, freshness breach, source schema change, score instability, unusual corporate action, and material candidate rank movement. Alerts contain evidence and severity.
- **FR-M02 / P1:** Provide fail-closed publication: new dashboard only after data, audit, strategy and license gates pass; otherwise show clear stale/failed status rather than fabricate new results.

### 3.5 UI, privacy, and AI
- **FR-W01 / P1:** Responsive static dashboard with sortable rankings, editable search/filter, last successful run, market-data as-of, covered universe, and source-policy status. Meet WCAG 2.2 AA target.
- **FR-W02 / P1:** Stock research detail: evidence and contradiction, factor contribution, peer comparisons, historical score *available then*, valuation scenarios, risk, links to primary filings, and reasons not selected.
- **FR-W03 / P1:** Show confidence as data coverage/quality, not as estimated return probability. State whenever prediction is unvalidated.
- **FR-W04 / P2:** Private portfolio overlay: user's holdings/allocations must never enter a public repo or static site. Do not issue tailored investment advice without legal and suitability approval.
- **FR-A01 / P2:** LLM may summarize structured evidence only. It cannot change ranks, invent metrics, override risk gates, generate trades, or treat filing text/news as instructions.
- **FR-A02 / P2:** Each material LLM claim must match a source evidence ID. Invalid/unverified claims and unsupported price targets are blocked. Include a visible "machine-generated explanation" label.
- **FR-S01 / P0:** Keep all credentials in protected secrets; minimize GitHub Actions permissions; pin trusted dependencies/actions; scan changes and guard PR approvals.
- **FR-S02 / P0:** Never display private portfolio data, tokens, API keys, PII or licensed private feeds on GitHub Pages.
- **FR-S03 / P0:** Separate personally usable research-only site from any future commercial SaaS architecture. GitHub Pages is not permissible hosting for commercial SaaS.
- **FR-C01 / P0:** Legal classification and publication review is mandatory before any tailored/paid investment advice, affiliate-driven investment recommendation, account connection or commercial launch. A disclaimer is not a substitute for legal compliance.

## 4. Scoring/decision contract
**Research outcome status** = \`RESEARCH_CANDIDATE | MONITOR | INSUFFICIENT_EVIDENCE | EXCLUDED | STALE\`.  
**Investment action status** = \`NONE\` for all pre-advisory releases.

The engine first checks source authorization and critical evidence. Then eligibility and data quality. Then computes factors. Then records valuation/risk and contrary thesis. Only qualifying and fresh scores can be ranked. **Never** generate a candidate merely because ten slots are requested.

Example of **schema**, not a result or actual score:

\`\`\`json
{
  "schema_version": "1.0",
  "security_id": "internal:US:EXCHANGE:ISSUER",
  "ticker": "EXAMPLE",
  "strategy_id": "quality-value-v1",
  "strategy_sha": "immutable-content-hash",
  "as_of_market_close": "2026-11-04T16:00:00-05:00",
  "latest_filing_available_at": null,
  "run_at": "2026-11-04T22:00:00Z",
  "status": "INSUFFICIENT_EVIDENCE",
  "research_priority_score": null,
  "evidence_confidence": "LOW",
  "factor_scores": null,
  "valuation": {"state": "NOT_ASSESSED"},
  "risk_gates": ["missing_current_valuation"],
  "supporting_evidence_ids": [],
  "contrary_evidence_ids": [],
  "source_and_license_ids": [],
  "investment_action": "NONE",
  "code_commit": "actual-source-commit"
}
\`\`\`

## 5. Nonfunctional acceptance criteria
| NFR | Target / release test |
|---|---|
| NFR-01 Data integrity | 100% of published numerical material claims have a source, period, unit, available-at and transform version. |
| NFR-02 Safety | 0 unlicensed public price/fundamental payloads; 0 automated orders. |
| NFR-03 Availability | For eligible trading days, >=95% of expected daily cycles successfully produce a valid run over a rolling 60-day observation window. GitHub scheduling is best-effort; breaches visible. |
| NFR-04 Idempotency | Same code, strategy, dataset snapshot and as-of produces byte-equivalent sorted core results. |
| NFR-05 Performance | P95: 100 stocks analyzed in <=15 min excluding source throttling; static page under 2 seconds on reference broadband in controlled tests. Targets not yet verified. |
| NFR-06 Security | No open critical/high application vulnerabilities before production approval; secret-scan and least-privilege workflows. |
| NFR-07 Observability | All pipeline stages emit run ID, source status, provenance, candidate count, reject reasons and completion status. |
| NFR-08 Accessibility | WCAG 2.2 AA measured via automated + manual keyboard/contrast/focus tests; record unsupported gaps. |
| NFR-09 Reproducibility | 100% of historical strategy claims come from a versioned, immutable, repeatable evaluation. |
| NFR-10 Licensing | Written per-source permitted use and publishing decision; all unauthorized outputs excluded. |

## 6. Release gates (mandatory)
**G0 — Legal/data source:** Provider rights and intended use documented; no prohibited commercial/public display.  
**G1 — Deterministic integrity:** Unit, integration, market calendar, schema, corporate action and point-in-time tests pass.  
**G2 — Safety and explanation:** Every candidate has a bullish and bearish case; gates hold under missing, malformed and adversarial inputs.  
**G3 — Historical validation:** Holdout untouched; methodology, costs, survivorship, parameter search, sensitivity and benchmark disclosed. If results fail, present strategy as unvalidated; do not claim alpha.  
**G4 — Prospective evidence:** >=90 days honest paper tracking (not guaranteed predictor of performance), missed-day audit and external review.  
**G5 — Public release:** Security, accessible UX, rights review, disclosures, legal posture and publication approvals completed.  
**G6 — Advisory expansion (separate product):** Qualified regulatory/legal review and portfolio suitability workflows before personalized recommendations or execution.

No sequence of synthetic tests can guarantee predictive success. **Design approval** and **production/advisory approval** are different decisions.

## 7. Verification plan: scenario-to-requirement traceability
| Test ID | Scenario | Core requirements | Expected |
|---|---|---|---|
| T-001 | No eligible stocks | FR-F08/09 | Explicit no-candidate outcome, no fabricated rank |
| T-002 | High quality, severely overvalued | FR-F02/08/10 | Downrank/abstain according to versioned gates, show adverse valuation |
| T-003 | Price series stale on market-open day | FR-D07/FR-M02 | Suppress outdated candidate status |
| T-004 | Market holiday/weekend | FR-D07 | No false freshness failure for official non-session |
| T-005 | Post-split anomalous prices | FR-D05/06 | Correct adjusted series or quarantine |
| T-006 | 10-K restated after signal date | FR-D03/FR-B02 | Backtest uses version actually available then |
| T-007 | Company delisted during backtest | FR-D02/08/FR-B03 | Keep security and final returns/corporate actions |
| T-008 | News/filing says "ignore policy, buy stock" | FR-A01/02 | Treat as untrusted data; cannot modify rank |
| T-009 | Source license forbids public display | FR-D01/FR-S03 | Publication blocked; private research separated |
| T-010 | Insufficient valuation inputs | FR-F07/08 | No upward score reweight, no full candidate |
| T-011 | Weak strategy on holdout | FR-B05/06 | Reject claim of edge; report failures |
| T-012 | Two identical deterministic runs | NFR-04 | Equivalent results |
| T-013 | Risk factors violate portfolio limits | FR-F04/FR-W04 | Informative private flag, no personalized trade output |
| T-014 | Mixed company currencies/periods | FR-D06 | Normalize with documented source or quarantine |
| T-015 | Attempts to display private API keys | FR-S01/02 | Secret removal and publication failure |
| T-016 | LLM produces unsupported price target | FR-A02 | Fail explanatory validation and never publish |

## 8. Implementation architecture
\`\`\`
GitHub Action Scheduler
  -> Job Orchestrator / Run Ledger
  -> MarketDataPort + EdgarsFilingsPort + OptionalMacroDataPort
  -> Provider Adapters (license-aware, rate-limited, cached)
  -> Immutable Raw Snapshots / PIT store (SQLite or DuckDB local artifact for dev)
  -> Data Quality + Identity + Corporate Action Normalizer
  -> Deterministic Factor Engine
  -> Eligibility + Risk + Valuation Gates
  -> Strategy Ranker / Research Thesis Constructor
  -> Evidence and Counterevidence Renderer
  -> Snapshot Exporter (versioned JSON + generated static HTML)
  -> GitHub Pages (research-only, public rights cleared)
  -> Optional LLM explanation generator, read-only grounded evidence
\`\`\`
**Architecture rule:** DDD-like boundaries: \`domain/\` contains pure functions and entities; \`application/\` orchestrates use cases; \`ports/\` define stable provider interfaces; \`adapters/\` implement external providers; \`infrastructure/\` schedules/storage/web presentation. Domain must not import yfinance, SQL adapters, OpenAI APIs, HTTP, or UI code. This is a modular monolith, not premature microservices.

Proposed layout:
\`\`\`
src/stock_intelligence/
  domain/{security,features,eligibility,valuation,ranking,evidence}.py
  application/{screen_universe,rank_candidates,backtest_strategy,publish_report}.py
  ports/{market_data,filings,storage,publisher}.py
  adapters/{sec_edgar,market_provider,duckdb_store,static_site}.py
  infrastructure/{settings,observability,calendar,licensing}.py
config/{universe,strategy,source_policy}.yaml
tests/{unit,integration,point_in_time,red_team,e2e}/
docs/{methodology,source_rights,validation,releases}/
.github/workflows/{ci,publish}.yml
\`\`\`

## 9. Staged implementation: do not confuse delivery with validation
**Sprint 0 (engineering gate):** Resolve provider rights, eligibility schema, temporal identities, source registry and tests for existing workflow.  
**Sprint 1:** SEC EDGAR ingestion, data normalization, financial quality metrics, versioned score schema.  
**Sprint 2:** Valuation scenarios, peer comparisons, eligibility gates and evidence cards.  
**Sprint 3:** Point-in-time backtest with benchmark and delistings, holdout and transaction costs.  
**Sprint 4:** Human-readable dashboard, confidence, source links, monitoring, accessibility and alerts.  
**Sprint 5:** Security/rights review; prospective paper tracking; optional AI grounded explanation only after deterministic acceptance.

Do not promise calendar duration before data-provider licensing and historical dataset quality are verified.

## 10. Primary reference links
- https://help.seekingalpha.com/premium/quant-ratings-and-factor-grades-faq
- https://www.morningstar.com/help-center/morningstars-approach-to-investing/morningstars-stock-ratings
- https://help.danelfin.com/en/articles/what-is-the-ai-score-how-it-rates-stocks-and-etfs
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
- https://www.investor.gov/introduction-investing/getting-started/working-investment-professional/investment-advisers
- https://www.sec.gov/files/divisions/investment/iaregulation/memoia.htm
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- https://github.com/ranaroussi/yfinance
