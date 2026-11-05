# Multi-Horizon Opportunity Discovery — Requirements v1.2
**Revision:** 1.2 / 2026-11-04  
**Status:** DESIGN ACCEPTABLE FOR IMPLEMENTATION; NOT VALIDATED FOR PROFITABILITY OR RELEASE AS TRADING ADVICE  
**Extends:** PRODUCT_REQUIREMENTS.md v1.0/v1.1, STEELMAN_REVIEW.md, ADVERSARIAL_REVIEW.md, CODEX_TASK.md  
**Decision owner:** Product owner; validation: independent data reviewer + quantitative methodology reviewer + security/legal sign-offs before live or public use.

## 1. User goal and precise interpretation
The user wants the system to **find previously unspecified stocks** with potentially attractive returns, including the potential to capitalize on fluctuations *within one trading day*. A five-name watchlist is not broad-market discovery. A high-volatility ranking is not a profitable opportunity ranking.

**Core BR-STD-01:** The platform SHALL independently discover and evaluate candidate stocks across an explicitly disclosed eligible universe for three distinct horizons:
1. **Intraday:** one regular trading session, research events in 5–60-minute windows, no overnight position by default.
2. **Swing:** 1–5 trading days; holds may experience overnight gaps.
3. **Position:** 20–252+ trading days, handled by the existing fundamental research design.

For each horizon, the engine SHALL report the economic basis of an opportunity, source time, plausible entry/exit assumptions, transaction costs, downside, uncertainty, expected holding period and invalidation conditions. **No qualifying opportunities** is an acceptable successful output.

**Do not promise "good returns"**. Operational success is *discovering candidates that had a measurable, out-of-sample, risk-adjusted positive expected net edge under realistic fill assumptions*, while allowing abstention. Even validated historical edge does not establish any particular trade will profit.

## 2. Definitions: avoid false confidence
- **Volatility:** amount of price movement. It is NOT directional accuracy, profit or an edge.
- **Gross hypothetical return:** raw assumed entry-to-exit percentage before costs.
- **Round-trip cost:** explicit buy/sell spread, slippage/market impact, commissions, regulatory fees, funding/borrow where applicable, and taxes shown separately because taxes depend on the person.
- **Net hypothetical trade return:** gross return less modeled executable costs. Store the fill model and timestamp; no midquote fills unless explicitly justified.
- **Expected net edge (conditional expectancy):** E[net P&L per eligible executed simulated trade], estimated strictly from eligible historical data and with a confidence/uncertainty interval. A high win rate does not alone prove positive expectancy.
- **Drawdown and tail loss:** maximum observed capital loss and adverse scenario stress, not guaranteed maximum future loss.
- **Signal vs trade:** a research signal is a model output. A trade requires a separate trading decision and executable order. Phase 1 has no orders, broker API, or personalized position sizing.
- **Signal time:** instant features and evidence were actually available. **Decision time** follows signal time. **Fill time** follows decision time plus conservative latency. **Published time** may be later still.
- **Data delay/coverage:** exchange feed scope and real-time entitlement are not interchangeable. Delayed data MUST NOT be labeled real-time or produce "enter now" calls.
- **Confidence:** evidence coverage/calibration, **not** a guaranteed chance of profit.

## 3. Socratic reasoning — repeated challenge and resolution
### Loop 1: What counts as a good opportunity?
**Question:** A stock moves 8% every day. Can we profit?  
**Challenge:** It can move the wrong way, gap unexpectedly and cost too much to trade.  
**Correction:** Require positive risk-adjusted net expectancy *as a hypothesis backed by independent data*, appropriate liquidity, controlled loss estimates, and explicit uncertainty.  
**Acceptance:** A high-volatility negative-expectancy stock fails selection. See ST-T01.

### Loop 2: Can an algorithm exploit a historical chart?
**Question:** If a backtest wins 80%, is it useful?  
**Challenge:** Look-ahead, hindsight pivots, survivorship, open/close execution ambiguity, repeated parameter search and missing failed orders can manufacture wins.  
**Correction:** Freeze market features as-of, simulate post-signal bid/ask execution with costs, include delistings and false signals, use purged walk-forward splits and untouched holdout, preserve failures.  
**Acceptance:** Data revisions and same-bar stop/target collisions cannot create free profits. See ST-T02/03/05/10.

