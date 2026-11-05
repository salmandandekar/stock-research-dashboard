"""Integration tests for source-rights controls and unvalidated trading scenarios."""
from datetime import date

import pandas as pd
import numpy as np

from analyze import analyze_history, render


def example_history(n=320, close=10.0, volume=300000):
    idx = pd.bdate_range(end="2026-11-04", periods=n)
    return pd.DataFrame({
        "High": np.full(n, close + .50),
        "Low": np.full(n, close - .50),
        "Close": np.full(n, close),
        "Adj Close": np.full(n, close),
        "Volume": np.full(n, volume),
        "Stock Splits": np.zeros(n),
    }, index=idx)


def test_full_report_has_research_status_but_no_unlicensed_prices():
    frame = example_history(close=37.00, volume=300000)
    result = analyze_history("ABC", frame, today=date(2026, 11, 5))
    assert result["plan_status"] == "RESEARCH_ONLY"
    assert result["scenario"].conditional_entry == 37.51
    html = render([result], [], "2026-11-05 20:00 UTC")
    assert "ABC" in html
    assert "RESEARCH ONLY" in html
    assert "not published automatically" in html
    assert "$37.51" not in html
    assert "37.51" not in html
    assert "research-plan-calculator" in html


def test_recent_corporate_action_invalidates_levels():
    frame = example_history()
    frame.iloc[-2, frame.columns.get_loc("Stock Splits")] = 10
    result = analyze_history("SPLIT", frame, today=date(2026, 11, 5))
    assert result["plan_status"] == "CORPORATE_ACTION_REVIEW"
    assert result["scenario"].conditional_entry is None


def test_low_price_risk_visible_without_executable_levels():
    frame = example_history(close=.75, volume=12_000_000)
    result = analyze_history("FLNA", frame, today=date(2026, 11, 5))
    assert result["plan_status"] == "EXCLUDED_LOW_PRICE"
    assert result["scenario"].conditional_entry is None
    html = render([result], [], "2026-11-05")
    assert "EXCLUDED LOW PRICE" in html


def test_short_history_still_lists_symbol_and_shows_scenario_gate():
    frame = example_history(n=100)
    result = analyze_history("NEW", frame, today=date(2026, 11, 5))
    assert result["score"] is None
    assert result["symbol"] == "NEW"
    assert result["scenario"] is not None
    html = render([result], [], "2026-11-05")
    assert "NEW" in html
    assert "—" in html


def test_stale_date_no_current_scenario():
    frame = example_history()
    result = analyze_history("OLD", frame, today=date(2026, 12, 1))
    assert result["plan_status"] == "STALE"
    assert "Stale" in render([result], [], "2026-12-01")
