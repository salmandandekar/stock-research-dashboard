"""Independent arithmetic and adverse-condition tests for first QFCS implementation.

Scope: these tests verify numerical mechanics and gates, not real market alpha.
"""
from datetime import datetime, timezone, timedelta

import pytest

from quant_core import (
    QuantInputError, price_return, total_return, compound_return, daily_volatility,
    sma, ema, max_drawdown, quoted_spread_bps, free_cash_flow, gross_margin,
    roic, wacc, fcff, dcf_enterprise_value, common_value_per_share,
    valuation_upside, long_trade_pnl, expected_net_return, time_weighted_return,
    brier_score, signal_is_usable
)


def test_price_return_vs_total_return():
    assert price_return(100, 105) == pytest.approx(.05)
    assert total_return(100, 105, 1) == pytest.approx(.06)
    with pytest.raises(QuantInputError, match="double counting"):
        total_return(100, 105, 1, dividend_adjusted=True)


def test_compounded_return_not_sum():
    assert compound_return([.10, -.05]) == pytest.approx(.045)
    assert time_weighted_return([.1, -.05]) == pytest.approx(.045)


@pytest.mark.parametrize("prices,n,expected", [
    ([10, 20, 30, 40, 50], 3, 40),
    ([10, 20, 30], 3, 20),
    ([10], 1, 10),
])
def test_sma(prices, n, expected):
    assert sma(prices, n) == pytest.approx(expected)


def test_sma_ema_reject_missing_or_bad_windows():
    with pytest.raises(QuantInputError):
        sma([1, 2, 3], 5)
    with pytest.raises(QuantInputError):
        ema([1, 2, 3], 0)
    assert ema([10, 20, 30, 40], 3) == pytest.approx(30)


def test_volatility_requires_samples_and_is_finite():
    assert daily_volatility([0, 0.01, -0.01]) > 0
    with pytest.raises(QuantInputError):
        daily_volatility([.01])


def test_max_drawdown_compares_all_prior_peaks():
    assert max_drawdown([100, 110, 99, 120, 90, 115]) == pytest.approx(.25)


def test_bid_ask_spread_and_crossed_market():
    assert quoted_spread_bps(99.9, 100.1) == pytest.approx(20)
    assert quoted_spread_bps(100, 100) == 0
    with pytest.raises(QuantInputError, match="crossed"):
        quoted_spread_bps(100.2, 100.1)


def test_fundamentals_and_negative_roic_denominator():
    assert free_cash_flow(120, 50) == 70
    assert gross_margin(100, 65) == pytest.approx(.35)
    assert roic(150, .25, 500, 550) == pytest.approx(.21428571428571427)
    with pytest.raises(QuantInputError):
        roic(150, .25, -10, 0)
    with pytest.raises(QuantInputError):
        free_cash_flow(100, -20)


def test_wacc_valid_weights_only():
    assert wacc(.8, .2, .10, .05, .25) == pytest.approx(.0875)
    with pytest.raises(QuantInputError):
        wacc(.9, .2, .10, .05, .25)


def test_fcff_and_terminal_growth_guard():
    assert fcff(100, .25, 10, 20, 5) == pytest.approx(60)
    assert dcf_enterprise_value([100, 110, 121], .10, .03) == pytest.approx(
        1610.38961038961)
    with pytest.raises(QuantInputError):
        dcf_enterprise_value([100], .02, .03)


def test_equity_bridge_and_upside():
    value = common_value_per_share(1610.38961038961, 50, 300, 50)
    assert value == pytest.approx(27.2077922077922)
    assert valuation_upside(80, 100) == pytest.approx(.25)
    with pytest.raises(QuantInputError):
        common_value_per_share(100, 1, 20, 0)


def test_long_trade_exact_cashflow_no_double_spread():
    trade = long_trade_pnl(100, 100.10, 101.20, 1, 1)
    assert trade.entry_cash == pytest.approx(10011)
    assert trade.exit_cash == pytest.approx(10119)
    assert trade.net_pnl == pytest.approx(108)
    assert trade.net_roi == pytest.approx(108 / 10011)
    instant = long_trade_pnl(1, 100.2, 100, 0, 0)
    assert instant.net_roi == pytest.approx(100 / 100.2 - 1)


def test_high_win_rate_can_lose_after_costs():
    assert expected_net_return(.55, .015, .02, .0015) == pytest.approx(-.00225)


def test_brier_is_bounded():
    assert brier_score([.8, .2], [1, 0]) == pytest.approx(.04)
    with pytest.raises(QuantInputError):
        brier_score([.8], [2])


def test_invalid_inputs_fail_closed():
    for value in (float("nan"), float("inf")):
        with pytest.raises(QuantInputError):
            price_return(1, value)
    with pytest.raises(QuantInputError):
        price_return(0, 100)
    with pytest.raises(QuantInputError):
        compound_return([-1.5])


def test_timing_entitlement_and_validation_gate():
    base = datetime(2026, 11, 4, 16, tzinfo=timezone.utc)
    kwargs = dict(
        source_available_at=base,
        signal_at=base + timedelta(minutes=1),
        published_at=base + timedelta(minutes=5),
        expires_at=base + timedelta(minutes=30),
        publication_rights_verified=True,
        tested_after_cost_edge=True,
    )
    assert signal_is_usable(**kwargs)
    assert not signal_is_usable(**{**kwargs, "tested_after_cost_edge": False})
    assert not signal_is_usable(**{**kwargs, "publication_rights_verified": False})
    assert not signal_is_usable(**{**kwargs, "published_at": base + timedelta(hours=1)})
    assert not signal_is_usable(**{**kwargs, "source_available_at": base + timedelta(hours=1)})
    with pytest.raises(QuantInputError):
        signal_is_usable(**{**kwargs, "signal_at": datetime(2026, 11, 4, 16)})