### Loop 3: Can a free daily website offer live intraday trades?
**Question:** Can a 4 PM scheduled job select a 10:20 AM move?  
**Challenge:** No. GitHub Actions scheduler is not a low-latency continuous stream, and free feeds can be partial or 15-minute delayed.  
**Correction:** Split **daily swing discovery** (free, batch) from **intraday research** (timestamped delayed or licensed real-time service with health checks and market-session monitoring). Static hosting is a report reader, not a real-time signal engine.  
**Acceptance:** Stale/delayed signals have no live-entry affordance. ST-T04/08/11.

### Loop 4: Should the system suggest a trade every day?
**Question:** How will a person profit if the scanner returns no stocks?  
**Challenge:** Forced picks inflate churn and risk. No trade is rational when the evidence or net expectancy is insufficient.  
**Correction:** Distinguish discovered, qualified, invalidated and abstained candidates; permit an empty shortlist; make costs/uncertainty and human review mandatory before any live order integration.  
**Acceptance:** Zero-trade and data-outage scenarios return explicit states and an auditable reason. ST-T06/07.

**Resolution:** The requirement is feasible as **evidence-backed opportunity discovery**, not as a profitable-trades guarantee or an unattended live trading bot.

## 4. Functional requirements, strict and testable
Priority P0: foundational blocker. P1: first feature in its relevant milestone. P2: future validated expansion.

### 4.1 Discovery and market data
| ID | Priority | SHALL requirement | Verification |
|---|---|---|---|
| ST-01 | P0 | Keep independent strategy IDs for intraday, 1–5-day swing and long-horizon investing. Store explicit expected holding period and timing assumptions. | Cross-horizon test never combines factor scores or performance histories. |
| ST-02 | P0 | Support **market-wide discovery**, not only user watchlist. Materialize and disclose scanned universe, eligible set, excluded instruments, source coverage and scan time. | Test sees candidates outside five default tickers; coverage counters reconcile exactly. |
| ST-03 | P1 | Apply liquidity eligibility: exchange/listing/share class; price, market cap when available, 20-day dollar ADV, spread, depth/quote activity where available, trade halts and recent corporate actions. All limits versioned. | Illiquid/large-spread stock is rejected with reason. |
| ST-04 | P0 | For all intraday bars, store source exchange/feed type, quote/bar timestamp, ingestion timestamp, timezone, adjustment basis, latency, data rights, session type, and full/partial-market coverage indicator. | Missing critical metadata blocks publication of a live-style research signal. |
| ST-05 | P0 | Implement explicit source policy for each data provider: personal research, live use, redistribution, retention, commercial rights, display and quotes. Unknown => deny for public release. | Unlicensed raw quotes/bars cannot be exported to public GitHub Pages. |
| ST-06 | P1 | Detect splits, reverse splits, dividends, halts, LULD pauses, stale quotes, crossed/locked quotes, abnormal spreads, broken high/low/volume bars, premarket/after-hours session mismatch and source gaps. | Malformed data is quarantined before feature computation. |
| ST-07 | P1 | Support session-aware America/New_York exchange calendars, DST changes, early closes, market holidays, scheduled earnings and major news/event timestamp availability. | Market closure and early-close tests do not produce false fresh signals. |
| ST-08 | P1 | Define opportunity types as **hypotheses**: momentum/breakout, mean reversion, opening-gap follow-through/fade, event-driven volatility, and multi-day swing. Each gets separate registration, risk rules and validation. | Scanner can disable each hypothesis and disclose its definition; no unsupported indicator becomes a recommendation. |
| ST-09 | P0 | Never imply that a delayed, partial-market, failed, or stale feed is real-time. Gate display of "live" signals on verified entitlement, full required market coverage, uptime and latency. | IEX-only, 15-minute delayed or disconnected feed triggers a visible downgrade/abstention. |

