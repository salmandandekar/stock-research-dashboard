# Competitor Benchmark and Research Differentiation
**Reviewed:** 2026-11-04. **Evidence:** primary product documentation; features change. Pricing, licensing and claimed model performance need independent verification. We did not subscribe to the products or evaluate their proprietary predictive accuracy.

| Product | URL and product evidence | Strong capability | Adopt as requirement | Do not assume |
|---|---|---|---|---|
| Seeking Alpha | https://help.seekingalpha.com/premium/quant-ratings-and-factor-grades-faq | >100 metrics and five sector-relative factor grades, quant history | FR-F05, F06; factor drilldown & score changes | Their scoring algorithm, weights or paid data are reusable |
| Morningstar | https://www.morningstar.com/help-center/morningstars-approach-to-investing/morningstars-stock-ratings | Fair value, uncertainty, competitive moat | FR-F02; valuation and uncertainty independent from quality | Fair-value estimates are facts or available for free redistribution |
| Danelfin | https://help.danelfin.com/en/articles/what-is-the-ai-score-how-it-rates-stocks-and-etfs | Predictive AI 1–10 for 3-month benchmark-relative horizon | FR-B04–B07; stated horizon and probabilistic calibration only after validation | Vendor-reported alpha implies ours will succeed |
| TipRanks | https://enterprise.tipranks.com/smart-score/ | Analyst sentiment, insider/hedge fund, news and technical signals | Optional independent evidence channel | Consensus signals prove causal value; API free |
| Simply Wall St | https://support.simplywall.st/hc/en-us/articles/360001740916-How-does-the-Snowflake-work | Five dimensions and intuitive visualization | FR-W01–W03; card with balanced evidence | Copy proprietary chart or rating design |
| Stock Rover | https://f3.stockrover.com/help/screeners-help/screener-overview/ | Weighted screening and historical screens | FR-U04 and parameterized strategy versions | Its historical feeds/metrics are licensed for redistribution |
| TIKR | https://www.tikr.com/stock-screener | International financial statements, ratios, valuation & forecasts | Later stage fundamental/peer comparisons | Broad global coverage can be reproduced free |
| TradingView | https://www.tradingview.com/support/solutions/43000718866-tradingview-stock-screener-trade-smarter-not-harder/ | Technical, market, financial and valuation filters | Chart and filtering UX | Widgets/public display have unrestricted commercial rights |
| Koyfin | https://www.koyfin.com/features/ | Customized fundamental dashboards and macro | Macro context in later stage | Market dashboards improve predictive alpha by default |
| Finviz | https://finviz.com/help/screener | Fast technical+fundamental filtering and signal lists | Fast shortlist flow, filter presets | Screener indicates causal investment value |
| StockAnalysis.com | https://stockanalysis.com/tools/ | Financial statements, DCF calculator, peer comparison and screeners | Transparent formulas and competing valuation assumptions | Its financial data is an unrestricted API |

## Gap assessment
Current prototype has 5 technical checks and a public static report but lacks:
1. Fundamental business-quality checks (cash flows, leverage, profitability).
2. Investment-value estimates and sensitivity bands.
3. Explicit peer/sector normalization.
4. Historical universe and historical-data snapshots.
5. Independent risk/valuation gates, contradictions and a no-candidate state.
6. Sound benchmark comparison and prospective validation.
7. A published, written source-usage/redistribution decision.
8. Distinction between personal research, broad impersonal research, tailored advice and commercial advisory services.

## Differentiation hypothesis
The product should **not** compete on the quantity of signals, opaque AI confidence, or output count. Compete on **traceable evidence, counterarguments, point-in-time validation, uncertainty and sensible abstention**.

This is a product hypothesis, not an established market advantage. Validate with user research, an evaluation rubric and demonstrable historical auditability.

## Comparative acceptance scenarios
- Seeking Alpha-like: factor decomposition and sector-relative comparability are visible.
- Morningstar-like: valuation uncertainty changes the visible thesis; expensive strong-company case is not automatically top ranked.
- Danelfin-like: model horizon and benchmark are explicit; no claim to probability without calibration.
- Simply Wall St-like: a novice can understand 5 main drivers within 2 minutes.
- Stock Rover-like: a strategy can be saved/versioned and rerun without silent parameter drift.
- Finviz-like: initial user can filter the universe quickly and see why every candidate was included or excluded.
- Original differentiator: user can replay the exact decision as of 2024-03-01 and recover the original available evidence and the opposite case, not today's revised filings.

## Decision on vendor integrations
External websites are references. Do **not** scrape their ratings or reuse proprietary algorithms.
Optional later adapters may integrate licensed APIs, including an MCP-based read-only comparison. Danelfin documents an MCP endpoint at https://mcp.danelfin.com/docs/en; access to site features does not imply permission to redistribute API outputs.
