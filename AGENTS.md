# Instructions for Codex

Build a transparent, low-cost scheduled stock *research* dashboard, not a trading bot.

- Python 3.12; keep the data-fetching adapter distinct from deterministic stock analysis.
- Run python -m pytest -q before every proposed change.
- Distinguish source timestamps, generated time, and potentially stale market data.
- Never invent market data, test evidence, fundamentals, performance, or citations.
- Never place API keys, personal portfolios, credentials or private financial details in public code or deployed artifacts.
- Do not publish raw quotes or price histories. Confirm source rights before publishing any derived market data.
- Signal thresholds are unvalidated heuristics, not forecasts or buy recommendations.
- Add tests and documentation to every new feature; preserve GitHub Pages deployment.
- Make changes through pull requests where feasible.

Roadmap: SEC fundamentals with fair-access requirements, historical walk-forward backtesting, survivorship-bias safeguards, optional evidence-grounded LLM summaries, material signal-change alerts.