### 4.2 Economic opportunity and risk
| ID | Priority | SHALL requirement | Verification |
|---|---|---|---|
| ST-10 | P0 | Keep **price movement magnitude**, **forecast direction**, **expected NET edge**, **risk**, **evidence confidence** and **liquidity** as distinct measures. Never equate large movement or 100-point screening score with profit probability. | A 7% volatility candidate with negative modeled edge fails qualification. |
| ST-11 | P1 | For each prospective setup specify signal time, allowed entry window, exit horizon, target/stop hypotheses, invalidation, catalyst, allowed session and eligible order assumptions. Record as research scenario, not an executable order. | Deterministic schema validation; no implied fill at signal-bar close unless next-price opportunity existed. |
| ST-12 | P0 | Calculate and show gross potential return, modeled round-trip spread, slippage, commission/fees, and **net** return; display uncertainty/sensitivity and estimated holding period. Include borrow/financing only if relevant and supported. Taxes displayed as separate unmodeled user-specific factor. | Increasing transaction costs can turn a positive gross signal into No Trade. |
| ST-13 | P1 | Quantify downside: realized and stress volatility, worst observed loss, MAE/MFE, peak-to-trough drawdown, overnight gap for swing, expected shortfall when sample suffices, correlation/clustering, and exposure concentration. | Tail-risk stress blocks or downgrades setup, not falsely "safe" stop guaranteed. |
| ST-14 | P1 | Implement deterministic opportunity states: DISCOVERED, RESEARCH_CANDIDATE, NOT_VALIDATED, INSUFFICIENT_EVIDENCE, STALE, DISQUALIFIED, NO_TRADE, EXPIRED. State transitions and reasons are persisted. | No candidate, invalid data, expired event, or failed holdout cannot produce entry-ready suggestions. |
| ST-15 | P0 | No trades, position sizes tailored to user finances, margin, shorts, options or leverage in the research product. Any broker/portfolio connection is a separate, opt-in and legally reviewed product boundary. | No executable order endpoint or broker credentials in app/site. |
| ST-16 | P1 | Version strategy thresholds, features, labels, outcome horizon, fill models, benchmark, maximum loss policies and optimization experiments. Define simulated risk budget examples, not personal advice. | Replays same data/version to exactly same report. |

### 4.3 Quantitative validation and falsification
| ID | Priority | SHALL requirement | Verification |
|---|---|---|---|
| ST-17 | P0 | Train and test with point-in-time universe and features; signals available before simulated execution; no same-bar future highs/lows. Use purging/embargo with overlapping horizons and never tune to untouched test data. | Injected future feature is detected and blocked. |
| ST-18 | P0 | Use a **realistic executable fill model** (post-signal bid/ask + configurable latency, spread, slippage, order fees, unfilled orders, gaps, liquidity, market impact). Conservatively resolve same-bar target/stop ambiguity or refuse to infer a fill without tick/quote data. | Profit cannot be created from midpoint, same-candle hindsight, missing liquidity or impossible price. |
| ST-19 | P1 | Benchmark against cash/no trade, buy-and-hold market/sector reference, random matched-liquidity/volatility candidate selection, and simple nonoptimized momentum/mean-reversion rules using identical costs and trade clocks. | Published reports include all baselines and negative results. |
| ST-20 | P1 | Disclose net expectancy per executed trade, compounded portfolio return with assumptions, payoff ratio, win rate, profit factor, Sharpe/Sortino where appropriate, maximum drawdown, tail losses, turnover, capacity, rejected/unfilled orders, sample size, regime and parameter sensitivity, confidence intervals and multiple-testing burden. | Report clearly distinguishes win rate from expectancy and avoids spurious statistically precise claims. |
| ST-21 | P1 | Require chronological walk-forward out-of-sample testing, locked final holdout, instrument/sector/regime splits, bootstrapped uncertainty, costs stress (e.g. 2x estimated slippage/spreads) and documented hypothesis search budget. | Strategy failure blocks "validated" labels and remains visible in audit. |
| ST-22 | P1 | Run prospective **paper-only** tracking before any live-trade-ready claim; minimum design target 60 trading sessions and 200 independent executed simulated outcomes, with regime limits reported. Neither target alone proves a future edge. | Signal timestamps precede outcomes; misses, zero-trade days and comparison baselines retained. |
| ST-23 | P0 | If net expected edge is nonpositive or cannot be credibly estimated, return NOT_VALIDATED/NO_TRADE. Do not fill ranking slots or forecast a success probability without calibration evidence. | No-edge data, high slippage and sparse sample tests produce abstention. |

