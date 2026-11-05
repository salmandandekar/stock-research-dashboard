"""Generate a private HTML and CSV swing-research report automatically.

Configured daily on your own computer. Uses authorized read-only market DATA
API credentials via environment variables. NEVER publishes prices to Pages,
public Actions artifacts or logs, or executes trades.

Run:
    python private_trade_report.py --source alpaca --feed sip
    python private_trade_report.py --demo   # synthetic demo, no internet
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from analyze import ROOT
from market_data_alpaca import fetch_alpaca_bars, provider_label
from trade_plan import ScenarioError, build_swing_scenario

PRIVATE_DIR = ROOT / "private_reports"
NY = ZoneInfo("America/New_York")
FIELDS = (
    "symbol", "data_asof", "setup_status", "reason",
    "research_window", "conditional_buy_trigger_usd", "hypothetical_stop_usd",
    "take_profit_2r_usd", "take_profit_3r_usd", "skip_gap_open_above_usd",
    "risk_fraction", "atr14_usd", "source", "strategy_validation",
)


def _destination(directory: Path) -> Path:
    target = directory.resolve()
    root = ROOT.resolve()
    private_root = PRIVATE_DIR.resolve()
    # Only private_reports is approved inside the public Git checkout.
    if target.is_relative_to(root) and not target.is_relative_to(private_root):
        raise ValueError("Refusing private market-data output inside public repository")
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        os.chmod(target, 0o700)
    except OSError:
        pass
    return target


def _file_private_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def analyze_private_bars(symbol: str, frame: pd.DataFrame, *,
                         now: datetime, feed: str) -> dict:
    """Calculate levels from completed SIP or partial IEX daily history.

    Market-source metadata is intentionally kept with results. 'RESEARCH_ONLY'
    does NOT mean that a trigger is active or that the proposed trade is sound.
    """
    if frame.empty or not {"High", "Low", "Close", "Volume"}.issubset(frame):
        raise ValueError("Missing OHLCV")
    reference_date = now.astimezone(NY).date()
    asof = pd.Timestamp(frame.index[-1]).date()
    age = (reference_date - asof).days
    if age < 0 or age > 5:
        return {"symbol": symbol, "data_asof": str(asof),
                "setup_status": "STALE", "reason": "Last completed market bar is stale"}
    if feed != "sip":
        return {"symbol": symbol, "data_asof": str(asof),
                "setup_status": "LIMITED_FEED",
                "reason": "IEX-only history is not a complete US market high/volume reference"}
    close = frame["Close"].astype(float)
    recent_ratios = close.tail(22).pct_change().dropna()
    if ((recent_ratios.abs() >= 0.45).any()):
        return {"symbol": symbol, "data_asof": str(asof),
                "setup_status": "CORPORATE_ACTION_REVIEW",
                "reason": "Large recent daily price change needs verified split/event review"}
    try:
        scenario = build_swing_scenario(
            symbol, frame["High"].tolist(), frame["Low"].tolist(),
            frame["Close"].tolist(), frame["Volume"].tolist(), str(asof)
        )
    except ScenarioError as exc:
        return {"symbol": symbol, "data_asof": str(asof),
                "setup_status": "INVALID_DATA", "reason": str(exc)}
    row = {"symbol": symbol, "data_asof": str(asof),
           "setup_status": scenario.status, "reason": scenario.reason}
    if scenario.status == "RESEARCH_ONLY" and scenario.has_levels():
        row.update(
            entry=f"{scenario.conditional_entry:.2f}",
            stop=f"{scenario.hypothetical_stop:.2f}",
            target2=f"{scenario.target_2r:.2f}",
            target3=f"{scenario.target_3r:.2f}",
            gap_limit=f"{scenario.skip_if_open_above:.2f}",
            atr=f"{scenario.atr_14:.2f}",
            risk_pct=f"{scenario.risk_fraction * 100:.2f}",
            risk_fraction=scenario.risk_fraction,
        )
    return row


def _synthetic_bars(symbol: str) -> pd.DataFrame:
    """Reproducible toy input, NEVER a real data source or actual stock prices."""
    dates = pd.bdate_range(end="2026-11-04", periods=250)
    # Alternate excluded and eligible stocks so the demo exercises both cases.
    low_price = symbol in {"FLNA", "URG", "LCID"}
    close = 0.75 if low_price else 10.0
    return pd.DataFrame({
        "High": [close + 0.5] * len(dates),
        "Low": [max(0.01, close - 0.5)] * len(dates),
        "Close": [close] * len(dates),
        "Volume": [350_000 if not low_price else 12_000_000] * len(dates),
    }, index=dates)


def build_reports(*, fetcher, output_dir: Path,
                  now: datetime, feed: str, source: str,
                  demo: bool = False, required_fraction: float = 0.60) -> dict:
    """Create private latest.html + latest.csv only if the freshness gate passes.

    Fetcher accepts symbol and returns a DataFrame. No credentials or quotes
    are ever printed. Both outputs are ignored by Git under private_reports/.
    """
    if now.tzinfo is None:
        raise ValueError("Now must be timezone-aware")
    symbols = json.loads((ROOT / "watchlist.json").read_text(encoding="utf-8"))["tickers"]
    rows = []
    failures = []
    for symbol in symbols:
        try:
            frame = fetcher(symbol)
            row = analyze_private_bars(symbol, frame, now=now, feed=feed)
            row["source"] = source
        except Exception as exc:
            # Show provider problem only by type to avoid leaking secrets/responses.
            row = {"symbol": symbol, "data_asof": "unavailable",
                   "setup_status": "INSUFFICIENT_EVIDENCE",
                   "reason": f"Provider error: {type(exc).__name__}",
                   "source": source}
            failures.append(f"{symbol}: {type(exc).__name__}")
        row["allowed"] = row["setup_status"] == "RESEARCH_ONLY"
        rows.append(row)
    fresh_count = sum(r["setup_status"] not in
                      {"STALE", "INSUFFICIENT_EVIDENCE", "INVALID_DATA"} for r in rows)
    required = math.ceil(len(symbols) * required_fraction)
    if fresh_count < required:
        raise RuntimeError(
            f"Fresh-data gate failed: {fresh_count}/{len(symbols)}; required {required}. "
            "Previous private latest report is unchanged."
        )
    directory = _destination(output_dir)
    stamp = now.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    env = Environment(loader=FileSystemLoader(str(ROOT)),
                      autoescape=select_autoescape(["html"]))
    page = env.get_template("private_report_template.html").render(
        rows=rows, generated_at=stamp,
        provider=("SYNTHETIC DEMO — NOT REAL MARKET PRICES" if demo else source),
        issues=failures,
    )
    import io
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS)
    writer.writeheader()
    for r in rows:
        writer.writerow({
            "symbol": r["symbol"], "data_asof": r["data_asof"],
            "setup_status": r["setup_status"], "reason": r["reason"],
            "research_window": "1-5 trading sessions, recompute after next completed bar",
            "conditional_buy_trigger_usd": r.get("entry", ""),
            "hypothetical_stop_usd": r.get("stop", ""),
            "take_profit_2r_usd": r.get("target2", ""),
            "take_profit_3r_usd": r.get("target3", ""),
            "skip_gap_open_above_usd": r.get("gap_limit", ""),
            "risk_fraction": r.get("risk_fraction", ""),
            "atr14_usd": r.get("atr", ""),
            "source": source,
            "strategy_validation": "UNVALIDATED RESEARCH ONLY; NO ORDERS",
        })
    prefix = "demo_" if demo else ""
    _file_private_atomic(directory / (prefix + "latest.csv"), buffer.getvalue())
    _file_private_atomic(directory / (prefix + "latest.html"), page)
    return {"count": len(rows), "fresh_count": fresh_count,
            "scenarios": sum(r["allowed"] for r in rows),
            "html": directory / (prefix + "latest.html"),
            "csv": directory / (prefix + "latest.csv")}


def main() -> None:
    parser = argparse.ArgumentParser(description="Private automated stock research; never trades")
    parser.add_argument("--source", choices=["alpaca"], default="alpaca")
    parser.add_argument("--feed", choices=["sip", "iex"], default="sip")
    parser.add_argument("--demo", action="store_true",
                        help="Offline synthetic demo; separate files, never actual prices")
    args = parser.parse_args()
    now = (datetime(2026, 11, 5, 22, tzinfo=timezone.utc)
           if args.demo else datetime.now(timezone.utc))
    if args.demo:
        fetcher = _synthetic_bars
        source = "SYNTHETIC DEMO"
        feed = "sip"
    else:
        feed = args.feed
        fetcher = lambda symbol: fetch_alpaca_bars(symbol, now=now, feed=feed)
        source = provider_label(feed)
    result = build_reports(fetcher=fetcher, output_dir=PRIVATE_DIR,
                           now=now, feed=feed, source=source, demo=args.demo)
    print(f"Updated {result['count']} locally analyzed symbols; "
          f"{result['scenarios']} illustrative scenarios; "
          f"{result['fresh_count']} had usable completed source history.")
    print(f"Private report: {result['html']}")
    print(f"Private CSV: {result['csv']}")
    print("No orders placed. Results are not proven profitable. Do not publish files.")


if __name__ == "__main__":
    main()
