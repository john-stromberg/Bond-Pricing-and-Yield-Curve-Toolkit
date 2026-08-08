from datetime import date

from fixed_income_toolkit.pricing import price_bond
from fixed_income_toolkit.types import BondSpec


def test_price_bond_from_yield_returns_metrics() -> None:
    spec = BondSpec(
        id="T1",
        face=100.0,
        coupon=0.045,
        maturity=date(2032, 6, 30),
        settlement=date(2026, 9, 15),
        frequency=2,
    )
    analytics = price_bond(spec, ytm=0.041)
    assert analytics.clean_price > 90.0
    assert analytics.dirty_price >= analytics.clean_price
    assert analytics.modified_duration > 0.0
    assert analytics.dv01 > 0.0


def test_price_bond_from_clean_price_solves_yield() -> None:
    spec = BondSpec(
        id="T2",
        face=100.0,
        coupon=0.04,
        maturity=date(2030, 9, 15),
        settlement=date(2026, 9, 15),
        frequency=2,
    )
    analytics = price_bond(spec, clean_price=99.0)
    assert 0.0 < analytics.ytm < 0.2