### 4.4 UI, orchestration, event monitoring, human-in-the-loop
| ID | Priority | SHALL requirement | Verification |
|---|---|---|---|
| ST-24 | P1 | Dashboard has **separate Intraday / Swing / Long-term tabs**; each states delay, data coverage, generated time, risk, candidate count, thesis and invalidation conditions. Never publish a mixed-horizon "best stock" score. | UI scenario tests with 3 independent opportunity records. |
| ST-25 | P1 | An evidence record links each signal to raw source snapshots, feature definitions, execution model, software SHA, strategy SHA, and market/decision/publication timestamps. Revision is append-only. | Replay an original signal without rewriting its expected results. |
| ST-26 | P1 | GitHub Actions batch may generate swing screens and overnight research only. Intraday monitoring requires a separate reliable session-aware worker with continuous data, queuing, error handling and broker-independent clock; public GitHub Pages remains a static reader of permitted snapshots. | A paused, delayed or disconnected worker never displays "active live opportunity." |
| ST-27 | P1 | Report candidates with possible economic edge, expected movement and **net** uncertainty, favorable/unfavorable rationale, evidence quality, data latency, horizon, expiry, next diligence action and "No Trade" alternatives. | Every ranked result includes contrary evidence and no guarantee language. |
| ST-28 | P1 | Human reviewer can accept/reject the research **for tracking**, annotate rationale and monitor results; no action executes a trade. Track overrides and human false positives. | Review event auditable; cannot write orders or alter historical model output. |
| ST-29 | P1 | Monitor signal expiry, news/earnings, changing spread/liquidity, trading halt, data drop, invalidation condition and material new risk; withdraw old signals, do not silently refresh old prices. | Expiration and halt produce appropriate state and alert. |
| ST-30 | P0 | Provide disclosure of active trading risks and broker-specific restrictions. FINRA replaced traditional PDT rules with intraday margin standards effective 2026-06-04, with transition through 2027-10-20; a broker may still apply old requirements during transition. Cash account settlement/tax rules need separate checks. | No false universal claim that a $25,000 PDT minimum always applies or never applies. Broker rules not inferred. |
| ST-31 | P1 | Public report must never publish account sizes, broker identities, private trade logs, personal strategy credentials or licensed raw market data without redistribution permission. | Artifact scan/test blocks prohibited data. |
| ST-32 | P2 | After data and evaluation gates, optional AI may create bull/bear summaries and event questions only from evidence IDs. No autonomous profit forecasts, orders, optimized stop levels or changes to model policy. | Prompt injection and hallucinated price claims fail typed validation. |

## 5. Required data and modeling choices
- Universe initially **US-listed common shares**; liquid ETFs may be used as benchmarks, not default recommendation candidates. Exclude OTC, low-float/penny stocks and thin markets until specific risk models are validated.
- Illustrative *starting filters for experimental tests only*: last price >= $5, 20-session average daily dollar turnover >= $20 million, 20-day median quoted spread <= 20 basis points, and valid primary listing. Tune only within preregistered training data, not test outcome. Values are not universal suitable-investment thresholds.
- For opening breakout or gap signals, constrain premarket versus regular-hours features. A market-on-open simulated fill must not use that day's opening price after knowing its intraday path.
- For swing trades, include overnight gap and earnings risk. The 1–5-day horizon cannot share the intraday same-session fill model.
- For any probability claim, specify the *event* (e.g., net positive return within H), training period, calibration method and interval. Without calibrated holdout evidence show "probability not established".
- Research setup outputs are **scenarios**, not personal price targets, purchase instructions or a guarantee. State where a live price is unknown.

