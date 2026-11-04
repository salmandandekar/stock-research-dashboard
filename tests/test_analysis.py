import numpy as np
import pandas as pd
import pytest
from analyze import analyze_stock, render


def history(start, end, count=320):
    idx = pd.bdate_range(end="2026-11-04", periods=count)
    return pd.Series(np.linspace(start, end, count), index=idx)


def test_uptrend_candidate():
    stock = analyze_stock("UP", history(50, 150), today=pd.Timestamp("2026-11-04").date())
    assert stock["score"] == 100
    assert stock["signal"] == "Research candidate"


def test_downtrend():
    stock = analyze_stock("DOWN", history(150, 50), today=pd.Timestamp("2026-11-04").date())
    assert stock["score"] < 40


def test_insufficient_history():
    with pytest.raises(ValueError, match="210"):
        analyze_stock("NEW", history(90, 110, 100))


def test_stale_score_suppressed_on_site():
    stock = analyze_stock("UP", history(50, 150), today=pd.Timestamp("2026-11-15").date())
    assert stock["stale"]
    page = render([stock], [], "2026-11-15 00:00 UTC")
    assert "Stale data" in page
    assert "Scores do not assess intrinsic value" in page
    assert "100/100" not in page
