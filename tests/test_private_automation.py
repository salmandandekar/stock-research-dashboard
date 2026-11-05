"""Offline private automatic report integration and privacy/abstention tests."""
from datetime import datetime, timezone

import pandas as pd
import pytest

from private_trade_report import (
    _destination, _synthetic_bars, analyze_private_bars, build_reports
)
from analyze import ROOT


NOW = datetime(2026, 11, 5, 22, tzinfo=timezone.utc)


def test_generate_automatic_html_and_csv_no_manual_quote_entry(tmp_path):
    report = build_reports(
        fetcher=_synthetic_bars, output_dir=tmp_path, now=NOW,
        feed="sip", source="SYNTHETIC TEST", demo=True
    )
    assert report["count"] == 13
    assert report["scenarios"] == 10
    assert report["fresh_count"] == 13
    html = (tmp_path / "demo_latest.html").read_text(encoding="utf-8")
    csv = (tmp_path / "demo_latest.csv").read_text(encoding="utf-8")
    assert "SYNTHETIC DEMO — NOT REAL MARKET PRICES" in html
    assert "USD 10.51" in html
    assert "USD 9.01" in html
    assert "USD 13.51" in html
    assert "USD 15.01" in html
    assert "EXCLUDED LOW PRICE" in html
    assert "ALPACA_API_SECRET" not in html
    assert "RESEARCH ONLY" in html
    assert "LUNR" in csv and "FLNA" in csv
    assert "10.51" in csv
    assert not (tmp_path / "latest.html").exists()


def test_refuse_to_put_market_levels_in_public_site():
    with pytest.raises(ValueError, match="Refusing"):
        _destination(ROOT / "site")


def test_limited_iex_coverage_never_claims_full_market():
    row = analyze_private_bars("AAPL", _synthetic_bars("AAPL"),
                               now=NOW, feed="iex")
    assert row["setup_status"] == "LIMITED_FEED"
    assert "entry" not in row


def test_stale_data_denies_levels():
    row = analyze_private_bars(
        "AAPL", _synthetic_bars("AAPL"),
        now=datetime(2026, 11, 18, 22, tzinfo=timezone.utc),
        feed="sip")
    assert row["setup_status"] == "STALE"
    assert "entry" not in row


def test_corporate_action_anomaly_denies_levels():
    frame = _synthetic_bars("AAPL")
    frame.iloc[-1, frame.columns.get_loc("Close")] = 20
    frame.iloc[-1, frame.columns.get_loc("High")] = 20.5
    row = analyze_private_bars("AAPL", frame, now=NOW, feed="sip")
    assert row["setup_status"] == "CORPORATE_ACTION_REVIEW"
    assert "entry" not in row


def test_missing_data_keeps_previous_report_intact(tmp_path):
    existing = tmp_path / "latest.html"
    existing.write_text("previous valid snapshot", encoding="utf-8")
    def only_one(symbol):
        if symbol != "AAPL":
            raise RuntimeError("Network source failed")
        return _synthetic_bars(symbol)
    with pytest.raises(RuntimeError, match="Fresh-data gate"):
        build_reports(fetcher=only_one, output_dir=tmp_path,
                      now=NOW, feed="sip", source="TEST")
    assert existing.read_text(encoding="utf-8") == "previous valid snapshot"
    assert not (tmp_path / "latest.csv").exists()


def test_real_mode_outputs_to_latest_when_mocked_and_source_is_preserved(tmp_path):
    report = build_reports(fetcher=_synthetic_bars, output_dir=tmp_path,
                           now=NOW, feed="sip", source="AUTHORIZED TEST")
    assert report["scenarios"] == 10
    assert (tmp_path / "latest.html").exists()
    text = (tmp_path / "latest.html").read_text(encoding="utf-8")
    assert "AUTHORIZED TEST" in text
    assert "USD 10.51" in text
    assert "No automatic orders" in text
    assert (tmp_path / "latest.csv").exists()
