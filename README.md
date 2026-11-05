# Stock Research Dashboard

Free, scheduled, research-only technical stock screening: Python + GitHub Actions + GitHub Pages.

## What it does

- Monitors 13 tickers: AAPL, MSFT, NVDA, GOOGL, AMZN, LUNR, MNSO, GRRR, URG, LTRX, LCID, NOK, FLNA.
- Fetches approximately 18 months of adjusted daily closes using yfinance for personal prototyping.
- Scores 5 deterministic technical indicators for an explainable 0-100 research rank.
- Suppresses stale scores, records unavailable symbols, and aborts deployment if fewer than 60% are fresh.
- Publishes only ranks, technical explanations and dates to a public static HTML site; no raw quotes or price histories.

## Run locally

Use Python 3.12:

    python -m pip install -r requirements.txt
    python -m pytest -q
    python analyze.py

Open site/index.html. Live data fetching requires internet connectivity.

## Activate GitHub Pages

1. Open repository Settings > Pages > Build and deployment.
2. Select GitHub Actions as the source.
3. Open Actions > Daily stock research and dashboard > Run workflow.
4. After a successful deploy, open https://salmandandekar.github.io/stock-research-dashboard/

The publish workflow is also scheduled for 4:17 PM America/Chicago on weekdays. GitHub schedules can be delayed or skipped. US market holidays may yield the previous trading session.

## Research scoring

| Rule | Points |
| --- | ---: |
| Close above 200-day moving average | 30 |
| 50-day average above 200-day average | 20 |
| Positive 63-trading-day momentum | 20 |
| Positive 126-trading-day momentum | 20 |
| 63-day annualized volatility below 40% | 10 |

70+ = research candidate; 40-69 = monitor; below 40 = weak technical setup.

**These are unvalidated technical heuristics, NOT personalized financial advice or a validated buy/sell strategy.** They do not model valuation, balance sheets, taxes, intrinsic value, or expected returns. No trades are placed.

## Data and public-site safeguards

yfinance/Yahoo Finance data is subject to provider terms and may be limited to personal use. This MVP deliberately avoids republishing quotes or price history; verify derived-data rights before making research outputs publicly accessible. If necessary, use a licensed provider or keep deployment private under a different hosting plan. Public Pages and public repositories must not contain personal portfolio data, API keys, credentials or account identifiers.

GitHub scheduled workflows can be delayed, skipped, or automatically disabled after long repository inactivity.

## Codex

Open https://chatgpt.com/codex, choose this repository as the Codex environment, and give Codex the contents of CODEX_TASK.md. AGENTS.md contains persistent engineering guidance. Codex access may require separate authorization from the GitHub connection in ChatGPT.

## References

- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://ranaroussi.github.io/yfinance/
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces


## Conditional buy/sell research planning — 13 tickers

The public report has a Swing Scenario section. It displays each stock's eligibility or exclusion status, and an entirely browser-local calculator for the user's own broker-provided last close, last 20 completed session high, Wilder ATR(14), and dollar turnover. These inputs are not transmitted or stored.

To generate a private CSV of automatically computed exact USD price levels on your own computer, run:

    python -m pip install -r requirements.txt
    python private_trade_report.py

The program uses the same unofficial personal-use yfinance adapter and writes private_reports/swing_research_*.csv. The directory is ignored by Git and not deployed. Keep this CSV private and verify provider rights.

Research-only formulas: conditional breakout entry is the smallest cent strictly above the last 20 completed-session highs; stop scenario = entry - 1.5 x ATR14; target 1 = entry + 2R; target 2 = entry + 3R, where R = entry - stop. Skip the entry if the opening price exceeds entry + 0.5 x ATR14. Recompute after each completed bar. Research horizon is 1–5 subsequent exchange trading sessions.

Unvalidated example gates: close >= USD 5; 20-session dollar volume proxy >= USD 2 million per day; entry-to-stop risk <=15%; valid 21+ raw, split-consistent OHLCV bars; no split in recent 21 bars.

Urgent caveat: These scenarios are NOT live buy/sell recommendations. They are not based on proven positive expected after-cost returns. Stop fills, 2R/3R targets, next-session price, spreads, trading halts, slippage and earnings gaps cannot be guaranteed.

FLNA (Filana Therapeutics) is the successor ticker to SAVA and has Nasdaq bid-price compliance risk. URG and FLNA remain on the watchlist while below the USD 5 research eligibility floor.

Yahoo's official market-data policy prohibits redistribution of its data. Until we have approved public display rights, exact provider-derived dollar levels remain private rather than posted on public GitHub Pages. For details see docs/SWING_SCENARIO_IMPLEMENTATION.md.
