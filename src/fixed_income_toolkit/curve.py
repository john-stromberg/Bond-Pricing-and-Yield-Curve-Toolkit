"""Spot and forward curve analytics."""

from __future__ import annotations

import math

from .types import CurvePoint, ForwardPoint, TreasuryInstrument


def bootstrap_spot_curve(instruments: list[TreasuryInstrument]) -> list[CurvePoint]:
    """Build a simplified Treasury spot curve from market yields by tenor."""
    if not instruments:
        return []

    sorted_instruments = sorted(instruments, key=lambda x: x.tenor_years)
    points: list[CurvePoint] = []
    for instrument in sorted_instruments:
        tenor = float(instrument.tenor_years)
        if tenor <= 0:
            raise ValueError("tenor_years must be positive")

        zero_rate = float(instrument.market_yield)
        frequency = 1 if instrument.instrument_type.lower() == "bill" else 2
        discount_factor = (1.0 + zero_rate / frequency) ** (-frequency * tenor)
        points.append(
            CurvePoint(
                tenor_years=tenor,
                zero_rate=zero_rate,
                discount_factor=float(discount_factor),
            )
        )
    return points


def derive_forward_curve(spot_curve: list[CurvePoint]) -> list[ForwardPoint]:
    if len(spot_curve) < 2:
        return []

    points = sorted(spot_curve, key=lambda x: x.tenor_years)
    forwards: list[ForwardPoint] = []

    for idx in range(len(points) - 1):
        t1 = points[idx].tenor_years
        t2 = points[idx + 1].tenor_years
        df1 = points[idx].discount_factor
        df2 = points[idx + 1].discount_factor
        if t2 <= t1:
            continue
        forward = (df1 / df2) ** (1.0 / (t2 - t1)) - 1.0
        forwards.append(
            ForwardPoint(start_tenor=t1, end_tenor=t2, forward_rate=float(forward))
        )

    return forwards


def interpolate_discount_factor(spot_curve: list[CurvePoint], tenor: float) -> float:
    if tenor <= 0:
        raise ValueError("tenor must be positive")
    points = sorted(spot_curve, key=lambda x: x.tenor_years)
    if not points:
        raise ValueError("spot_curve must not be empty")

    if tenor <= points[0].tenor_years:
        return points[0].discount_factor
    if tenor >= points[-1].tenor_years:
        return points[-1].discount_factor

    for left, right in zip(points, points[1:]):
        if left.tenor_years <= tenor <= right.tenor_years:
            w = (tenor - left.tenor_years) / (right.tenor_years - left.tenor_years)
            log_df = (1.0 - w) * math.log(left.discount_factor) + w * math.log(right.discount_factor)
            return float(math.exp(log_df))

    return points[-1].discount_factor
