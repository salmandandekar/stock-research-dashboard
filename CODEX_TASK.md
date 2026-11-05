# Codex Implementation Brief — Stock Intelligence Platform v1

## Governing documents
Before any code change, read:
1. AGENTS.md
2. docs/PRODUCT_REQUIREMENTS.md — BRD/FRS, architecture, gates and acceptance matrix
3. docs/ADVERSARIAL_REVIEW.md — attack cases, red-team tests, exit criteria
4. docs/COMPETITOR_BENCHMARK.md — competitor inspirations, not reusable proprietary implementations

**Decision:** The original five-indicator score remains an experimental technical screen. It is not a validated Buy/Sell recommendation, and the project must never claim it predicts price appreciation.

## First implementation PR: data governance and temporal correctness
- Define typed, immutable domain schemas for Security, Observation, SourceLicense, Evidence, ResearchResult and StrategyVersion (no third-party provider imports inside domain).
- Write a signed-off source-rights configuration framework with per-provider allowed uses and blocking public publication. Default unknown permissions to "disallowed" for publication. Do not invent actual licenses.
- Implement date-aware exchange calendar, stale data checks, corporate-action anomaly checks and symbol/CIK identity as far as supported by available data.
- Change ranking output to explicitly report evaluated universe, eligible count, exclusion reasons, as-of timestamps and Research Priority Score (not expected return). Add \`INSUFFICIENT_EVIDENCE\` and \`NO_CANDIDATES\` states.
- Add red-team tests RT-01/02/09/10/13/16/17/18 and acceptance tests T-001/T-003/T-004/T-005/T-009/T-010/T-012/T-014/T-015.
- Keep old dashboard publishing stable unless public data rights are unverified: prefer fail-closed publication, explain the status in HTML rather than exposing unauthorized data.
- Preserve CI; run tests, lint/compile and show actual outputs. Do not merge automatically.

## Subsequent PRs
1. SEC EDGAR adapter with caching, CIK matching, fiscal period alignment and publication timestamps.
2. Fundamental-quality metrics with sector-specific applicability.
3. Explicit valuation scenario model and risk gates.
4. Evidence + counterevidence detail UI.
5. Point-in-time backtesting with delistings, costs, historical universe, untouched holdout, uncertainty reporting.
6. Prospective paper monitoring, reporting and optional read-only AI explanation after factual-verification gates.

## Explicit release restrictions
- No trading API or order placement.
- No personalized portfolio advice or private account data on public GitHub Pages.
- No commercial SaaS deployment on GitHub Pages.
- No vendor score scraping, unlicensed quotes or analyst estimates.
- No claim of superior investment performance until independently reproducible tests demonstrate it; failure remains visible.
- Any critical/high red-team defect blocks release.

Open each change as a pull request against main with requirements IDs, tests, known limitations and deployment notes. **Do not claim all release gates passed from tests that have not been run.**


## Steelman v1.1 mandatory engineering update
Read `docs/STEELMAN_REVIEW.md` before work. Implement the following in a staged, reviewable way:
- AM-01 and AM-12: measure a no-AI baseline, enforce candidate abstention, show contradictory evidence and a specific next diligence action.
- AM-02: design the build-versus-buy 30-company pilot, including immutable cohort, human time, factual accuracy and licensing cost. Do not claim it has run until independently recorded.
- AM-06: add sector-specific price-implied-expectations and internally consistent bear/base/bull scenarios when licensed data and the fundamentals model are ready.
- AM-07/08: introduce a timestamped Thesis Ledger and an event-to-thesis reassessment process, not repeated uncontextualized daily Buy labels.
- AM-03/11/13: benchmark all strategies against simple factors, broad and sector-matched baselines with identical point-in-time data and costs.
- AM-04/05: optional read-only AI bull/bear reviewer; source-ground every material assertion and compare effectiveness to a no-AI baseline.
- AM-09/14: public license and private-portfolio boundaries fail closed.
- Deliver one narrow PR per independently testable capability. Never mark red-team or alpha gates complete based solely on documentation.

## Additional governed implementation scope — v1.2 short-term opportunity scanner

Read `docs/SHORT_TERM_OPPORTUNITY_REQUIREMENTS.md` and `config/short_term_strategy.example.json`. The example configuration is disabled by default and MUST NOT be treated as live functionality.

**First coding deliverable after source and provenance foundation:** Add a market-wide eligible universe abstraction and 1–5-day batch *swing research* evaluator. Keep intraday live mode disabled. Implement separately versioned horizon IDs, deterministic net-of-cost cost simulation, explicit NO_TRADE and NOT_VALIDATED states, expiry and evidence timestamps, and reproducible acceptance tests ST-T01, ST-T03, ST-T06, ST-T16, ST-T17 and ST-T18.

**Subsequent PR:** Build realistic point-in-time fill simulation, original signal records, corporate-action and same-candle ambiguity safeguards, historical delistings, benchmark+regime evaluation, and holdout. Add ST-T02/05/09/10/12/13/19/20/21.

**Later PR:** Add delayed historical minute-bar integration with provider/venue/latency/cost and licensing safeguards. Live intraday research requires a separate, monitored, licensed streaming runtime, not GitHub Pages alone. Add ST-T04/07/08/11/14/15/22.

Never label research results as "Buy now" or "profitable" without appropriate evidence and legal/product approvals. Returns may be negative. Never create order execution. Do not merge implementation PRs automatically; report real test outputs and unresolved data rights.


## Steelman v1.2a implementation constraints

Read `docs/SHORT_TERM_STEELMAN.md`. New requirements ST-SM-01..16 and tests SM-T01..16 strengthen the already proposed v1.2 requirements.

- Implement a `MechanismRegistry` with immutable versions, feature availability timestamps, experiment budget, expected holding horizon, causal rationale, and predefined falsifiers. No mechanism => research only, never "validated".
- Initial MVP: **one versioned daily EOD swing research hypothesis** with a clearly defined eligible universe, baseline, conservative next-available execution costs, rejected/unfilled cases, NO_TRADE, and source-rights gates.
- Validate a minimum simple counterfactual (no-trade/cash and low-complexity time-matched strategy). Test net expectancy, downside tails, sample dependence and 2x cost stress before adding complexity.
- Maintain a ledger of **all** emitted and withheld candidate signals, their original timestamps, source IDs, strategy version, state and eventual observed outcome. Include no-trade days and expiry.
- Keep academic intraday patterns as test hypotheses; they do not transfer automatically from ETFs or older market samples to 2026 US equities. Never claim guaranteed returns or daily profit.
- Before any live signal work: require authorized full-market data or explicitly limited-coverage semantics, continuous session worker, latency/error monitoring, realistic fill evaluation, and a separate reviewed release. Keep automated orders and tailored advice out of scope.

Each implementation PR must cite linked ST/ST-SM requirement IDs, include adversarial fixture tests, record benchmark comparisons, and disclose negative outcomes.
