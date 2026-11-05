"""Scheduled technical stock research. Not investment advice or a trading bot."""
from __future__ import annotations

import json
import logging
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
from quant_core import daily_volatility, price_return, sma
from trade_plan import build_swing_scenario, ScenarioError

ROOT = Path(__file__).resolve().parent
LOG = logging.getLogger("stock-research")
SYMBOL = re.compile(r"^[A-Z0-9.^=\-]{1,18}$")


def analyze_stock(symbol: str, closes: pd.Series, today=None) -> dict:
    series = pd.to_numeric(closes, errors="coerce").astype(float)
    if series.isna().any() or series.index.has_duplicates:
        raise ValueError(f"{symbol}: missing, nonnumeric or duplicate daily prices")
    series = series.sort_index()
    if len(series) < 210:
        raise ValueError(f"{symbol}: need at least 210 trading closes")
    if not np.isfinite(series.to_numpy()).all() or (series <= 0).any():
        raise ValueError(f"{symbol}: prices must be positive and finite")
    last = float(series.iloc[-1])
    sma50 = sma(series.tail(50).tolist(), 50)
    sma200 = sma(series.tail(200).tolist(), 200)
    mom3 = price_return(float(series.iloc[-64]), last)
    mom6 = price_return(float(series.iloc[-127]), last)
    volatility = daily_volatility(series.pct_change().dropna().tail(63).tolist())
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


def fetch_history(symbol: str) -> pd.DataFrame:
    import yfinance as yf
    last_error = None
    for attempt in range(3):
        try:
            frame = yf.Ticker(symbol).history(period="18mo", auto_adjust=False, actions=True)
            if frame.empty or not {"Close", "Adj Close", "High", "Low", "Volume"}.issubset(frame.columns):
                raise ValueError("Empty or invalid market history")
            # A daily OHLC bar may be partially formed before a reliable close.
            # Keep this run end-of-day only. 17:00 ET is a conservative cutoff,
            # not an exchange holiday calendar or real-time feed guarantee.
            ny_now = datetime.now(ZoneInfo("America/New_York"))
            if ny_now.hour < 17:
                dates = pd.DatetimeIndex(frame.index).date
                frame = frame.loc[[d < ny_now.date() for d in dates]]
            if frame.empty:
                raise ValueError("No completed daily price bars available")
            return frame
        except Exception as exc:
            last_error = exc
            LOG.warning("%s fetch attempt %d failed: %s", symbol, attempt + 1, exc)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"{symbol}: no market data") from last_error


def fetch_closes(symbol: str) -> pd.Series:
    """Adjusted series for the legacy scoring model; no executable quote."""
    return fetch_history(symbol)["Adj Close"]


def analyze_history(symbol: str, frame: pd.DataFrame,
                    *, today=None) -> dict:
    """Evaluate adjusted technical screen and raw-price research scenario.

    Do not use adjusted prices as hypothetical executable fills. Numeric
    scenarios are not copied into the public HTML until data rights are cleared.
    """
    if frame.empty or not {"High", "Low", "Close", "Adj Close", "Volume"}.issubset(frame):
        raise ValueError("Missing OHLCV or adjusted close")
    asof = str(pd.Timestamp(frame.index[-1]).date())
    try:
        result = analyze_stock(symbol, frame["Adj Close"], today=today)
    except ValueError as exc:
        result = {
            "symbol": symbol, "score": None, "signal": "Insufficient evidence",
            "risk": "Not assessed", "asof": asof, "stale": True,
            "strengths": [], "concerns": [str(exc)], "rules": [],
        }
    recent_splits = ("Stock Splits" in frame and
                     bool((frame["Stock Splits"].tail(21).fillna(0) != 0).any()))
    try:
        scenario = build_swing_scenario(
            symbol, frame["High"].tolist(), frame["Low"].tolist(),
            frame["Close"].tolist(), frame["Volume"].tolist(), asof,
            split_in_recent_window=recent_splits)
        result["scenario"] = scenario
        result["plan_status"] = (
            "STALE" if result["stale"] else scenario.status
        )
        result["plan_reason"] = (
            "Stale or insufficient completed price history" if result["stale"]
            else scenario.reason
        )
    except (ScenarioError, ValueError) as exc:
        result["plan_status"] = "INSUFFICIENT_EVIDENCE"
        result["plan_reason"] = str(exc)
        result["scenario"] = None
    return result


def render(rows: list[dict], errors: list[str], generated_at: str) -> str:
    env = Environment(loader=FileSystemLoader(str(ROOT)),
                      autoescape=select_autoescape(["html"]))
    return env.get_template("site_template.html").render(
        rows=sorted(rows, key=lambda row: (row["stale"], -(row["score"] if row["score"] is not None else -1), row["symbol"])),
        errors=errors, generated_at=generated_at,
        candidate_count=sum(r["score"] is not None and r["score"] >= 70 and not r["stale"] for r in rows),
        monitor_count=sum(r["score"] is not None and 40 <= r["score"] < 70 and not r["stale"] for r in rows),
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
            row = analyze_history(symbol, fetch_history(symbol))
            rows.append(row)
            LOG.info("%s: score=%s, plan_status=%s, data-as-of=%s, stale=%s",
                     symbol, row["score"], row["plan_status"], row["asof"], row["stale"])
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
