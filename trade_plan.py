"""Research-only daily swing scenario math (QF-M09, QF-T07, ST-11, ST-14).

No order routing, personalized advice, executable fill certification, or alpha forecast.
Trading levels are hypothetical triggers derived from completed RAW OHLC sessions.
They must not be published from an unlicensed market-data source.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from math import isfinite
from typing import Sequence


class ScenarioError(ValueError):
    """Input is invalid or insufficient. Do not create trading levels."""


@dataclass(frozen=True)
class SwingScenario:
    symbol: str
    status: str
    reason: str
    asof: str
    reference_close: float | None = None
    high_20: float | None = None
    atr_14: float | None = None
    avg_dollar_volume_20: float | None = None
    conditional_entry: float | None = None
    hypothetical_stop: float | None = None
    target_2r: float | None = None
    target_3r: float | None = None
    skip_if_open_above: float | None = None
    risk_fraction: float | None = None
    horizon_sessions: int = 5

    def has_levels(self) -> bool:
        return self.conditional_entry is not None


def _finite(values: Sequence[float], field: str) -> list[float]:
    out = []
    for value in values:
        try:
            n = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ScenarioError(field + ": missing numeric value") from exc
        if not isfinite(n):
            raise ScenarioError(field + ": NaN or infinite value")
        out.append(n)
    return out


def _round_tick(value: float, tick: Decimal, direction: str) -> float:
    amount = Decimal(str(value))
    if tick <= 0:
        raise ScenarioError("invalid tick size")
    mode = ROUND_CEILING if direction == "up" else ROUND_FLOOR
    return float((amount / tick).to_integral_value(rounding=mode) * tick)


def true_range(high: float, low: float, previous_close: float) -> float:
    """QF-M09: true range from completed, split-consistent OHLC data."""
    h, l, prev = _finite([high, low, previous_close], "true range")
    if min(h, l, prev) <= 0 or h < l:
        raise ScenarioError("invalid OHLC for true range")
    return max(h - l, abs(h - prev), abs(l - prev))


def atr_wilder(highs: Sequence[float], lows: Sequence[float],
               closes: Sequence[float], periods: int = 14) -> float:
    """QF-M09: seed first 14 TRs, Wilder smoothing alpha=1/14."""
    if periods < 2:
        raise ScenarioError("ATR period must be at least two")
    h, l, c = (_finite(values, name) for name, values in
               [("highs", highs), ("lows", lows), ("closes", closes)])
    if len(h) != len(l) or len(h) != len(c) or len(c) < periods + 1:
        raise ScenarioError("insufficient or mismatched completed OHLC")
    for hi, lo, cl in zip(h, l, c):
        if min(hi, lo, cl) <= 0 or not lo <= cl <= hi:
            raise ScenarioError("OHLC inconsistent: close outside low/high")
    ranges = [true_range(h[i], l[i], c[i - 1]) for i in range(1, len(c))]
    atr = sum(ranges[:periods]) / periods
    for tr in ranges[periods:]:
        atr = ((periods - 1) * atr + tr) / periods
    if not isfinite(atr) or atr <= 0:
        raise ScenarioError("ATR unavailable or zero")
    return atr


def hypothetical_levels(high_20: float, atr_14: float,
                        tick_size: str = "0.01") -> dict:
    """Hypothetical 20-session breakout, 1.5xATR risk, 2R/3R targets.

    Parameters are UNVALIDATED, not a forecast or executable fill.
    """
    hi, atr = _finite([high_20, atr_14], "hypothetical levels")
    if hi <= 0 or atr <= 0:
        raise ScenarioError("high/ATR must be positive")
    try:
        tick = Decimal(tick_size)
    except Exception as exc:
        raise ScenarioError("invalid tick size") from exc
    if not tick.is_finite() or tick <= 0:
        raise ScenarioError("invalid tick size")
    entry = _round_tick(hi, tick, "up") + float(tick)
    entry = _round_tick(entry, tick, "up")
    stop = _round_tick(entry - 1.5 * atr, tick, "down")
    if stop <= 0 or stop >= entry:
        raise ScenarioError("nonpositive stop or risk")
    risk = entry - stop
    return {
        "conditional_entry": entry,
        "hypothetical_stop": stop,
        "target_2r": _round_tick(entry + 2 * risk, tick, "up"),
        "target_3r": _round_tick(entry + 3 * risk, tick, "up"),
        "skip_if_open_above": _round_tick(entry + 0.5 * atr, tick, "up"),
        "risk_fraction": risk / entry,
    }


def build_swing_scenario(symbol: str, highs: Sequence[float],
                         lows: Sequence[float], closes: Sequence[float],
                         volumes: Sequence[float], asof: str, *,
                         split_in_recent_window: bool = False,
                         minimum_price: float = 5.0,
                         minimum_dollar_adv: float = 2_000_000,
                         maximum_risk_fraction: float = 0.15) -> SwingScenario:
    """Research-only levels. No bid/ask, backtested edge or trade instruction."""
    h, l, c, v = (_finite(values, name) for name, values in [
        ("highs", highs), ("lows", lows), ("closes", closes), ("volumes", volumes)
    ])
    if len(c) < 21 or any(len(x) != len(c) for x in (h, l, v)):
        return SwingScenario(symbol, "INSUFFICIENT_EVIDENCE",
                             "Need 21 completed and matching OHLCV sessions", asof)
    if any(min(hi, lo, cl) <= 0 or not lo <= cl <= hi or volume < 0
           for hi, lo, cl, volume in zip(h, l, c, v)):
        return SwingScenario(symbol, "INVALID_DATA", "OHLCV invalid", asof)
    if split_in_recent_window:
        return SwingScenario(symbol, "CORPORATE_ACTION_REVIEW",
                             "Recent split needs price-basis validation", asof)
    last_close = c[-1]
    if last_close < minimum_price:
        return SwingScenario(symbol, "EXCLUDED_LOW_PRICE",
                             "Completed close below initial USD 5.00 research floor", asof,
                             reference_close=last_close)
    adv = sum(c[i] * v[i] for i in range(len(c) - 20, len(c))) / 20
    if adv < minimum_dollar_adv:
        return SwingScenario(symbol, "EXCLUDED_LIQUIDITY",
                             "20-session dollar volume below initial floor", asof,
                             reference_close=last_close, avg_dollar_volume_20=adv)
    try:
        atr = atr_wilder(h, l, c, periods=14)
        hh = max(h[-20:])
        levels = hypothetical_levels(hh, atr)
    except ScenarioError as exc:
        return SwingScenario(symbol, "INSUFFICIENT_EVIDENCE", str(exc), asof)
    if levels["risk_fraction"] > maximum_risk_fraction:
        return SwingScenario(symbol, "EXCLUDED_EXCESS_RISK",
                             "ATR-derived entry-to-stop distance exceeds 15%", asof,
                             reference_close=last_close, atr_14=atr, high_20=hh,
                             avg_dollar_volume_20=adv, risk_fraction=levels["risk_fraction"])
    return SwingScenario(symbol, "RESEARCH_ONLY",
                         "UNVALIDATED breakout scenario, not a trade instruction",
                         asof, last_close, hh, atr, adv, **levels)
