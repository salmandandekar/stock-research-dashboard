"""Contract completeness tests for the *requirements documents*, not the stock engine.

Do not present passing checks here as validation of trading strategies or actual
financial calculation functions. Engineers must separately implement all math,
adversarial and point-in-time tests before enabling financial signals.
"""
import json
import math
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "01_MARKET_MATH.md": ("M", 20),
    "02_FUNDAMENTALS.md": ("F", 20),
    "03_VALUATION.md": ("V", 16),
    "04_EXECUTION_COSTS.md": ("T", 20),
    "05_PORTFOLIO_RISK.md": ("B", 20),
    "06_STATISTICAL_VALIDATION.md": ("S", 20),
}


def _load_vectors():
    result = []
    for name in ("quant_vectors_A.json", "quant_vectors_B.json"):
        doc = json.loads((ROOT / "tests" / "specs" / name).read_text("utf-8"))
        assert doc["schema"] == "QFCS-GOLDEN-v1.3"
        assert doc["verified"] == "ARITHMETIC_EXAMPLES_ONLY_NOT_EXECUTED_TESTS"
        result.extend(doc["cases"])
    return result


def test_formula_id_inventory_is_unique_and_complete():
    all_ids = []
    for filename, (category, count) in MODULES.items():
        text = (ROOT / "docs" / "quant" / filename).read_text("utf-8")
        found = re.findall(r"(?m)^\\| (QF-" + category + r"\\d{2}) \\|", text)
        assert len(found) == count, (filename, len(found), count)
        assert len(set(found)) == count
        all_ids.extend(found)
    assert len(set(all_ids)) == 116


def test_golden_vector_specs_have_ids_valid_formula_references_and_finite_numbers():
    ids = set()
    formulas = set()
    for filename in MODULES:
        text = (ROOT / "docs" / "quant" / filename).read_text("utf-8")
        formulas.update(re.findall(r"QF-[MFVTBS]\\d{2}", text))
    cases = _load_vectors()
    assert len(cases) == 40
    for case in cases:
        assert case["id"] not in ids
        ids.add(case["id"])
        assert case["formula"] in formulas
        assert isinstance(case["input"], dict)
        assert isinstance(case["expected"], dict) and case["expected"]
        for value in case["expected"].values():
            if isinstance(value, (int, float)):
                assert math.isfinite(value)


def test_independently_recomputed_selected_synthetic_examples():
    by_id = {c["id"]: c for c in _load_vectors()}
    assert by_id["G01"]["expected"]["value"] == pytest.approx(105 / 100 - 1)
    assert by_id["G02"]["expected"]["value"] == pytest.approx((105 + 1) / 100 - 1)
    assert by_id["G03"]["expected"]["value"] == pytest.approx(1.10 * 0.95 - 1)
    assert by_id["G07"]["expected"]["wacc"] == pytest.approx(0.8 * 0.1 + 0.2 * 0.05 * 0.75)
    flows = [100, 110, 121]
    tv = flows[-1] * 1.03 / (0.10 - 0.03)
    ev = sum(x / 1.10 ** (i + 1) for i, x in enumerate(flows)) + tv / 1.10 ** 3
    assert by_id["G08"]["expected"]["enterprise_value"] == pytest.approx(ev)
    assert by_id["G15"]["expected"]["net_pnl"] == pytest.approx(100 * (101.2 - 100.1) - 2)
    assert by_id["G16"]["expected"]["expectancy"] == pytest.approx(0.55 * 0.015 - 0.45 * 0.02 - 0.0015)
    assert by_id["G23"]["expected"]["brier"] == pytest.approx(((0.8 - 1) ** 2 + (0.2 - 0) ** 2) / 2)
