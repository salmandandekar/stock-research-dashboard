# Steelman Review — Stock Intelligence Platform v1.1
**Date:** 2026-11-04  
**Status:** Design strengthening addendum; requires review before merging.  
**Depends on:** [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md), [ADVERSARIAL_REVIEW.md](ADVERSARIAL_REVIEW.md), [COMPETITOR_BENCHMARK.md](COMPETITOR_BENCHMARK.md).  
**Review type:** Strongest defensible case + competing cases + falsifiable criteria. No predictive result, penetration-test evidence, live product pilot, or regulatory approval is claimed.

## 1. One-sentence strongest product thesis
**Build a research decision ledger that identifies a manageable number of securities for further diligence, presents independently sourced bull and bear cases, measures how valuations and expectations may diverge, monitors thesis-invalidating events, and records whether that process improves decisions versus simpler alternatives.**

The differentiator is **reproducible decision quality**, not the claim that AI always predicts prices.

### Positive case, stated at full strength
1. **A real workflow problem:** fragmented portals force an investor to repeatedly reconcile filings, valuation, forecasts, earnings revisions, technical context, and downside risk. These can be assembled into a traceable brief.
2. **Relevant, documented signals:** quality/profitability, value and momentum have substantial academic literature, enough to warrant an independently tested starting hypothesis. This does **not** warrant claiming persistent excess return for this implementation.
3. **The epistemic advantage:** a dated investment thesis with explicit counterevidence and falsification triggers is more auditable than an unexplained Buy label.
4. **Personal benefit before alpha:** even if every predictive signal fails, automation can reduce research time, improve coverage, detect stale information, and enforce a consistent review protocol.
5. **A legitimate path to useful decisions:** use sector-specific comparisons and valuation scenarios to prioritize diligence; then separate actual portfolio suitability from generic stock attractiveness in a secure, separately governed private workflow.
6. **Compounding internal knowledge:** immutable decisions, forecasts, thesis changes, and review outcomes create an auditable learning record. Continuous event-driven re-evaluation is more useful than a fresh top-ten list disconnected from prior decisions.
7. **No obligatory recommendation:** when no stock meets evidence and valuation standards, an empty shortlist is a correct product response.

### Evidence anchors, not proof of our forecast
- Asness/Frazzini/Pedersen, *Quality Minus Junk*: https://www.aqr.com/insights/research/working-paper/quality-minus-junk
- Asness/Moskowitz/Pedersen, *Value and Momentum Everywhere*: https://www.aqr.com/insights/research/journal-article/value-and-momentum-everywhere
- Kenneth French research data library: https://mba.tuck.dartmouth.edu/pages/Faculty/ken.french/data_library.html
- SPIVA U.S. Year-End 2025 (79% of U.S. large-cap active funds underperformed S&P 500 in 2025): https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2025/
- SEC EDGAR Company Facts and submissions: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- QuantConnect explanation of look-ahead bias: https://www.quantconnect.com/docs/v2/research-environment/datasets/key-concepts

## 2. Steelman the competing case first — "Do not build this"
**Best argument:** Existing, well-resourced platforms already solve screening, factor scoring, visualization, and some fair-value research. Building a free solution risks lower-quality data, uncalibrated quantitative forecasts, legal problems, and an illusion of rigor. The most efficient user outcome may be a disciplined workflow on an existing platform plus an investment journal. Active outperformance is difficult and persistent winners are rare.

**Response:** Agree. Do not build a generic clone. Establish a **build-versus-buy experiment** with a real workflow baseline. If our product does not substantially improve auditability and time-to-evidence over a low-cost existing tool, stop. Treat an API/orchestration layer over authorized third-party sources as a valid alternative.

**Gate BV-01:** compare a manual portal workflow (e.g. a free screener + SEC filings + template), a paid/reputable portal workflow, and our platform on the same 30 preselected companies and a blinded evaluation rubric.

**Stop condition:** do not invest in predictive AI if product research efficiency or factual correctness is inferior to a simpler workflow.

