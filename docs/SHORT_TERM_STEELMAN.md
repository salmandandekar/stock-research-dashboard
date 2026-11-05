# Steelman Addendum — Short-Term Opportunity Discovery v1.2a
**Date:** 2026-11-04  
**Status:** DESIGN REVIEW COMPLETE / ENGINEERING VALIDATION PENDING  
**Extends:** [SHORT_TERM_OPPORTUNITY_REQUIREMENTS.md](SHORT_TERM_OPPORTUNITY_REQUIREMENTS.md) and the pre-existing long-horizon requirements.  
**Decision:** Pursue a *selective, mechanism-driven, cost-adjusted, multi-horizon discovery engine*, not a high-frequency "daily winning stock" predictor. No automated execution or user-tailored trade recommendation.

## 1. Strongest affirmative case
The investment opportunity is not that every volatile stock is predictable. It is that **some price deviations may arise from time-specific order imbalances, slow or uneven reaction to new information, participant constraints and temporary liquidity needs**. An appropriately designed research engine can recognize predeclared conditions, compare them against their real historical net execution outcomes, and refrain from proposing an opportunity when the evidence fails.

### Empirical reasons to investigate (not performance guarantees)
1. Gao, Han, Li and Zhou (2018), *Market intraday momentum*, Journal of Financial Economics: historical first-half-hour market performance helped predict the last-half-hour return in a sample of ETFs, particularly during high-volume and volatile sessions. This is evidence of a *conditional pattern*, not proof that our individual-stock scanner will profit. Source: https://profiles.wustl.edu/en/publications/market-intraday-momentum/
2. Heston, Korajczyk and Sadka (2010), *Intraday Patterns in the Cross-Section of Stock Returns*: documents intraday continuation and short-term reversal patterns, along with order imbalance and liquidity. The sample and observations are not an implementable profitability guarantee after current costs. Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1107590
3. Ignashkina, Rinne and Suominen (2022), *Short-term reversals, returns to liquidity provision and the costs of immediacy*: short-term reversals can be associated with liquidity supply while liquidity takers pay immediacy costs. This warns against a simplistic contrarian/volatility strategy that crosses spreads indiscriminately. Source: https://doi.org/10.1016/j.jbankfin.2022.106430
4. Almgren (2003), *Optimal execution with nonlinear impact functions and trading-enhanced risk*: execution costs and price impact are functions of trading rate and size, not constants that can be safely ignored. Source: https://doi.org/10.1080/135048602100056

**Steelman product hypothesis:** The system could discover a *small number of unusual, causally motivated research setups*, with evidence of favorable executable net expectancy in the specific regime, sufficient liquidity and tolerable downside; simultaneously it can help users avoid false opportunities by exposing the cases where volatility does not cover the cost of trading.

## 2. Best possible opposing argument: do not build
- Professional market participants compete for short-lived signals using lower latency, richer feeds and better order execution. Retail-grade free feeds have different venue coverage and constraints.
- Apparent profit is frequently bid/ask bounce, adverse selection, stale quotes, corporate-action errors, incomplete order simulation, selection bias, or optimization against a historical sample.
- Day-trading outcomes are weak for most individuals. Barber, Lee, Liu and Odean report that under 1% of day traders in a historical Taiwan sample predictably earned positive abnormal returns net of costs; extrapolation to current US securities is not justified. https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html
- The SEC warns that day trading can lead to severe losses and is not a reliable easy-income strategy. https://www.sec.gov/about/reports-publications/investorpubsdaytipshtm
- A complicated scanner may increase attention, overtrading and false confidence, even if its forecasting usefulness is low.
- A simpler, cheaper outcome may be EOD swing idea generation plus disciplined research, or no trading at all. That is the counterfactual benchmark.

**Steelman response:** Concede the market competition and the possibility that no profitable strategy exists. Limit research to predeclared, lower-frequency mechanisms. Make the **simplest viable nontrading or EOD alternative** the baseline. Stop development or do not enable a strategy if measurable after-cost out-of-sample advantage is absent. Optimize for research quality and abstention before maximizing signal count.

## 3. Strengthening loops (Socratic -> contrary hypothesis -> design correction)

### Loop A — What produces an edge?
**Socratic question:** Why should a 6% daily swing have positive expected net return for us rather than for better-resourced traders?
**Contrary case:** The move is explained by news already incorporated in prices, or by untradeable spreads and slippage.
**Correction:** Require every proposed strategy to register an economic mechanism, observable trigger, direction/holding interval, execution assumption, risk from being wrong, and conditions under which the mechanism should disappear.
**Acceptance:** A mechanism with no falsifiable prediction must remain "exploratory" and cannot yield validated opportunity status.

