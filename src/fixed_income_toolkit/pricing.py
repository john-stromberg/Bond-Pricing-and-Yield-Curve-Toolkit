"""Bond pricing analytics."""

from __future__ import annotations

from datetime import date

try:
    import QuantLib as ql
except ImportError:  # pragma: no cover
    ql = None

from .types import BondAnalytics, BondSpec, DayCount


def _years_to_maturity(spec: BondSpec) -> float:
    return max((spec.maturity - spec.settlement).days / 365.25, 1e-6)


def _manual_analytics_from_yield(spec: BondSpec, ytm: float) -> BondAnalytics:
    years = _years_to_maturity(spec)
    n_periods = max(1, int(round(years * spec.frequency)))
    coupon_cash = spec.face * spec.coupon / spec.frequency
    period_rate = ytm / spec.frequency

    discount = lambda i: (1.0 + period_rate) ** (-i)
    cashflows = [coupon_cash] * n_periods
    cashflows[-1] += spec.face

    pv_cashflows = [cf * discount(i + 1) for i, cf in enumerate(cashflows)]
    dirty_price = float(sum(pv_cashflows))
    clean_price = dirty_price
    accrued_interest = 0.0

    times = [(i + 1) / spec.frequency for i in range(n_periods)]
    macaulay_duration = sum(t * pv for t, pv in zip(times, pv_cashflows)) / dirty_price
    modified_duration = macaulay_duration / (1.0 + period_rate)
    convexity = (
        sum(pv * t * (t + 1.0 / spec.frequency) for t, pv in zip(times, pv_cashflows))
        / (dirty_price * (1.0 + period_rate) ** 2)
    )
    dv01 = abs(modified_duration * dirty_price * 0.0001)

    return BondAnalytics(
        clean_price=clean_price,
        dirty_price=dirty_price,
        accrued_interest=accrued_interest,
        ytm=float(ytm),
        macaulay_duration=float(macaulay_duration),
        modified_duration=float(modified_duration),
        convexity=float(convexity),
        dv01=float(dv01),
    )


def _manual_yield_from_clean_price(spec: BondSpec, clean_price: float) -> float:
    low = 0.0
    high = 1.0
    for _ in range(100):
        mid = 0.5 * (low + high)
        price_mid = _manual_analytics_from_yield(spec, mid).clean_price
        if price_mid > clean_price:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def _to_ql_date(value: date) -> "ql.Date":
    return ql.Date(value.day, value.month, value.year)


def _frequency_to_ql(frequency: int) -> "ql.Frequency":
    mapping = {1: ql.Annual, 2: ql.Semiannual, 4: ql.Quarterly}
    if frequency not in mapping:
        raise ValueError("Frequency must be one of 1, 2, or 4")
    return mapping[frequency]


def _day_count_to_ql(day_count: DayCount) -> "ql.DayCounter":
    if day_count == DayCount.THIRTY_360:
        return ql.Thirty360(ql.Thirty360.BondBasis)
    if day_count == DayCount.ACT_360:
        return ql.Actual360()
    return ql.ActualActual(ql.ActualActual.ISDA)


def _build_bond(spec: BondSpec) -> tuple["ql.FixedRateBond", "ql.Date", "ql.DayCounter", "ql.Frequency"]:
    settlement_date = _to_ql_date(spec.settlement)
    maturity_date = _to_ql_date(spec.maturity)
    day_counter = _day_count_to_ql(spec.day_count)
    frequency = _frequency_to_ql(spec.frequency)
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    period_months = int(12 / spec.frequency)
    issue_date = settlement_date - ql.Period(period_months, ql.Months)
    schedule = ql.Schedule(
        issue_date,
        maturity_date,
        ql.Period(frequency),
        calendar,
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Backward,
        False,
    )
    bond = ql.FixedRateBond(0, spec.face, schedule, [spec.coupon], day_counter)
    return bond, settlement_date, day_counter, frequency


def analytics_from_yield(spec: BondSpec, ytm: float) -> BondAnalytics:
    if ql is None:
        return _manual_analytics_from_yield(spec, ytm)

    bond, settlement_date, day_counter, frequency = _build_bond(spec)
    compounding = ql.Compounded

    clean_price = ql.BondFunctions.cleanPrice(
        bond, ytm, day_counter, compounding, frequency, settlement_date
    )
    accrued_interest = bond.accruedAmount(settlement_date)
    dirty_price = clean_price + accrued_interest

    macaulay_duration = ql.BondFunctions.duration(
        bond, ytm, day_counter, compounding, frequency, ql.Duration.Macaulay, settlement_date
    )
    modified_duration = ql.BondFunctions.duration(
        bond, ytm, day_counter, compounding, frequency, ql.Duration.Modified, settlement_date
    )
    convexity = ql.BondFunctions.convexity(
        bond, ytm, day_counter, compounding, frequency, settlement_date
    )

    dv01 = abs(modified_duration * dirty_price * 0.0001)
    return BondAnalytics(
        clean_price=float(clean_price),
        dirty_price=float(dirty_price),
        accrued_interest=float(accrued_interest),
        ytm=float(ytm),
        macaulay_duration=float(macaulay_duration),
        modified_duration=float(modified_duration),
        convexity=float(convexity),
        dv01=float(dv01),
    )


def yield_from_clean_price(spec: BondSpec, clean_price: float) -> float:
    if ql is None:
        return _manual_yield_from_clean_price(spec, clean_price)

    bond, settlement_date, day_counter, frequency = _build_bond(spec)
    compounding = ql.Compounded
    return float(
        ql.BondFunctions.bondYield(
            bond, clean_price, day_counter, compounding, frequency, settlement_date
        )
    )


def price_bond(spec: BondSpec, ytm: float | None = None, clean_price: float | None = None) -> BondAnalytics:
    if ytm is None and clean_price is None:
        raise ValueError("Provide either ytm or clean_price")

    if ytm is None:
        ytm = yield_from_clean_price(spec, float(clean_price))

    return analytics_from_yield(spec, float(ytm))
