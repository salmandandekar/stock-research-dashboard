# Stock Research Dashboard

Free, scheduled, research-only technical stock screening: Python + GitHub Actions + GitHub Pages.

## What it does

- Monitors the tickers in watchlist.json (initially AAPL, MSFT, NVDA, GOOGL, AMZN).
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