### Loop B — Does a backtest measure executable opportunity?
**Socratic question:** What happens if the model enters on a 1-minute candle low and exits on its high?
**Contrary case:** Candle hindsight, lack of quote/queue evidence, and adverse fills manufacture profit.
**Correction:** Quote-level or conservatively modeled next-available execution, no same-bar high/low hindsight; include no-fills, partial fills, time delay, spread, slippage, adverse selection, and fixed historical cost stress. Make net expectancy and lower-bound uncertainty separate from a point prediction.
**Acceptance:** A bullish test becomes NO_TRADE when 2x trading costs remove the modeled benefit; unavailable quote data blocks any "executable" certification.

### Loop C — Will the result remain useful across regimes?
**Socratic question:** Does a positive average survive earnings days, rate announcements, recessions, high volatility, and quiet markets?
**Contrary case:** A strategy owes its gains to a tiny number of unusual dates or one sector, while losses cluster.
**Correction:** Predeclare regimes, stratify sectors, issuers and sessions, analyze worst cases, bootstrap by **trading date/event clusters** rather than assuming independent trades, limit concurrent exposures, measure drift and add suspension triggers.
**Acceptance:** Strong overall backtest with unacceptable clustered tail loss or high fragility is not promoted.

### Loop D — Is the product economically useful?
**Socratic question:** How many alerts are worth a user spending time and money on?
**Contrary case:** A high-volume scanner produces noise; even technically correct alerts lead to overtrading and unplanned risks.
**Correction:** Allow 0 outputs, score *attention value* separately from potential price opportunity, show a rank-limited, diversified shortlist, require a human review and an "avoid" rationale for disqualified results. Compare to a no-trade benchmark and a simple EOD strategy.
**Acceptance:** Zero-edge conditions yield no new trading signal; dashboard still reports coverage, invalidation and reasons. No frequency target encourages forced signals.

### Loop E — What is the correct first deployment?
**Socratic question:** Can the free Github infrastructure reliably identify and present real-time US-wide intraday opportunities?
**Contrary case:** No. Scheduled Actions is not a continuous market worker, and free IEX live data is a subset of the market while full SIP recent data requires an entitlement.
**Correction:** Three separate releases: (1) EOD swing discovery; (2) offline intraday historical evaluation; (3) separately budgeted continuously monitored, licensed *paper-only* live signal service. GitHub Pages only displays permitted derived research artifacts.
**Acceptance:** An expired, delayed, partial-venue or disconnected signal is never presented as current full-market actionable data.

## 4. Candidate mechanism register (research hypotheses, not proven strategies)
| ID | Rationale | Observable pre-trade features | Direction + horizon | Falsifier | Primary danger |
|---|---|---|---|---|---|
| HYP-01 | Opening order imbalance / excessive overnight price response may partially revert | Overnight gap, timestamped first-window volume, market/sector-relative change, spread and calendar events | Long-only opening-reversal hypothesis within predefined regular session window | No OOS positive net expectancy after spread/latency; signal disappears with available timestamps | News not digested, continuation against position, untradeable opening spread |
| HYP-02 | Strong early-session market participation can persist late in the day | First-window return, volume, realized volatility, whole-market regime, event calendar | Long-only late-session momentum *conditional on regime* | Signal fails on held-out recent years or at realistic next-quote fill | Historical ETF result does not transfer to individual names |
| HYP-03 | Earnings/guidance revision may cause multi-session adjustment | Public announcement/filing time, surprise versus authorized consensus (if licensed), abnormal volume and gap, liquidity | 1–5 day swing | Return earned only before publication time or disappears after realistic next-day entry | Earnings gaps and stale/unlicensed estimates |
| HYP-04 | Temporary liquidity dislocation might reverse when selling pressure subsides | Pretrade quote/volume imbalance, extreme price deviation from sector baseline, spread, event flags | 5–60-minute reversal for study only | Signal alpha fully explained by bid/ask bounce or impossible fills | Adverse selection and nonstationary liquidity |
| HYP-05 | Sustained momentum/relative strength can rank swing candidates | Prior-day relative strength, market-relative returns, liquidity, sector participation | 1–5 day swing | OOS net expectancy does not exceed simple benchmark | Trend crash, sector clustering, overnight gap |

**No historical claim is made that HYP-01..05 will work for this platform.** They are competing hypotheses to *try to falsify* with independent data. Start with at most two low-frequency hypotheses, and limit the first paid data investment until value is shown.

