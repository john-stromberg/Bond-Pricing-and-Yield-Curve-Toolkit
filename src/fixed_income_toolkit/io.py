"""CSV I/O helpers for toolkit entities."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from .types import BondSpec, CurvePoint, ForwardPoint, TreasuryInstrument


def _parse_date(value: str) -> date:
    return date.fromisoformat(str(value))


def read_treasuries_csv(path: str | Path) -> list[TreasuryInstrument]:
    frame = pd.read_csv(path)
    required = {"tenor_years", "instrument_type", "coupon", "market_yield"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    instruments: list[TreasuryInstrument] = []
    for row in frame.itertuples(index=False):
        instruments.append(
            TreasuryInstrument(
                tenor_years=float(row.tenor_years),
                instrument_type=str(row.instrument_type),
                coupon=float(row.coupon),
                market_yield=float(row.market_yield),
            )
        )
    return instruments


def read_bonds_csv(path: str | Path, settlement: date) -> list[BondSpec]:
    frame = pd.read_csv(path)
    required = {"id", "face", "coupon", "maturity", "freq"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    bonds: list[BondSpec] = []
    for row in frame.itertuples(index=False):
        bonds.append(
            BondSpec(
                id=str(row.id),
                face=float(row.face),
                coupon=float(row.coupon),
                maturity=_parse_date(row.maturity),
                settlement=settlement,
                frequency=int(row.freq),
                position=float(getattr(row, "position", 1.0)),
            )
        )
    return bonds


def read_portfolio_csv(path: str | Path, settlement: date) -> list[BondSpec]:
    return read_bonds_csv(path, settlement=settlement)


def write_spot_curve_csv(points: list[CurvePoint], path: str | Path) -> None:
    frame = pd.DataFrame(
        {
            "tenor_years": [p.tenor_years for p in points],
            "zero_rate": [p.zero_rate for p in points],
            "discount_factor": [p.discount_factor for p in points],
        }
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def write_forward_curve_csv(points: list[ForwardPoint], path: str | Path) -> None:
    frame = pd.DataFrame(
        {
            "start_tenor": [p.start_tenor for p in points],
            "end_tenor": [p.end_tenor for p in points],
            "forward_rate": [p.forward_rate for p in points],
        }
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
