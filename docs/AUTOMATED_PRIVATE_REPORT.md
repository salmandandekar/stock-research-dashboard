# Automated Private Swing Research — No Manual Dollar-Level Inputs
**Status:** Implemented local pipeline / initial tests. **Not:** broker trading, live intraday scanning, a validated profitable strategy, public price redistribution, or a running task on any user's device.

## What changes
Previously the public browser calculator required typing four market values. Now the private, scheduled pipeline **automatically fetches authorized completed daily bars** and recomputes entry trigger, hypothetical stop, 2R/3R targets and opening-gap-skip threshold for **all 13 stocks**.

Output on the computer running the task:
- private_reports/latest.html — responsive private research report with exact dollar levels and explicit exclusions.
- private_reports/latest.csv — rows for all 13 stocks, including excluded/failed symbols.
- No quotes or price levels in GitHub Pages, GitHub CI output, Git repository or Actions artifacts.

### Calculation per stock
1. Request at least 21 daily bars using Alpaca's officially documented historical stock bars endpoint. Request **split-adjusted** and **SIP** for consolidated historical stock data.
2. Accept bars only from completed sessions. Current-session bar is excluded until **5 p.m. New York time**. Default scheduled run is **4:45 p.m. Central = 5:45 p.m. Eastern**.
3. Enforce data age <=5 calendar days (initial conservative guard, with market holiday calendar still pending); reject source failures, repeated pages and invalid OHLC.
4. Calculate existing \`trade_plan.py\` Wilder ATR(14), the 20-completed-session high and hypothetical breakout level:
   - Conditional entry = first cent above last 20-session high.
   - Stop scenario = entry minus 1.5 ATR.
   - Targets = entry plus 2R and 3R, where R = entry-stop.
   - Gap skip = entry plus 0.5 ATR.
5. Exclude low-priced (< USD 5), low-dollar-volume (< USD 2 million/session proxy), excessively wide modeled stop (>15%), stale, malformed or large potentially split/event-affected price moves.
6. **Never** claim an executable fill, positive expectancy, guaranteed stop, active live breakout or next-session return. Show "RESEARCH ONLY" or precise exclusion.

These are unoptimized heuristic thresholds. Spreads, gap risks, earnings and bid/ask costs are NOT included in their target arithmetic; do not convert a calculation into an executable trade without separate validation.

## Required one-time data access
Use an Alpaca account with **paper/data API credentials**, not live brokerage keys. The official historical-bar endpoint is:

https://docs.alpaca.markets/us/reference/stockbars

Alpaca market-data details and IEX/SIP entitlement/coverage are described at:
https://docs.alpaca.markets/us/docs/market-data-faq

- Source must be personally authorized. Terms, historical SIP entitlement and exchange reporting/redistribution rights must be accepted and verified by the account owner.
- Historical SIP data may be accessible on basic accounts when outside the recent ~15-minute restriction. This implementation requests bars at least 25 minutes old and runs after market close. If authorization fails, the job **does not** downgrade to an IEX full-market proxy.
- The optional IEX feed is deliberately gated to "LIMITED_FEED": single-venue highs, lows and volume must not be presented as consolidated market entry levels.
- No Alpaca **trading** API endpoints are used. API keys can still be sensitive and must not be committed, shared, logged, or put in Pages HTML.

## First test — no account or credentials needed
On a computer with Python 3.12:

    git pull
    python -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python private_trade_report.py --demo

On Windows use \`.\.venv\Scripts\python.exe\` instead of \`.venv/bin/python\`.

Open \`private_reports/demo_latest.html\`. This uses **synthetic test data**, not real prices. Do NOT treat it as an investment report. Real reports have the filename \`latest.html\`.

## Windows — daily automatic run
1. Install Python 3.12 and dependencies in \`.venv\` under the repository.
2. Open PowerShell in the repository. Run:
   
   \`.\scripts\setup_windows_auto_report.ps1\`
   
3. Enter the **Alpaca data/paper API key ID** as the username and the **API secret** as the password in the Windows credential prompt. The script encrypts them with Windows DPAPI into the current user's profile outside Git. They are decrypted only in the local scheduled runner process.
4. Windows Task Scheduler executes the report **Monday–Friday at 4:45 p.m. computer local time**, not necessarily Central unless Windows is set to Central. It usually requires the user's computer to be running and the task account to be available.
5. Verify manually without entering any price data:
   
   \`Start-ScheduledTask -TaskName "StockResearchPrivateDaily"\`
   
   Open \`private_reports\latest.html\` afterward.

For a different local time, run setup with \`-AtLocalTime "16:45"\` or another desired time. Do not put credentials in script arguments, source control or public issues.

## RHEL / Linux — daily automatic run
1. Install venv and dependencies:
   
   \`python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt\`
2. Create **outside Git** \`~/.config/stock-research/alpaca.env\` with two named entries:
   
   \`ALPACA_API_KEY_ID=<your authorized key ID>\`
   
   \`ALPACA_API_SECRET_KEY=<your authorized API secret>\`
   
   Use a secure editor; do not paste secret values into shell history or chat. Set \`chmod 600 ~/.config/stock-research/alpaca.env\` and restrict parent directory permissions.
3. Run \`bash scripts/install_linux_timer.sh\`.
4. Verify \`systemctl --user list-timers stock-research-private.timer\`, and test with \`systemctl --user start stock-research-private.service\`.
5. Open \`private_reports/latest.html\`.

The systemd user timer uses \`Mon..Fri *-*-* 16:45:00 America/Chicago\`. A user session may need to remain available. If the service must run without login, configure systemd user lingering separately and review your machine's security policy.

## Manual immediate run after credentials configured
    python private_trade_report.py --source alpaca --feed sip

This command downloads 13 histories, generates both output files, and does not require typing prices. For Windows, use the installed scheduled wrapper so credentials are loaded from DPAPI.

## Operational failure behavior
- No credentials -> error, no report overwritten.
- Network/provider problems affecting most symbols -> error, existing last report retained.
- Missing/invalid/stale individual symbol -> its row is marked unavailable; no dollar levels fabricated.
- Holiday -> weekday task may run, but use last completed bars; report dates remain visible.
- False breakouts and target prices -> not claimed as profitable; the historical strategy backtest and intraday execution model are still outstanding.
- File privacy -> any attempted output to the repo's public \`site/\` directory is rejected.

## Red-team checkpoints
- API credentials never appear in URLs, Git branches, GitHub Actions or public HTML.
- Every provider request identifies source feed and split-adjustment.
- Pagination handles repeated tokens and partial data.
- Current incomplete bar is excluded.
- IEX-only results cannot masquerade as full SIP levels.
- Stale source and insufficient data abstain.
- Excessive modeled risk, corporate-action anomalies, liquidity and low price abstain.
- Synthesized example prices are labeled demo and saved separately from actual results.
- The latest report never includes trading order functions.
- Human action remains necessary to decide whether any trade is appropriate.