## 6. Implementation modes and data-entitlement reality
### Mode A — Batch swing screen: feasible with current stack
- Daily EOD workflow ranks 1–5 session research ideas with last-available close, risk, likely calendar events, estimated *historical* net expectancy, and source references.
- The next-session trade clock is explicit; never imply a next-day executable price equals prior close.
- Existing public GitHub Pages can show only authorized derived research fields. If licenses are unverified, block public output.
- **Label:** "End-of-day research", not live trades.

### Mode B — Delayed intraday research
- Use permitted minute-bar historical snapshots for 5–60-minute pattern study and retrospective alerts.
- Alpaca free Basic supports limited real-time IEX and older-than-15-minute SIP history per documentation; IEX-only is partial market, not equivalent to full SIP. Provider terms and actual user entitlement must be validated separately.
- Mark "delayed" and disable "enter now" recommendations.

### Mode C — Real-time intraday research (future separate service)
- Use authorized consolidated quotes, exchange coverage, specified latency SLO, monitored worker with reliable market-session uptime, and persistent event storage.
- May require paid feed / hosting and a distinct private application. Public GitHub Pages alone cannot host the running signal engine. Never claim $0 without validating costs and rights.
- Begin **paper only**. No autonomous broker orders; legal/suitability and account workflow outside original scope.

**Research source options (nonexclusive):**
- Alpaca market data docs: https://docs.alpaca.markets/us/docs/about-market-data-api ; https://docs.alpaca.markets/us/docs/market-data-faq
- Massive (Polygon successor), free EOD/paid delayed/realtime tiers; personal vs public terms: https://massive.com/stocks
- FINRA new intraday margin rule transition: https://syndication.finra.org/content/understanding-new-intraday-margin-requirements
- SEC day trading risks: https://www.investor.gov/additional-resources/spotlight/formerdirectorlorischock-directors-take/thinking-day-trading-know-risks

