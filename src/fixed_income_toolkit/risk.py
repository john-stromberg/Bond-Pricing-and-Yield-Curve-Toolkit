"""Portfolio risk analytics."""

from __future__ import annotations

from datetime import date

from .curve import interpolate_discount_factor
from .pricing import analytics_from_yield
from .types import BondSpec, CurvePoint, PortfolioRiskSummary, RiskRow


DEFAULT_KRD_BUCKETS = [2.0, 5.0, 10.0, 30.0]


def _years_to_maturity(settlement: date, maturity: date) -> float:
    return max((maturity - settlement).days / 365.25, 1e-6)


def _yield_from_curve(spot_curve: list[CurvePoint], tenor: float) -> float:
    discount_factor = interpolate_discount_factor(spot_curve, tenor)
    return discount_factor ** (-1.0 / tenor) - 1.0


def _nearest_bucket(tenor: float, buckets: list[float]) -> float:
    return min(buckets, key=lambda b: abs(tenor - b))


def shift_spot_curve_parallel(spot_curve: list[CurvePoint], shift_bps: float) -> list[CurvePoint]:
    shift = shift_bps / 10000.0
    shifted: list[CurvePoint] = []
    for point in spot_curve:
        zero_rate = max(0.0, point.zero_rate + shift)
        frequency = 2
        discount_factor = (1.0 + zero_rate / frequency) ** (-frequency * point.tenor_years)
        shifted.append(
            CurvePoint(
                tenor_years=point.tenor_years,
                zero_rate=float(zero_rate),
                discount_factor=float(discount_factor),
            )
        )
    return shifted


def risk_for_bond(spec: BondSpec, spot_curve: list[CurvePoint], buckets: list[float] | None = None) -> RiskRow:
    selected_buckets = buckets or DEFAULT_KRD_BUCKETS
    tenor = _years_to_maturity(spec.settlement, spec.maturity)
    ytm = _yield_from_curve(spot_curve, tenor)
    analytics = analytics_from_yield(spec, ytm)
    scaled_dv01 = analytics.dv01 * spec.position

    bucket = _nearest_bucket(tenor, selected_buckets)
    krd_map = {2.0: 0.0, 5.0: 0.0, 10.0: 0.0, 30.0: 0.0}
    if bucket in krd_map:
        krd_map[bucket] = scaled_dv01

    return RiskRow(
        instrument_id=spec.id,
        dv01=float(scaled_dv01),
        krd_2y=float(krd_map[2.0]),
        krd_5y=float(krd_map[5.0]),
        krd_10y=float(krd_map[10.0]),
        krd_30y=float(krd_map[30.0]),
    )


def portfolio_risk_report(
    bonds: list[BondSpec],
    spot_curve: list[CurvePoint],
    buckets: list[float] | None = None,
) -> tuple[list[RiskRow], PortfolioRiskSummary]:
    rows = [risk_for_bond(spec, spot_curve, buckets=buckets) for spec in bonds]

    summary = PortfolioRiskSummary(
        total_dv01=float(sum(r.dv01 for r in rows)),
        total_krd_2y=float(sum(r.krd_2y for r in rows)),
        total_krd_5y=float(sum(r.krd_5y for r in rows)),
        total_krd_10y=float(sum(r.krd_10y for r in rows)),
        total_krd_30y=float(sum(r.krd_30y for r in rows)),
    )
    return rows, summary


def scenario_risk_report(
    bonds: list[BondSpec],
    base_curve: list[CurvePoint],
    scenario_shifts_bps: dict[str, float],
) -> list[dict[str, float | str]]:
    results: list[dict[str, float | str]] = []
    for scenario_name, shift_bps in scenario_shifts_bps.items():
        shifted_curve = shift_spot_curve_parallel(base_curve, shift_bps)
        _, summary = portfolio_risk_report(bonds, shifted_curve)
        results.append(
            {
                "scenario": scenario_name,
                "curve_shift_bps": float(shift_bps),
                "total_dv01": float(summary.total_dv01),
                "krd_2y": float(summary.total_krd_2y),
                "krd_5y": float(summary.total_krd_5y),
                "krd_10y": float(summary.total_krd_10y),
                "krd_30y": float(summary.total_krd_30y),
            }
        )
    return results
