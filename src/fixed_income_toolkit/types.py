"""Domain models for fixed-income analytics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class DayCount(str, Enum):
    THIRTY_360 = "30_360"
    ACT_360 = "act_360"
    ACT_ACT = "act_act"


@dataclass(frozen=True)
class BondSpec:
    id: str
    face: float
    coupon: float
    maturity: date
    settlement: date
    frequency: int = 2
    day_count: DayCount = DayCount.ACT_ACT
    position: float = 1.0


@dataclass(frozen=True)
class TreasuryInstrument:
    tenor_years: float
    instrument_type: str
    coupon: float
    market_yield: float


@dataclass(frozen=True)
class CurvePoint:
    tenor_years: float
    zero_rate: float
    discount_factor: float


@dataclass(frozen=True)
class ForwardPoint:
    start_tenor: float
    end_tenor: float
    forward_rate: float


@dataclass(frozen=True)
class BondAnalytics:
    clean_price: float
    dirty_price: float
    accrued_interest: float
    ytm: float
    macaulay_duration: float
    modified_duration: float
    convexity: float
    dv01: float


@dataclass(frozen=True)
class RiskRow:
    instrument_id: str
    dv01: float
    krd_2y: float
    krd_5y: float
    krd_10y: float
    krd_30y: float


@dataclass(frozen=True)
class PortfolioRiskSummary:
    total_dv01: float
    total_krd_2y: float
    total_krd_5y: float
    total_krd_10y: float
    total_krd_30y: float
