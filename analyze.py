"""Scheduled technical stock research. Not investment advice or a trading bot."""
from __future__ import annotations

import json
import logging
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
LOG = logging.getLogger("stock-research")
SYMBOL = re.compile(r"^[A-Z0-9.^=\-]{1,18}$")


def analyze_stock(symbol: str, closes: pd.Series, today=None) -> dict:
    series = pd.to_numeric(closes, errors="coerce").dropna().astype(float)
    series = series[~series.index.duplicated(keep="last")].sort_index()
    if len(series) < 210:
        raise ValueError(f"{symbol}: need at least 210 trading closes")
    if not np.isfinite(series.to_numpy()).all() or (series <= 0).any():
        raise ValueError(f"{symbol}: prices must be positive and finite")
    last = float(series.iloc[-1])
    sma50 = float(series.tail(50).mean())
    sma200 = float(series.tail(200).mean())
    mom3 = last / float(series.iloc[-64]) - 1
    mom6 = last / float(series.iloc[-127]) - 1
    volatility = float(series.pct_change().dropna().tail(63).std() * np.sqrt(252))
    if not math.isfinite(volatility):
        raise ValueError(f"{symbol}: volatility invalid")
    checks = [
        ("Above 200-day moving average", last > sma200, 30),
        ("50-day average above 200-day average", sma50 > sma200, 20),
        ("Positive 3-month momentum", mom3 > 0, 20),
        ("Positive 6-month momentum", mom6 > 0, 20),
        ("63-day annualized volatility under 40%", volatility < 0.40, 10),
    ]
    score = sum(points for _, passed, points in checks if passed)
    date = pd.Timestamp(series.index[-1]).date()
    current_date = today or datetime.now(timezone.utc).date()
    stale = (current_date - date).days > 5 or date > current_date
    return {
        "symbol": symbol, "score": score,
        "signal": ("Research candidate" if score >= 70 else
                   "Monitor" if score >= 40 else "Weak setup"),
        "risk": ("High volatility" if volatility >= 0.50 else
                 "Moderate volatility" if volatility >= 0.30 else "Lower volatility"),
        "asof": str(date), "stale": stale,
        "strengths": [name for name, passed, _ in checks if passed],
        "concerns": [name for name, passed, _ in checks if not passed],
        "rules": [{"name": name, "passed": bool(passed), "points": points}
                  for name, passed, points in checks],
    }


def fetch_closes(symbol: str) -> pd.Series:
    import yfinance as yf
    last_error = None
    for attempt in range(3):
        try:
            frame = yf.Ticker(symbol).history(period="18mo", auto_adjust=True)
            if frame.empty or "Close" not in frame:
                raise ValueError("Empty or invalid market history")
            return frame["Close"]
        except Exception as exc:
            last_error = exc
            LOG.warning("%s fetch attempt %d failed: %s", symbol, attempt + 1, exc)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"{symbol}: no market data") from last_error


def render(rows: list[dict], errors: list[str], generated_at: str) -> str:
    env = Environment(loader=FileSystemLoader(str(ROOT)),
                      autoescape=select_autoescape(["html"]))
    return env.get_template("site_template.html").render(
        rows=sorted(rows, key=lambda row: (row["stale"], -row["score"], row["symbol"])),
        errors=errors, generated_at=generated_at,
        candidate_count=sum(r["score"] >= 70 and not r["stale"] for r in rows),
        monitor_count=sum(40 <= r["score"] < 70 and not r["stale"] for r in rows),
        stale_count=sum(r["stale"] for r in rows))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = json.loads((ROOT / "watchlist.json").read_text(encoding="utf-8"))
    symbols = config["tickers"]
    if not isinstance(symbols, list) or not 1 <= len(symbols) <= 40:
        raise ValueError("Watchlist must contain 1-40 symbols")
    symbols = list(dict.fromkeys(str(s).upper().strip() for s in symbols))
    if any(not SYMBOL.fullmatch(s) for s in symbols):
        raise ValueError("Watchlist contains invalid stock symbols")
    rows, errors = [], []
    for symbol in symbols:
        try:
            row = analyze_stock(symbol, fetch_closes(symbol))
            rows.append(row)
            LOG.info("%s: score=%s, data-as-of=%s, stale=%s",
                     symbol, row["score"], row["asof"], row["stale"])
        except Exception as exc:
            LOG.exception("Failed analyzing %s", symbol)
            errors.append(f"{symbol}: unavailable ({type(exc).__name__})")
    fresh = sum(not row["stale"] for row in rows)
    required = math.ceil(len(symbols) * .6)
    if fresh < required:
        raise RuntimeError(f"Only {fresh}/{len(symbols)} fresh analyses; need {required}.")
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (site / "index.html").write_text(render(rows, errors, stamp), encoding="utf-8")
    (site / ".nojekyll").write_text("", encoding="utf-8")
    LOG.info("Built site/index.html with %d research results", len(rows))


if __name__ == "__main__":
    main()
