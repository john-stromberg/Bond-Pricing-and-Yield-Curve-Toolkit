from fixed_income_toolkit.curve import bootstrap_spot_curve, derive_forward_curve, interpolate_discount_factor
from fixed_income_toolkit.types import TreasuryInstrument


def test_bootstrap_and_forward_curve_lengths() -> None:
    instruments = [
        TreasuryInstrument(0.5, "bill", 0.0, 0.04),
        TreasuryInstrument(1.0, "note", 0.03, 0.041),
        TreasuryInstrument(2.0, "note", 0.035, 0.039),
        TreasuryInstrument(5.0, "bond", 0.04, 0.04),
    ]
    spot = bootstrap_spot_curve(instruments)
    forward = derive_forward_curve(spot)
    assert len(spot) == 4
    assert len(forward) == 3


def test_interpolate_discount_factor_returns_valid_value() -> None:
    instruments = [
        TreasuryInstrument(1.0, "note", 0.03, 0.04),
        TreasuryInstrument(5.0, "bond", 0.04, 0.042),
    ]
    spot = bootstrap_spot_curve(instruments)
    df = interpolate_discount_factor(spot, 3.0)
    assert 0.0 < df < 1.0
