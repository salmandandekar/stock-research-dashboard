"""Synthetic, reproducible swing-scenario and red-team tests."""
import pytest

from trade_plan import (ScenarioError, true_range, atr_wilder,
                        hypothetical_levels, build_swing_scenario)


def bars(close=10.0, hi=10.5, lo=9.5, n=35, volume=300_000):
    return ([hi] * n, [lo] * n, [close] * n, [volume] * n)


def test_true_range_prior_close_gap():
    assert true_range(105, 100, 90) == pytest.approx(15)


def test_wilder_atr_constant_range():
    h, l, c, _ = bars()
    assert atr_wilder(h, l, c) == pytest.approx(1.0)


def test_wilder_rejects_invalid_close_or_insufficient_data():
    h, l, c, _ = bars(n=5)
    with pytest.raises(ScenarioError, match="insufficient"):
        atr_wilder(h, l, c)
    h, l, c, _ = bars()
    c[-1] = 11
    with pytest.raises(ScenarioError, match="inconsistent"):
        atr_wilder(h, l, c)


def test_levels_arithmetic_and_risk_reward():
    p = hypothetical_levels(high_20=10.50, atr_14=1.00)
    assert p["conditional_entry"] == pytest.approx(10.51)
    assert p["hypothetical_stop"] == pytest.approx(9.01)
    assert p["target_2r"] == pytest.approx(13.51)
    assert p["target_3r"] == pytest.approx(15.01)
    assert p["skip_if_open_above"] == pytest.approx(11.01)
    assert p["risk_fraction"] == pytest.approx(1.5 / 10.51)


def test_scenario_valid_is_research_only_not_a_trade_signal():
    h, l, c, v = bars()
    x = build_swing_scenario("TEST", h, l, c, v, "2026-11-04")
    assert x.status == "RESEARCH_ONLY"
    assert x.has_levels()
    assert x.conditional_entry == pytest.approx(10.51)
    assert x.asof == "2026-11-04"
    assert x.horizon_sessions == 5
    assert "UNVALIDATED" in x.reason


def test_penny_stock_is_monitored_but_no_buy_levels():
    h, l, c, v = bars(close=0.75, hi=0.80, lo=0.70, volume=12_000_000)
    x = build_swing_scenario("URG", h, l, c, v, "2026-11-04")
    assert x.status == "EXCLUDED_LOW_PRICE"
    assert not x.has_levels()


def test_liquidity_floor_prevents_hypothetical_trade():
    h, l, c, v = bars(volume=10)
    x = build_swing_scenario("THIN", h, l, c, v, "2026-11-04")
    assert x.status == "EXCLUDED_LIQUIDITY"
    assert not x.has_levels()


def test_corporate_action_requires_revalidation():
    h, l, c, v = bars()
    x = build_swing_scenario("SPLIT", h, l, c, v, "2026-11-04",
                             split_in_recent_window=True)
    assert x.status == "CORPORATE_ACTION_REVIEW"
    assert not x.has_levels()


def test_risk_ceiling_abstains():
    h, l, c, v = bars(hi=11.5, lo=8.5)
    x = build_swing_scenario("RISK", h, l, c, v, "2026-11-04")
    assert x.status == "EXCLUDED_EXCESS_RISK"
    assert not x.has_levels()


def test_bad_ohlc_rejected_before_trade():
    h, l, c, v = bars()
    h[-1] = 8
    x = build_swing_scenario("BAD", h, l, c, v, "2026-11-04")
    assert x.status == "INVALID_DATA"
    assert not x.has_levels()


def test_missing_history_abstains():
    h, l, c, v = bars(n=15)
    x = build_swing_scenario("NEW", h, l, c, v, "2026-11-04")
    assert x.status == "INSUFFICIENT_EVIDENCE"
    assert not x.has_levels()


def test_invalid_nan_rejected():
    h, l, c, v = bars()
    h[-1] = float("nan")
    with pytest.raises(ScenarioError, match="NaN"):
        build_swing_scenario("BAD", h, l, c, v, "2026-11-04")


def test_flat_market_has_no_atr_no_setup():
    h, l, c, v = bars(hi=10, lo=10, close=10)
    x = build_swing_scenario("FLAT", h, l, c, v, "2026-11-04")
    assert x.status == "INSUFFICIENT_EVIDENCE"


def test_levels_cannot_use_zero_or_invalid_tick():
    with pytest.raises(ScenarioError):
        hypothetical_levels(10, 0)
    with pytest.raises(ScenarioError):
        hypothetical_levels(10, 1, tick_size="0")


def test_current_symbol_list_has_eight_new_entries():
    import json
    from pathlib import Path
    data = json.loads((Path(__file__).resolve().parents[1] / "watchlist.json").read_text())
    expected = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
                "LUNR", "MNSO", "GRRR", "URG", "LTRX", "LCID", "NOK", "FLNA"}
    assert set(data["tickers"]) == expected
    assert data["publication"]["show_price_levels"] is False