## 3. Reconstruct the strongest investment workflow
### Separate the decisions; do not collapse them into one score
A. **Discover:** which securities have enough evidence and unusual characteristics to review?  
B. **Assess business:** is financial quality resilient in its sector and cycle?  
C. **Assess expectations:** what future growth, margins, and reinvestment does the current price imply? Compare implied expectations to feasible scenarios, rather than asserting one point fair value.  
D. **Assess price and catalysts:** what change could cause the market to reassess the company? What observable event would disconfirm the thesis?  
E. **Assess downside:** what goes wrong in the adverse case, with liquidity, debt maturity, dilution, and business-specific risks considered?  
F. **Assess candidate quality:** independent data coverage, source time, valuation sensitivity and contradictory evidence.  
G. **Assess portfolio fit privately:** current exposures, correlation/concentration, loss capacity, investment horizon and tax situation. This is a separate product boundary requiring legal and privacy review before personalized advice.  
H. **Track and revisit:** record the original assumptions, catalysts and invalidation conditions; re-evaluate on material events and fixed intervals.  
I. **Audit outcomes:** compare decisions to risk-matched, sector-matched and broad-index baselines, incorporating all costs and appropriate timing.

### The specific value of an LLM
Not an oracle. It can be a **research coordinator and adversarial reviewer**:
- synthesize citations from authorized sources;
- independently articulate bull, bear and "nothing compelling" interpretations;
- identify assumptions, contradictions, unit errors and missing evidence;
- propose diligence questions and monitoring triggers;
- draft short explanations of an already computed score.
It cannot invent facts, choose strategy weights, change gates or issue trades. Treat company filings/news as untrusted data against prompt injection.

## 4. Three strengthening iterations
### Iteration A — strongest case for systematic factors
**Thesis:** sector-normalized quality, value, momentum and risk could rationally screen candidates and potentially improve research allocation.
**Strongest counterargument:** historical factor premia can be crowded, regime-sensitive, collinear or disappear; chosen 35/25/20/20 weights are arbitrary.
**Resolution:** initial weights remain an **explicit preregistered baseline**, not calibrated optimum. Run a fixed battery: each factor alone, equal weights, original weights, and a simple quality+value comparator. Use the same investable universe, timestamps and costs. Reject complexity if it adds no demonstrable value.
**New criteria:** AM-01, AM-02, AM-03.

### Iteration B — strongest case for AI
**Thesis:** grounded AI is an inexpensive, consistent adversarial analyst capable of accelerating research across hundreds of filings.
**Strongest counterargument:** persuasive hallucinations, omitted negative facts, data poisoning, prompt injection and hard-to-audit synthesis.
**Resolution:** the AI emits *typed evidence claims* with direct references to an immutable evidence ID and exact unit/period. Independent deterministic verification rejects unsupported quantitative assertions. The bear review cannot see the bull narrative until it independently selects potential contrary sources; compare claims after both are produced.
**New criteria:** AM-04, AM-05.

### Iteration C — strongest case for useful suggestions
**Thesis:** people want candidates, not just a huge dashboard. Give a small shortlist with actionable diligence questions and conditions for reassessment.
**Strongest counterargument:** users may treat "Top stock" as a personal buy instruction; an arbitrary top 10 rewards false positives and ignores suitability.
**Resolution:** label results "Research Candidate" rather than "Buy"; display universe size, as-of time, evidence confidence, adverse scenario, and "what would invalidate this". Permit zero candidates. Gate any personalized portfolio suggestion under separate approval.
**New criteria:** AM-06, AM-07, AM-08.

### Final adversarial reassessment
All three objections have specific planned controls and pass/fail verification methods. **The documentation is acceptable for implementation design.** It is not an implemented safety mechanism or evidence that the investment method beats its benchmark.