## 5. Added normative requirements (ST-SM-01 .. ST-SM-16)
| ID | Priority | Requirement / verification |
|---|---|---|
| ST-SM-01 | P0 | Maintain a versioned **Mechanism Registry** for each strategy: explanation, features available at decision time, universe, long-only direction, holding period, counterfactual, regime, falsifiers, change budget. **Test:** reject a mechanism without timestamped features and falsification criteria. |
| ST-SM-02 | P0 | Separate three measurements: potential gross move, modeled executable net expectancy, and **uncertainty-adjusted** rank. Do not use volatility or win rate as a substitute. **Test:** large moves but negative net expectancy return NO_TRADE. |
| ST-SM-03 | P1 | Publish a distribution of outcomes, not merely an average: median, 5th/95th quantiles, stop/gap stress, profit factor, cost sensitivity, cluster-robust uncertainty and sample size. **Test:** a positive average with extreme tail losses cannot be promoted silently. |
| ST-SM-04 | P0 | Require the **source market microstructure coverage** needed for each strategy. When order book/quote information is insufficient, only label results "exploratory", never "executable". **Test:** minute OHLC without quotes cannot certify realistic limit fills. |
| ST-SM-05 | P1 | Calibrate costs and fill assumptions to actual spread, trade size, venue, time of day and liquidity cohort; vary costs by regime and verify 1x/2x stress. **Test:** strategy correctly abstains when stressed net expectancy <= 0. |
| ST-SM-06 | P1 | Preregister at most two candidate mechanisms for initial evaluation, with fixed factor definitions, tests, baseline and optimization budget. **Test:** no unlogged threshold experiments or repeated holdout reuse. |
| ST-SM-07 | P1 | Include matched controls: do nothing/cash, simple EOD strategy, random signals matched on time/sector/liquidity/volatility, and market-adjusted benchmark where economically appropriate. **Test:** "edge" improvement vs best simple alternative can be computed net of identical costs. |
| ST-SM-08 | P1 | Run date/event-cluster bootstrap and per-regime analysis; include correlated losses, exposure clustering and concentration. **Test:** correlated signals aren't incorrectly counted as independent evidence. |
| ST-SM-09 | P0 | Never use a fixed number of alerts as a success target. Include a measurable **abstention rate** and the reasons; no-trade days are reported. **Test:** all candidates can fail without fabricated recommendations. |
| ST-SM-10 | P1 | Maintain a **Research Opportunity Ledger** with original feature snapshot, predicted horizon, output time, expiry, fill assumptions, subsequent observed outcome and failure rationale. Preserve "no trade" decisions. **Test:** point-in-time replay independently reproduces selection. |
| ST-SM-11 | P1 | Measure user benefit independently of alpha: time spent per qualified opportunity, false-alert rate, model abstention usefulness, evidence completeness and cost to operate. **Test:** controlled comparison with a manual/EOD-only workflow. |
| ST-SM-12 | P1 | Set prospective **drift and suspension conditions**: data loss, cost increase, regime shift, recurring failure, degraded realized spread and drawdown thresholds, plus human review. **Test:** triggered suspension prevents new live-style alerts, with visible explanation. |
| ST-SM-13 | P0 | Disable **real-time actionable framing** unless licensed venue coverage, latency, compute uptime and paper evidence are verified. **Test:** IEX-only feed or >=15-min recent-SIP delay never claims comprehensive live price. |
| ST-SM-14 | P1 | Disclose which research universe was scanned and why candidate is ranked. No "market-wide" label unless coverage is defined and observed. **Test:** missing exchanges, partial feed, duplicate symbols or disqualified low-float shares show correct coverage and exclusions. |
| ST-SM-15 | P0 | Make investment advice, position sizing, leverage, shorts, order handling and API broker connections separate scope requiring product/legal/privacy review. **Test:** no order endpoint or private account fields are present in public artifacts. |
| ST-SM-16 | P1 | Use a stage gate that favors simpler strategy over more complex one unless superior after-cost out-of-sample **economic and statistical** evidence is demonstrated. **Test:** zero economically relevant improvement rejects the complex candidate. |

