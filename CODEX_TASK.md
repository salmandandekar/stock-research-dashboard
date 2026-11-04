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
