"""Read-only Alpaca adapter tests with a fake transport: NO network or credentials."""
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import pandas as pd
import pytest

from market_data_alpaca import MarketDataError, fetch_alpaca_bars, provider_label


def payload_bars(last="2026-11-04", n=25):
    dates = pd.bdate_range(end=last, periods=n)
    return [{"t": str(day.date()) + "T15:00:00Z",
             "h": 10.5, "l": 9.5, "c": 10.0, "v": 300_000}
            for day in dates]


def test_sip_fetch_is_authenticated_split_adjusted_and_page_aware():
    bars = payload_bars()
    calls = []
    def fake(url, headers):
        query = parse_qs(urlparse(url).query)
        calls.append((query, headers))
        if "page_token" not in query:
            return {"bars": {"MNSO": bars[:10]}, "next_page_token": "NEXT"}
        return {"bars": {"MNSO": bars[10:]}, "next_page_token": None}
    df = fetch_alpaca_bars(
        "MNSO", now=datetime(2026, 11, 5, 22, tzinfo=timezone.utc),
        feed="sip", transport=fake, key_id="dummy-id", secret_key="dummy-secret")
    assert len(df) == 25
    assert len(calls) == 2
    assert calls[0][0]["feed"] == ["sip"]
    assert calls[0][0]["adjustment"] == ["split"]
    assert calls[0][0]["timeframe"] == ["1Day"]
    assert calls[0][1]["APCA-API-KEY-ID"] == "dummy-id"
    assert calls[0][1]["APCA-API-SECRET-KEY"] == "dummy-secret"
    assert df.iloc[-1]["Close"] == pytest.approx(10)
    assert "IEX" in provider_label("iex")


def test_exclude_unfinished_current_session_even_if_provider_returns_it():
    bars = payload_bars(last="2026-11-05", n=26)
    def fake(url, headers):
        return {"bars": {"AAPL": bars}, "next_page_token": None}
    df = fetch_alpaca_bars(
        "AAPL", now=datetime(2026, 11, 5, 19, tzinfo=timezone.utc),
        feed="sip", transport=fake, key_id="dummy-id", secret_key="dummy-secret")
    assert df.index[-1].isoformat() == "2026-11-04"


def test_credentials_are_required_and_never_leak_into_error(monkeypatch):
    monkeypatch.delenv("ALPACA_API_KEY_ID", raising=False)
    monkeypatch.delenv("ALPACA_API_SECRET_KEY", raising=False)
    with pytest.raises(MarketDataError, match="credentials"):
        fetch_alpaca_bars("MSFT", now=datetime(2026, 11, 5, 22, tzinfo=timezone.utc))


def test_invalid_bar_must_not_be_used():
    bars = payload_bars()
    bars[-1]["h"] = 8
    def fake(url, headers):
        return {"bars": {"AAPL": bars}}
    with pytest.raises(MarketDataError, match="invalid"):
        fetch_alpaca_bars("AAPL", now=datetime(2026, 11, 5, 22, tzinfo=timezone.utc),
                          transport=fake, key_id="dummy-id", secret_key="dummy-secret")


def test_fail_closed_if_only_few_completed_bars():
    def fake(url, headers):
        return {"bars": {"AAPL": payload_bars(n=15)}}
    with pytest.raises(MarketDataError, match="Fewer than 21"):
        fetch_alpaca_bars("AAPL", now=datetime(2026, 11, 5, 22, tzinfo=timezone.utc),
                          transport=fake, key_id="dummy-id", secret_key="dummy-secret")


def test_unknown_feed_and_bad_symbols_rejected():
    with pytest.raises(MarketDataError):
        fetch_alpaca_bars("AAPL", feed="magic", key_id="id", secret_key="secret")
    with pytest.raises(MarketDataError):
        fetch_alpaca_bars("AAPL/../../x", feed="sip", key_id="id", secret_key="secret")