## 6. Test matrix and review cycles
| Test | Design risk | Fixture | Required result |
|---|---|---|---|
| SM-T01 | Trading noise mistaken for edge | 8% volatility and negative expected net outcome | NO_TRADE |
| SM-T02 | Incomplete market data | Full-market breakout relying on free IEX-only bars | Not labeled full-market live |
| SM-T03 | Impossible fill | Signal at 10:15 candle low and exit same candle high | Look-ahead/error or conservative abstention |
| SM-T04 | Cost fragility | Gross expectancy > 0 but 2x spread/slippage consumes it | Not promoted |
| SM-T05 | Rare ruin event | 96% winners but severe drawdown in remaining 4% | Tail and ruin warning; fail gate if above threshold |
| SM-T06 | Parameter fishing | 500 variants tested, winner chosen using final holdout | Holdout invalidated |
| SM-T07 | Correlated signals | 50 technology names signal same sector shock | Clustered exposure and uncertainty; no false independence |
| SM-T08 | Overfitted regime | Strategy profitable only during one 2020-style period | Report and reject unsupported broad performance claim |
| SM-T09 | Latency | Event ended before generated/publication time | EXPIRED; no current opportunity |
| SM-T10 | Coercion to overtrade | No candidate meets edge threshold today | Zero candidates and NO_TRADE |
| SM-T11 | Data provider loses market coverage | Venue loss, halt, disconnected websocket | Suspend or downgrade label immediately |
| SM-T12 | Research falsification | All tested hypothesis mechanisms fail out-of-sample | Publish failure; no claim of profitable edge |
| SM-T13 | False precision | Insufficiently powered sample presented as 82% win probability | Probability withheld and confidence marked insufficient |
| SM-T14 | Post-hoc earnings signal | Entry before publicly timestamped filing/announcement | Reject look-ahead |
| SM-T15 | Synthetic paper fills | Limit order always fills at touch without queue/liquidity | Conservative fill model or omit certification |
| SM-T16 | User confused by research call | Hypothetical idea shown as "buy now" | UI rejects wording and shows research-only status |

### Independent role-based future human review
- Quant researcher: inspect all signal timestamps, competing controls, statistical uncertainty, regime breakdown, costly failures and multiple-test counts.
- Market data engineer: independently reconcile quotes against authorized source, venue coverage and provider entitlement.
- Platform engineer: verify operational latency, expiry, resilience and CI/PR supply chain.
- Security/legal reviewer: confirm source rights and no public portfolio, advice or order integration.
- Research user: evaluate favorable and unfavorable exemplars and whether each card can justify a **No Trade** conclusion.

The role-based review is **required work**, not work already completed. All tests above are specifications, not executed code tests.

## 7. Decision gate / release stages
### D0: Steelman design gate — PASS (documentation)
- A plausible time-specific economic mechanism is stated and independently sourced.
- Its strongest counterargument is acknowledged.
- Every pretrade input has a time and coverage contract.
- Net expectancy, realistic fills, tail risk, no-trade and falsification are mandatory.
- Simple alternatives, not just chance, are explicit baselines.
**This D0 verdict is limited to the *design*.**

### D1: Data and execution proof — NOT MET
- Source licensing; historical bid/ask/available-at coverage; realistic fills; test pass reports.
- No hidden future data, overfit universe or uncompensated costs.

### D2: Out-of-sample proof — NOT MET
- Pre-registered variants; untouched holdout; adequate independent event count; sensitivity across cost, regime, sector, calendar time; uncertainty estimates.
- If a proposed 95% lower-bound expectation test is used, justify the dependence and false-discovery corrections; statistical significance alone is insufficient without economic significance.
- No promise of specific positive returns; negative results and model churn are visible.

### D3: Prospective paper evidence — NOT MET
- Timestamped signals *before outcomes*, included NO_TRADE days, realistic fills and errors, and observation across market conditions. The proposed 60-session/200-observation minimum remains a planning target only; do not generate additional signals just to meet it.
- If sample is inadequate, keep monitoring or do not promote.

### D4: Operational and human readiness — NOT MET
- Data entitlements, security/rights and human quantitative review.
- If advisory/trading ever considered, separate investor-suitability, legal, operational and account controls. **No automatic execution in v1.2.**

## 8. Development priority recommended by the steelman
1. Preserve the merged v1.1 fundamentals and source provenance foundation. Reuse security identity, source contracts, strategy versioning, audit ledger and testing harness.
2. Build **batch swing** MVP with *one* high-quality hypothesis, explicit counterfactuals, risk/cost accounting, and No Trade. Historical next-session execution only.
3. Add realistic point-in-time backtest with *at least* simple momentum/mean-reversion controls, executed or conservatively unfilled quote model, date clustering, and transparent negative results.
4. Only then trial minute-level intraday hypotheses using licensed historical data. Keep results exploratory if quote depth cannot support realistic fill assumptions.
5. Decide to stop, license a live feed and run paper-only signal monitor, or remain with EOD swing based on demonstrated incremental value.

## 9. Key product positioning
**Bad:** "An AI finds stocks that can make profits every day."  
**Good:** "A transparent, evidence-based scanner identifies potentially attractive short-term research setups, estimates execution costs and downside, and explains when *not* to trade."

**Final design decision:** Approve the requirements upgrade at the design level, but do not equate academic intraday anomalies with our own forecast accuracy, net profit, advisory compliance, or deployment readiness.
