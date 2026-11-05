"""Read-only, authenticated Alpaca historical EOD market bars.

Uses only official historical-bar API. Requires the user to provide their own
credentials and agree to provider terms. No trading calls are implemented.
Never log credentials, raw prices, or query contents. Do not publish these
results on public GitHub Pages without verified data display rights.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import pandas as pd

MARKET_DATA_URL = "https://data.alpaca.markets/v2/stocks/bars"
NEW_YORK = ZoneInfo("America/New_York")
FEEDS = {"sip": "Consolidated US exchanges, delayed historical data",
         "iex": "IEX venue only; incomplete market coverage"}


class MarketDataError(RuntimeError):
    pass


def _default_transport(url: str, headers: dict) -> dict:
    """Transport is injectable in tests; no credentials ever in the URL."""
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=25) as response:
            return json.load(response)
    except HTTPError as exc:
        raise MarketDataError(f"Alpaca HTTP {exc.code}; verify credentials, feed entitlement or rate limits") from None
    except (URLError, TimeoutError) as exc:
        raise MarketDataError("Alpaca network unavailable") from exc


def fetch_alpaca_bars(symbol: str, *, now: datetime | None = None,
                      feed: str = "sip", transport=None,
                      key_id: str | None = None,
                      secret_key: str | None = None) -> pd.DataFrame:
    """Return split-adjusted OHLCV in current share units, completed sessions only.

    Historical SIP is typically available on basic accounts once data is
    older than the provider's recent-15-minute window. Subscription/rights
    must still be verified by the user. Never automatically downgrade SIP
    to IEX when entitlement fails.
    """
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        raise MarketDataError("Current time must be timezone-aware")
    if feed not in FEEDS:
        raise MarketDataError("Allowed market feeds: sip or iex")
    if not symbol.isascii() or not symbol.replace(".", "").replace("-", "").isalnum():
        raise MarketDataError("Invalid stock symbol")
    api_id = key_id or os.environ.get("ALPACA_API_KEY_ID")
    api_secret = secret_key or os.environ.get("ALPACA_API_SECRET_KEY")
    if not api_id or not api_secret:
        raise MarketDataError("Alpaca data credentials not configured")
    ny = current.astimezone(NEW_YORK)
    # Do not include the current date until after 17:00 NY time.
    latest_allowed_date = ny.date() if ny.hour >= 17 else ny.date() - timedelta(days=1)
    # Query the prior 580 calendar days, enough for ~18 months of daily bars.
    start = (ny.date() - timedelta(days=580)).isoformat()
    end = (current - timedelta(minutes=25)).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    headers = {"APCA-API-KEY-ID": api_id,
               "APCA-API-SECRET-KEY": api_secret,
               "Accept": "application/json"}
    call = transport or _default_transport
    observations = []
    next_page = None
    seen_tokens = set()
    for _ in range(12):
        query = {
            "symbols": symbol, "timeframe": "1Day", "start": start,
            "end": end, "adjustment": "split", "feed": feed,
            "limit": "1000", "sort": "asc"
        }
        if next_page:
            query["page_token"] = next_page
        payload = call(MARKET_DATA_URL + "?" + urlencode(query), headers)
        if not isinstance(payload, dict) or not isinstance(payload.get("bars"), dict):
            raise MarketDataError("Unexpected Alpaca market-data response")
        observations.extend(payload["bars"].get(symbol, []))
        next_page = payload.get("next_page_token")
        if not next_page:
            break
        if next_page in seen_tokens:
            raise MarketDataError("Alpaca repeated its pagination token")
        seen_tokens.add(next_page)
    else:
        raise MarketDataError("Alpaca history exceeded safe pagination limit")
    rows = []
    for bar in observations:
        try:
            ts = datetime.fromisoformat(bar["t"].replace("Z", "+00:00"))
            if ts.tzinfo is None:
                raise ValueError("timezone absent")
            session = ts.astimezone(NEW_YORK).date()
            if session > latest_allowed_date:
                continue
            row = {
                "date": session, "High": float(bar["h"]), "Low": float(bar["l"]),
                "Close": float(bar["c"]), "Volume": float(bar["v"])
            }
        except (TypeError, KeyError, ValueError, OverflowError) as exc:
            raise MarketDataError("Malformed Alpaca daily bar") from exc
        if not (row["Volume"] >= 0 and row["Low"] > 0 and
                row["Low"] <= row["Close"] <= row["High"]):
            raise MarketDataError("Alpaca daily OHLCV invalid")
        rows.append(row)
    if not rows:
        raise MarketDataError("No completed daily bars found")
    df = pd.DataFrame(rows).set_index("date").sort_index()
    if df.index.has_duplicates:
        raise MarketDataError("Duplicate daily bars from provider")
    # Also protect downstream calculations against NaN/infinite values.
    if not df.apply(lambda column: column.map(pd.notna)).all().all():
        raise MarketDataError("Missing daily OHLCV")
    if not df.map(lambda val: bool(pd.notna(val) and abs(val) < 1e18)).all().all():
        raise MarketDataError("Nonfinite or unreasonable market observation")
    if len(df) < 21:
        raise MarketDataError("Fewer than 21 completed trading sessions")
    return df


def provider_label(feed: str) -> str:
    return f"Alpaca {feed.upper()} historical 1Day bars, split-adjusted; {FEEDS[feed]}"