## 7. Signals and contracts
### 7.1 Signal lifecycle
\`DISCOVERED -> (INSUFFICIENT_EVIDENCE | DISQUALIFIED | NOT_VALIDATED | RESEARCH_CANDIDATE) -> (EXPIRED | WITHDRAWN)\`.
\`NO_TRADE\` is a report-level result if the horizon has zero qualifying candidates.
Changes after publication create a new immutable record; do not overwrite past candidates.

### 7.2 Minimum typed payload (illustration, NOT a live signal)
\`\`\`json
{
  "schema_version": "1.2",
  "symbol": "EXAMPLE",
  "security_id": "US:EXCHANGE:PERMANENT_ID",
  "research_horizon": "SWING_1_TO_5_DAYS",
  "strategy_id": "swing-momentum-v0-experimental",
  "market_source_id": "provider-feed-license-version",
  "coverage": "EOD_US_EQUITIES",
  "market_data_asof": "2026-11-04T16:00:00-05:00",
  "features_available_at": "2026-11-04T21:15:00Z",
  "signal_created_at": "2026-11-04T21:20:00Z",
  "expires_at": "2026-11-05T16:00:00-05:00",
  "state": "NOT_VALIDATED",
  "signal_description": "hypothesis-only, not a trade instruction",
  "historical_net_expectancy": null,
  "expected_net_return_interval": null,
  "execution_cost_model_id": null,
  "out_of_sample_validation_id": null,
  "liquidity_gate": "UNVERIFIED",
  "risk_gates": ["VALIDATION_NOT_COMPLETE"],
  "supporting_evidence_ids": [],
  "contrary_evidence_ids": [],
  "potential_entry_scenario": null,
  "invalidation_trigger": "No reliable evidence yet",
  "investment_action": "NONE"
}
\`\`\`
Exact date fields are examples. All real records take times from source receipts and deterministic run clocks.

## 8. Red team in repeated loops
### Round A — Financial edge
| Scenario | Attack/Failure | Fix | Test |
|---|---|---|---|
| Volatility trap | 10% daily move but negative after costs | Separate magnitude and net edge gates | ST-T01 |
| Spread/impact trap | "Profit" smaller than spread and exit slippage | Round-trip cost and 2x cost stress | ST-T03 |
| High win-rate trap | Many tiny wins plus rare huge losses | Payoff, tail risk, drawdown, expected shortfall | ST-T09 |
| Churn / fee trap | Many trades exhaust capital via costs | Realistic turnover, rejected fills, capacity | ST-T09 |

### Round B — Temporal and backtest integrity
| Scenario | Attack/Failure | Fix | Test |
|---|---|---|---|
| Candle hindsight | Entry at low, exit at high of same bar | Execution after feature cutoff; prohibit same-bar high/low fills | ST-T02 |
| Target + stop touched same OHLC bar | Assumes winning order without knowing sequence | Use ticks or worst-case/ambiguous-unfilled rule | ST-T10 |
| Data snooping | Repeatedly retune on test results | Experiment ledger and immutable holdout | ST-T05 |
| Survivorship | Failed companies disappear | As-of universe + delistings | ST-T05 |
| Corporate action leakage | Future split adjusted history used wrongly | Versioned as-of data and adjusted/unadjusted metadata | ST-T12 |
| Overnight gap | Stop assumed guaranteed even after gap | Gap-aware downside simulator | ST-T13 |

### Round C — Data, runtime and human risk
| Scenario | Attack/Failure | Fix | Test |
|---|---|---|---|
| Delayed data sold as live | User enters after move already ended | Feed/latency gate + UI downgrade | ST-T04 |
| IEX sample treated as full market | Missing venue liquidity/quotes | Coverage label and conservative qualification | ST-T08 |
| Trading halt or feed outage | Stale "act now" candidate | Circuit breaker, expiration and explicit state | ST-T07 |
| AI fabricates a price target | False precision and user loss | Evidence-only read-only model, typed checks | ST-T14 |
| Trading compliance misconception | Wrong assumption about margin/PDT limits | Broker-specific transition-state disclosure | ST-T15 |
| Private account or licensed data leak | Security/licensing harm | Public artifact scanning and publication deny | ST-T11 |

### Round D — Human-in-the-loop challenge
1. **Product owner** reviews whether the output fulfills short-term opportunity *discovery*, not a promise of profit; signs off on three horizons and No Trade.
2. **Quantitative reviewer** replays an unexpected top-ranked signal, independently checks all costs/fills, and demands an untouched holdout.
3. **Data engineer** verifies venue coverage, availability and rights; challenges any free-data "real-time" assertion.
4. **Security/legal reviewer** challenges public distribution, autonomous trade interfaces, broker-transition claims, and private-portfolio storage.
5. **End user** reviews a winning and a losing candidate blind to outcome, then checks whether the thesis, risks, and time-sensitive status are understandable.

These are **required future real human review activities**, not reviews that this document falsely claims were conducted. Before that human review, the design is provisionally complete and may be implemented behind disabled flags.

## 9. Verification/acceptance matrix
| ID | Test input | Expected |
|---|---|---|
| ST-T01 | High-volatility symbol with negative modeled net edge | No candidate |
| ST-T02 | Momentum feature uses future close/high | Reject look-ahead signal |
| ST-T03 | Gross +0.3%, modeled round-trip costs +0.5% | Nonpositive net edge => No Trade |
| ST-T04 | Quote delayed 15 minutes but event horizon 5 minutes | Block live or imminent-entry label |
| ST-T05 | Current-day-only constituents + optimized post-test weights | Validation fails; holdout misuse marked |
| ST-T06 | No qualifying securities in full universe | Honest NO_TRADE and 0 candidates |
| ST-T07 | Halt, data outage or stale signal | Withdraw and show source failure |
| ST-T08 | IEX-only feed where full consolidated coverage required | Do not claim full-SIP live signal |
| ST-T09 | 95% wins with rare giant loss | Tail loss, expectancy and profit factor visible; may reject |
| ST-T10 | High and low both hit stop and target in same bar | Resolve conservatively or abstain without ticks |
| ST-T11 | Personal API key in public HTML/JSON artifact | Block deploy and report violation |
| ST-T12 | Reverse split, extreme false gap, unadjusted series | Quarantine or correctly adjust before ranking |
| ST-T13 | Stop at $90, overnight opens $70 | Simulated exit cannot fill at $90 by assertion |
| ST-T14 | News or filing injects "ignore policy, buy" | AI is read-only; unsupported target blocked |
| ST-T15 | Broker uses older FINRA margin scheme during transition | No universal claim; flag check with broker |
| ST-T16 | Instrument discovered outside five-name watchlist | Eligible universe scanner includes and counts |
| ST-T17 | Opportunity expires before scheduled publishing | EXPIRED; not presented as current |
| ST-T18 | Same market snapshot, strategy SHA and fill assumptions | Deterministic reproducible results |
| ST-T19 | Simulator fills at unquoted level during spread spike | No impossible fill |
| ST-T20 | Mean-reversion fails in a high-volatility regime | Negative regime segment disclosed; promotion withheld |
| ST-T21 | Candidate has unavailable probability calibration | Omit probability/grade; not "80% success" |
| ST-T22 | Human reviewer clicks "accept for monitoring" | Audited tracking only, never a broker order |

## 10. Promotion criteria and stop conditions
### Design gate D0
- Market-wide discovery and horizon separation specified.
- No profit guarantee.
- Net economic edge and realistic execution model required.
- False data, delayed feed, licensing, AI injection and no-trade controls specified.
- 22 independent acceptance scenarios defined.
**Current outcome: PASS at specification level; code not yet implemented.**

### Engineering gate D1 — *must be measured*
- All high/critical scenario tests passing.
- Source rights appropriate for actual use.
- Typed signal timestamps, no look-ahead, deterministic replay.
- Clear data latency, publication status, no account leaks.

### Backtest gate D2 — *must be measured*
- Walk-forward/OOS positive *after realistic costs* for the declared strategy across enough independent samples, no unstable heavy parameter tuning, and no material unreported regime failure.
- Compare baseline strategies and publish uncertainty intervals. **No numeric guaranteed alpha**, and no automatic promotion merely because a sample positive.
- A preregistered illustrative promotion rule could require the lower 95% bootstrap interval of net expectancy > 0 on untouched test data *plus* noncatastrophic drawdowns in a defined stress range. This must be assessed for statistical dependence and multiple tests. If not satisfied, mark NOT_VALIDATED.

### Paper gate D3 — *must be measured*
- Minimum **60 trading sessions** and **200 independent simulated trades** per promoted strategy with every alert recorded before outcomes, plus realistic fill timing, transaction costs and missed alerts. If one condition is not achieved, continue observation; these minima do not prove cross-regime robustness.
- Trading regulations and exchange-data rights independently confirmed before live execution readiness.

### Human gate D4 — *must be performed*
- Quant, data, security/legal and actual user reviews; accepted negative/positive examples.
- Do not deploy a brokerage connection or call a trade actionable merely because model testing passed.

### Stop conditions
- Negative net OOS expectancy under realistic costs.
- Severe unquantified tail loss or transaction-cost sensitivity.
- Unlicensed public data; poor coverage; unknown freshness.
- Material backtest leakage, false outperformance claim or expired signals.
- No demonstrated product benefit over a simple baseline.

The system **must remain useful when there is no opportunity**: report how many securities were screened, why candidates failed, market/strategy conditions, and which factors would change the assessment.

## 11. Build sequence (Codex)
1. **ST-M1 / Batch swing:** Build eligible market-wide universe loader, data-rights manifest, 1–5-day swing hypothesis, net transaction cost model, NO_TRADE states, source-timestamped reporting and unit tests. No "live intraday" label. Preserve v1.1 fundamental roadmap.
2. **ST-M2 / Backtest:** Point-in-time execution simulator with bid/ask and conservative OHLC fallback, spreads, fees, slippage, regime splits, historical universe and costs; preregister results and run ST-T01..22.
3. **ST-M3 / Delayed intraday R&D:** Historical minute data adapter behind license gate, event-catalyst features, latency/venue coverage, 5–60-minute hypothesis evaluation; research-only.
4. **ST-M4 / Live paper monitoring:** Only if licensed comprehensive feed and always-on runtime approved; timestamped real-time observation, explicit server-side eligibility and status expiry. Paper-only; no orders.
5. **ST-M5 / Human pilot and potential future advisory/trading scope:** Only after D1–D4; build-versus-buy validation and separate legal/product review.

Do not start with a prediction-focused LLM or optimize aggressive return targets before establishing actual executable data and a credible benchmark.

## 12. Primary references
- SEC: Day-trading risk: https://www.investor.gov/additional-resources/spotlight/formerdirectorlorischock-directors-take/thinking-day-trading-know-risks
- FINRA, effective 2026 margin standards and broker transition: https://syndication.finra.org/content/understanding-new-intraday-margin-requirements
- Investor.gov pattern-day-trader transition: https://www.investor.gov/introduction-investing/investing-basics/glossary/pattern-day-trader
- Alpaca feed capabilities and entitlement: https://docs.alpaca.markets/us/docs/about-market-data-api
- Alpaca IEX vs SIP coverage and 15-min recent window: https://docs.alpaca.markets/us/docs/market-data-faq
- Massive feed and personal/commercial rights: https://massive.com/stocks
- GitHub Pages restrictions: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits


## 13. Steelman v1.2a normative requirements extension

Read [SHORT_TERM_STEELMAN.md](SHORT_TERM_STEELMAN.md) before implementing any short-term scoring algorithm.

**The strongest investable-design claim is conditional and falsifiable:** temporary price dislocations and information/flow effects might yield **occasional** cost-adjusted opportunities. A profitable historical pattern from academia does not establish our own after-cost edge. The system must explicitly seek falsification against simple baselines and permit zero candidates.

Additional normative requirements **ST-SM-01 through ST-SM-16** and acceptance tests **SM-T01 through SM-T16** apply. In particular:
- **ST-SM-01 / 06:** Every strategy needs a versioned, preregistered economic mechanism and an experimental search budget.
- **ST-SM-02 / 03 / 05:** Movement magnitude, executable net expectancy, uncertainty-adjusted evaluation and stress/tail losses are separately disclosed.
- **ST-SM-04 / 13:** Missing market microstructure data prevents labeling a result as executable; stale/partial IEX and unentitled SIP must never appear as current full-market opportunities.
- **ST-SM-07 / 08 / 16:** Comparison against no-trade, simple low-frequency strategies and matched controls, with cluster-sensitive uncertainty and preference for simpler methods, is mandatory.
- **ST-SM-09 / 10 / 12:** No forced alerts. Immutable opportunity ledger and automatic suspension when data, economics or performance deteriorates.
- **ST-SM-11 / 14 / 15:** The product must demonstrate research value independent of alpha, identify universe coverage, and maintain strict research/advisory/execution boundaries.

**Release precedence:** design gate D0 passed on paper; D1–D4 remain unverified. Requirements cannot be labeled implemented by their inclusion in this PR. No automated trade placement, leverage or "Buy now" outputs are authorized.

## 14. Financial calculation dependency — short-term trading v1.3

Normative: [quant/01_MARKET_MATH.md](quant/01_MARKET_MATH.md), [quant/04_EXECUTION_COSTS.md](quant/04_EXECUTION_COSTS.md), [quant/05_PORTFOLIO_RISK.md](quant/05_PORTFOLIO_RISK.md), [quant/06_STATISTICAL_VALIDATION.md](quant/06_STATISTICAL_VALIDATION.md), and [quant/07_RED_TEAM_STEELMAN.md](quant/07_RED_TEAM_STEELMAN.md).

- **ST-QF-01:** Discovery identifies possible movement. Research qualification requires evidence-backed net after-cost expectancy, fill policy, uncertainty and tail risk.
- **ST-QF-02:** Volatility, price movement, individual realized PnL, total strategy return and risk-adjusted performance are independent metrics.
- **ST-QF-03:** Missing bid/ask, partial fills, delayed/stale quotes, same-candle ambiguity, stop gaps, poor liquidity and unlicensed data cause abstention, exploratory status or publication rejection.
- **ST-QF-04:** Backtest requires capital-constrained NAV, point-in-time available inputs, realistic execution cost, immutable experiment record and independent holdout.
- **ST-QF-05:** The 40 example golden vectors in tests/specs are *partial, unexecuted* requirements; implement a separate test for every formula and all 50 red-team scenarios before promotion. No guaranteed profitability or automatic trade placement.
