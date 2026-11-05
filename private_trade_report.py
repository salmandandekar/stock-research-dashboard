"""Generate a LOCAL-ONLY personal swing scenario report from current provider history.

Usage:
    python private_trade_report.py

This program downloads unofficial personal-use research data via the
existing fetch_history adapter. It NEVER uploads the price levels to Pages,
a public repository, Actions artifacts, or job logs. The output stays on
the computer where the user runs the command. Validate data/provider rights.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from analyze import ROOT, analyze_history, fetch_history

PRIVATE_DIR = ROOT / "private_reports"


def main() -> None:
    data = json.loads((ROOT / "watchlist.json").read_text(encoding="utf-8"))
    PRIVATE_DIR.mkdir(exist_ok=True)
    out = PRIVATE_DIR / ("swing_research_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".csv")
    fields = [
        "symbol", "data_asof", "technical_score", "setup_status", "reason",
        "research_window", "conditional_buy_trigger_usd", "hypothetical_stop_usd",
        "take_profit_2r_usd", "take_profit_3r_usd", "skip_gap_open_above_usd",
        "risk_fraction", "atr14_usd", "source", "strategy_validation"
    ]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for symbol in data["tickers"]:
            try:
                row = analyze_history(symbol, fetch_history(symbol))
                scenario = row.get("scenario")
                status = row["plan_status"]
                usable = status == "RESEARCH_ONLY" and scenario is not None
                writer.writerow({
                    "symbol": symbol,
                    "data_asof": row["asof"],
                    "technical_score": row["score"],
                    "setup_status": status,
                    "reason": row["plan_reason"],
                    "research_window": "1-5 trading sessions, recalculate daily",
                    "conditional_buy_trigger_usd": scenario.conditional_entry if usable else "",
                    "hypothetical_stop_usd": scenario.hypothetical_stop if usable else "",
                    "take_profit_2r_usd": scenario.target_2r if usable else "",
                    "take_profit_3r_usd": scenario.target_3r if usable else "",
                    "skip_gap_open_above_usd": scenario.skip_if_open_above if usable else "",
                    "risk_fraction": scenario.risk_fraction if usable else "",
                    "atr14_usd": scenario.atr_14 if usable else "",
                    "source": "Unofficial Yahoo Finance/yfinance personal-use prototype",
                    "strategy_validation": "UNVALIDATED - NOT AN ORDER INSTRUCTION",
                })
            except Exception as exc:
                writer.writerow({
                    "symbol": symbol, "setup_status": "INSUFFICIENT_EVIDENCE",
                    "reason": type(exc).__name__,
                    "source": "Personal-use research - provider access failed",
                    "strategy_validation": "UNVALIDATED"
                })
    print("Local-only report saved:", out)
    print("The levels are hypothetical, not live price quotes, not validated trading predictions.")
    print("Do not upload this file publicly or treat stop prices as guaranteed executions.")


if __name__ == "__main__":
    main()
