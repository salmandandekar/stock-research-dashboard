"""Deterministic research calculations: QFCS v1.3 initial implementation.

This module computes descriptive metrics and synthetic scenario arithmetic.
It is NOT an investment-advice, order-execution, or predictive model.
Each function references the corresponding approved requirement ID.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite, sqrt
from statistics import mean, stdev
from typing import Sequence


class QuantInputError(ValueError):
    """Invalid or insufficient financial evidence; caller must abstain."""


def finite(value: float, label: str = "value") -> float:
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise QuantInputError(f"{label}: not a finite numeric value") from exc
    if not isfinite(number):
        raise QuantInputError(f"{label}: not finite")
    return number


def positive(value: float, label: str = "value") -> float:
    number = finite(value, label)
    if number <= 0:
        raise QuantInputError(f"{label}: must be positive")
    return number


def _values(values: Sequence[float], min_count: int = 1) -> list[float]:
    if len(values) < min_count:
        raise QuantInputError(f"need at least {min_count} observations")
    return [finite(v, f"observations[{i}]") for i, v in enumerate(values)]


def price_return(p0: float, p1: float) -> float:
    """QF-M01: price-only simple return, NOT dividend total return."""
    return finite(p1, "p1") / positive(p0, "p0") - 1


def total_return(p0: float, p1: float, cash_dividends: float = 0,
                 *, dividend_adjusted: bool = False) -> float:
    """QF-M02: same-share-unit, cash-dividend holding return."""
    if dividend_adjusted and cash_dividends != 0:
        raise QuantInputError("dividend double counting")
    return (finite(p1) + finite(cash_dividends) -
            positive(p0, "p0")) / positive(p0, "p0")


def compound_return(returns: Sequence[float]) -> float:
    """QF-M04: geometric compounding."""
    v = 1.0
    for r in _values(returns):
        if r < -1:
            raise QuantInputError("single-period loss below -100%")
        v *= 1 + r
    return v - 1


def daily_volatility(returns: Sequence[float], annual_sessions: int = 252) -> float:
    """QF-M05: daily sample standard deviation and annualization convention."""
    if annual_sessions <= 0:
        raise QuantInputError("invalid annual_sessions")
    r = _values(returns, 2)
    return stdev(r) * sqrt(annual_sessions)


def sma(prices: Sequence[float], window: int) -> float:
    """QF-M06: n completed daily observations."""
    if window < 1:
        raise QuantInputError("window must be positive")
    return mean(_values(prices, window)[-window:])


def ema(prices: Sequence[float], window: int) -> float:
    """QF-M07: seed with SMA then alpha=2/(n+1)."""
    values = _values(prices, window)
    if window < 1:
        raise QuantInputError("window must be positive")
    result = mean(values[:window])
    alpha = 2 / (window + 1)
    for p in values[window:]:
        result = alpha * p + (1 - alpha) * result
    return result


def max_drawdown(wealth: Sequence[float]) -> float:
    """QF-M11/B06: maximum peak-to-trough loss as a positive fraction."""
    values = _values(wealth)
    if any(v <= 0 for v in values):
        raise QuantInputError("wealth series must be positive")
    peak = values[0]
    worst = 0.0
    for value in values:
        peak = max(peak, value)
        worst = max(worst, 1 - value / peak)
    return worst


def quoted_spread_bps(bid: float, ask: float) -> float:
    """QF-M15: spread / midpoint, in basis points."""
    bid, ask = positive(bid, "bid"), positive(ask, "ask")
    if ask < bid:
        raise QuantInputError("crossed market")
    return 10000 * (ask - bid) / ((ask + bid) / 2)


def free_cash_flow(operating_cash_flow: float, positive_capex_outflow: float) -> float:
    """QF-F04: basic unlevered-to-owner FCF proxy; NOT FCFF."""
    capex = finite(positive_capex_outflow, "positive_capex_outflow")
    if capex < 0:
        raise QuantInputError("capex must be a positive cash outflow")
    return finite(operating_cash_flow) - capex


def gross_margin(revenue: float, cost_of_goods_sold: float) -> float:
    """QF-F03: GAAP gross margin when mapping is valid."""
    return (positive(revenue, "revenue") -
            finite(cost_of_goods_sold)) / positive(revenue, "revenue")


def roic(ebit: float, tax_rate: float, beginning_capital: float,
         ending_capital: float) -> float:
    """QF-F06: NOPAT / average coherent operating invested capital."""
    tax = finite(tax_rate, "tax")
    if not 0 <= tax <= 1:
        raise QuantInputError("tax outside [0,1]")
    invested = (finite(beginning_capital) + finite(ending_capital)) / 2
    return finite(ebit) * (1 - tax) / positive(invested, "average invested capital")


def wacc(equity_weight: float, debt_weight: float, cost_equity: float,
         cost_debt: float, tax_rate: float) -> float:
    """QF-V02: non-preferred WACC; weights must add to one."""
    e, d = finite(equity_weight), finite(debt_weight)
    tax = finite(tax_rate)
    if e < 0 or d < 0 or abs(e + d - 1) > 1e-10 or not 0 <= tax <= 1:
        raise QuantInputError("invalid capital weights or tax")
    ke, kd = finite(cost_equity), finite(cost_debt)
    if ke < 0 or kd < 0:
        raise QuantInputError("negative discount rate")
    return e * ke + d * kd * (1 - tax)


def fcff(ebit: float, tax_rate: float, depreciation: float,
         capex_outflow: float, increase_non_cash_nwc: float) -> float:
    """QF-V03: free cash flow to the firm with positive CAPEX outflow."""
    tax = finite(tax_rate)
    if not 0 <= tax <= 1 or finite(capex_outflow) < 0 or finite(depreciation) < 0:
        raise QuantInputError("invalid tax/depreciation/capex")
    return (finite(ebit) * (1 - tax) + finite(depreciation)
            - finite(capex_outflow) - finite(increase_non_cash_nwc))


def dcf_enterprise_value(future_fcff: Sequence[float], discount_rate: float,
                         terminal_growth: float) -> float:
    """QF-V04/V05: end-year FCFF DCF using Gordon terminal at last forecast year."""
    flows = _values(future_fcff)
    rate, growth = finite(discount_rate), finite(terminal_growth)
    if rate <= growth or rate <= -1 or growth <= -1 or flows[-1] <= 0:
        raise QuantInputError("invalid perpetuity or discount rate")
    terminal = flows[-1] * (1 + growth) / (rate - growth)
    return (sum(cf / (1 + rate) ** (i + 1) for i, cf in enumerate(flows))
            + terminal / (1 + rate) ** len(flows))


def common_value_per_share(enterprise_value: float, excess_cash: float,
                           debt_and_other_claims: float,
                           economic_diluted_shares: float) -> float:
    """QF-V06/V07: simplified equity bridge, *only when claims are not double counted*."""
    equity = (finite(enterprise_value) + finite(excess_cash) -
              finite(debt_and_other_claims))
    return equity / positive(economic_diluted_shares, "economic diluted shares")


def valuation_upside(market_price: float, value_per_share: float) -> float:
    """QF-V08: modeled upside (different from margin-of-safety denominator)."""
    return finite(value_per_share) / positive(market_price) - 1


@dataclass(frozen=True)
class ExecutedLong:
    shares: float
    entry_cash: float
    exit_cash: float
    net_pnl: float
    net_roi: float


def long_trade_pnl(shares: float, buy_exec: float, sell_exec: float,
                   buy_fee: float = 0, sell_fee: float = 0) -> ExecutedLong:
    """QF-T01: exact long buy/sell cash accounting. Executed prices INCLUDE quoted spread."""
    qty, buy, sell = positive(shares, "shares"), positive(buy_exec), positive(sell_exec)
    fee_in, fee_out = finite(buy_fee), finite(sell_fee)
    if fee_in < 0 or fee_out < 0:
        raise QuantInputError("negative fee")
    entry, exit_cash = qty * buy + fee_in, qty * sell - fee_out
    profit = exit_cash - entry
    return ExecutedLong(qty, entry, exit_cash, profit, profit / entry)


def expected_net_return(p_win: float, gross_win: float, gross_loss_abs: float,
                        round_trip_cost_fraction: float) -> float:
    """QF-T04: two-outcome gross payoff model less costs once; NOT a predictive estimator."""
    p = finite(p_win)
    gain, loss = finite(gross_win), finite(gross_loss_abs)
    cost = finite(round_trip_cost_fraction)
    if not 0 <= p <= 1 or min(gain, loss, cost) < 0:
        raise QuantInputError("invalid outcome probability/return/cost")
    return p * gain - (1 - p) * loss - cost


def time_weighted_return(subperiod_returns: Sequence[float]) -> float:
    """QF-B01: geometric linking of cashflow-separated holding periods."""
    return compound_return(subperiod_returns)


def brier_score(predictions: Sequence[float], outcomes: Sequence[int]) -> float:
    """QF-S04: Brier score for an independently defined, observed binary event."""
    ps = _values(predictions)
    if len(ps) != len(outcomes):
        raise QuantInputError("prediction/outcome count mismatch")
    for p, y in zip(ps, outcomes):
        if not 0 <= p <= 1 or y not in (0, 1):
            raise QuantInputError("probability/outcome outside valid range")
    return mean((p - y) ** 2 for p, y in zip(ps, outcomes))


def signal_is_usable(source_available_at: datetime, signal_at: datetime,
                     expires_at: datetime, published_at: datetime,
                     *, publication_rights_verified: bool,
                     tested_after_cost_edge: bool) -> bool:
    """QF-R02 / ST-SM: deterministic evidence and freshness gates.

    The proof of permission and OOS validation must occur *outside* this function.
    False is a valid NO_TRADE outcome.
    """
    timestamps = (source_available_at, signal_at, expires_at, published_at)
    if any(t.tzinfo is None or t.utcoffset() is None for t in timestamps):
        raise QuantInputError("timestamps require timezone offsets")
    return (publication_rights_verified and tested_after_cost_edge and
            source_available_at <= signal_at <= published_at < expires_at)