## 5. Strengthened requirements (v1.1 change request)
| ID | Priority | Requirement | Acceptance test |
|---|---|---|---|
| **AM-01** | P0 | Define separate user-value hypotheses: research efficiency, correctness/reproducibility, and investment predictive performance. Do not use predictive alpha as the only success measure. | Each hypothesis has a recorded baseline, threshold, experiment plan, and decision owner. |
| **AM-02** | P1 | Run the 30-company build-versus-buy pilot; compare to a disciplined free research workflow and one existing paid platform if available. | Measure total analyst minutes and blinded evidence correctness; retain all task logs. |
| **AM-03** | P1 | Register multiple benchmark models before backtesting: equal-weight factors, each single factor, original weighted factors, broad-market total-return, sector-matched, and a low-complexity reference. | One report per model using identical temporal universe, execution assumptions and holdout. |
| **AM-04** | P2 | Implement read-only bull/bear/neutral analysis from immutable evidence; require a typed source ID for each material assertion. | Adversarial corpus: unsupported numeric claims and prompt injections fail verification. |
| **AM-05** | P2 | Measure AI research assistance against a no-AI baseline: factual accuracy, omissions, citations, time saved, and error severity. | Predeclared thresholds; any critical fabricated financial assertion blocks publication. |
| **AM-06** | P1 | Implement the **Expectations Gap** research module: explicitly derive price-implied operational assumptions and compare with cited feasible scenarios. | At least three internally consistent scenarios; versioned units/discount rates and sensitivity analysis; absent data yields "not assessed". |
| **AM-07** | P1 | Implement a **Thesis Ledger**: timestamped initial thesis, positive/contrary evidence, catalysts, invalidation criteria, changes, reviews, and outcome. Historical entries immutable. | Reproduce prior thesis unmodified; trigger explicit change event when assumptions are revised. |
| **AM-08** | P1 | Provide an **Event-to-Thesis Monitor** for relevant new filings, earnings, debt changes, guidance revisions, material adverse risks, and invalidation triggers. No LLM-altered rank. | Idempotent event detection, correct time attribution, false-alert tracking, source-referenced change notice. |
| **AM-09** | P0 | Explicitly isolate generic ranking from personal portfolio fit and any trading. No personalized investment advice without approved product/legal review. | Attempted private portfolio ingestion in public pipeline is rejected. |
| **AM-10** | P1 | Track cost, calendar time, data coverage, human overrides and thesis accuracy; preserve a frozen baseline and cohort definition. | Monthly evaluation table with missing observations and changes disclosed. |
| **AM-11** | P1 | Disclose selection bias, factor exposures and investment concentration; include sector-neutral and size-adjusted comparisons. | A concentrated top-ten technology list receives a concentration warning and matched-factor baseline. |
| **AM-12** | P0 | Require **decision hygiene:** source-backed uncertainty, possible "none", changing conditions, and "next research action" rather than an unconditional recommendation. | Every candidate card shows downside and next verification step; no empty-provenance candidate. |
| **AM-13** | P1 | Compare performance against low-turnover rules and realistic post-publication execution costs; holdout remains frozen. | All results reproducible; regressions are not suppressed; complexity must earn its cost. |
| **AM-14** | P1 | Keep data licensing and operating-cost decision logs. Never assume public redistribution merely because a dataset has a free download. | Source with unknown rights blocks public release; cost table includes historical point-in-time coverage. |

### Metric design and release decisions
These are **proposed thresholds**, not measured achievements.

| Dimension | Candidate target | Why it matters |
|---|---|---|
| Analyst time | >=40% reduction in median time to a structured research brief compared with the baseline in AM-02 | Demonstrates usefulness independent of returns |
| Research correctness | 0 critical material factual errors in a double-reviewed pilot sample; report minor errors explicitly | Safety, not a guarantee of future zero errors |
| Provenance | 100% of quantitative assertions linked to raw source, units, availability time and transform version | Auditable results |
| Thesis coverage | >=95% of eligible analyzed companies have complete factor coverage or documented abstention | Prevents silent imputation |
| Historical replay | 100% deterministic replay for sampled dates and strategy versions | Reproducibility |
| Adversarial tests | All critical/high attack cases pass before any public nonprototype release | No knowingly unresolved high-severity failures |
| Investment advantage | **No target alpha assumed.** Statistical significance and economic significance required before claiming any outperformance | Reject promotional claims without evidence |
| Event monitor | >=95% of mandatory monitored filing events ingested in observation cohort, with latency/miss log | Useful ongoing research |
| Operational cost | Explicit monthly measured cost versus the free objective; scope cut rather than license violation | Sustainable operation |

**Do not treat a small pilot as proof of zero error rates or of positive expected returns.**

## 6. Build-versus-buy experiment
- **Cohort:** 30 companies across at least six nonfinancial sectors; stratified by market cap, profitability and data complexity, selected in advance. Preserve cases with weak evidence. Blind the evaluator to workflow.
- **Tasks:** identify 2 favorable facts, 2 unfavorable facts, valuation assumptions, source dates, risk flags, and 3 observable change triggers per company.
- **Arms:** A) free portal + SEC + manual checklist; B) reputable paid portal when licensed; C) proposed platform.
- **Measures:** human elapsed/active time, material factual errors, missing disclosures, provenance completeness, confidence calibration of human evaluators, cost, qualitative trust.
- **Decision:** proceed with a bespoke analysis engine only if C improves efficiency **without sacrificing evidence correctness**; otherwise orchestrate existing tools. Do not condition continuation on an unverified promise to beat S&P 500.

## 7. Architecture enhancement: evidence-first thesis intelligence
\`\`\`
Acquisition Ports (EDGAR + authorized EOD prices + events)
     |
Identity / PIT Timestamp / License / Corporate-action Data Quality
     |
Immutable Evidence Store + Evidence Graph (facts, claims, contradictions)
     |
Industry-Specific Quality + Price-Implied Expectations + Risk + Momentum
     |
Eligibility + Completeness Gates ---> No candidate / Abstain
     |
Research Priority Engine (versioned, testable and benchmarked)
     |
Thesis Ledger (initial claim + competing claim + invalidation triggers)
     |
Event-to-Thesis Monitor ----> Material-change alert + new version
     |
Read-only AI Evidence Explainer (optional, deterministic claim checker)
     |
Report Publisher (licensed noncommercial static research only)
     |
Research Evaluation + Benchmarks + Prospective Paper Log
\`\`\`

**Do not build** a generic real-time prediction AI, public portfolio storage, order execution, an ontology/graph database, or multi-agent autonomy as prerequisites. The first evidence graph can be a typed relational model. Add complex infrastructure only when a demonstrated bottleneck justifies it.

## 8. Concrete example: correct output semantics
**Hypothetical illustration — not a real security or quote.**
ACME has growing free cash flow and improving operating margins, but at its current assumed price the implied future margin is higher than its historical observed range. The technical trend is positive. The balance sheet has a debt maturity within 18 months. The system therefore logs:
- Research status: **MONITOR / NOT YET A CANDIDATE**.
- Strength: Improving cash generation.
- Contradiction: Price assumes optimistic future margins, debt refinancing uncertainty.
- Evidence confidence: HIGH *only if source coverage and lineage are complete*; confidence does not imply a likely positive return.
- Thesis change trigger: next earnings release, refinancing disclosure, material valuation change.
- Next research action: reconcile refinancing capacity and operating margin assumptions.
- Investment action: **NONE**.

This is valuable research output, even when the result is no stock to buy.

## 9. Exit criteria for the steelman stage
| Gate | Design status | Verification status |
|---|---|---|
| Strongest product hypothesis stated with alternative comparison | PASS | Pilot pending |
| Objections to systematic signals answered with falsifiable tests | PASS | Backtest pending |
| Objections to LLM answered by independent fact-validation contract | PASS | Adversarial code tests pending |
| User-facing candidate usefulness balanced against abstention | PASS | Usability tests pending |
| Explicit sourcing/licensing/legal boundaries | PASS | Provider/legal sign-off pending |
| Better-than-competitor claims | NOT MADE | No measured evidence |
| Predictive edge / investment recommendation | NOT CLAIMED | No measured evidence |

**Design decision:** Accept v1.1 steelman as the preferred engineering hypothesis. Retain the original v1.0 baseline. Do not assert alpha, safety certification, or production readiness.
