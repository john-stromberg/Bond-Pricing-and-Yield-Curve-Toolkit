"""CLI entrypoint."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

from fixed_income_toolkit.curve import bootstrap_spot_curve, derive_forward_curve
from fixed_income_toolkit.io import (
    read_bonds_csv,
    read_treasuries_csv,
    write_forward_curve_csv,
    write_spot_curve_csv,
)
from fixed_income_toolkit.pricing import price_bond
from fixed_income_toolkit.risk import portfolio_risk_report
from fixed_income_toolkit.types import BondSpec

app = typer.Typer(add_completion=False, help="Fixed income analytics toolkit CLI")
console = Console()


@app.command("price-bond")
def price_bond_command(
    face: float = typer.Option(100.0),
    coupon: float = typer.Option(..., help="Annual coupon rate, e.g., 0.045"),
    maturity: str = typer.Option(..., help="Maturity date YYYY-MM-DD"),
    settlement: str = typer.Option(..., help="Settlement date YYYY-MM-DD"),
    freq: int = typer.Option(2, help="Coupon frequency: 1, 2, or 4"),
    ytm: float | None = typer.Option(None),
    clean_price: float | None = typer.Option(None),
) -> None:
    spec = BondSpec(
        id="single",
        face=face,
        coupon=coupon,
        maturity=date.fromisoformat(maturity),
        settlement=date.fromisoformat(settlement),
        frequency=freq,
    )
    analytics = price_bond(spec, ytm=ytm, clean_price=clean_price)

    table = Table(title="Bond Analytics")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Clean Price", f"{analytics.clean_price:.6f}")
    table.add_row("Dirty Price", f"{analytics.dirty_price:.6f}")
    table.add_row("Accrued Interest", f"{analytics.accrued_interest:.6f}")
    table.add_row("Yield", f"{analytics.ytm:.6%}")
    table.add_row("Macaulay Duration", f"{analytics.macaulay_duration:.6f}")
    table.add_row("Modified Duration", f"{analytics.modified_duration:.6f}")
    table.add_row("Convexity", f"{analytics.convexity:.6f}")
    table.add_row("DV01", f"{analytics.dv01:.6f}")
    console.print(table)


@app.command("build-curve")
def build_curve_command(
    input: Path = typer.Option(..., exists=True, readable=True),
    out_spot: Path = typer.Option(...),
    out_fwd: Path = typer.Option(...),
) -> None:
    instruments = read_treasuries_csv(input)
    spot_curve = bootstrap_spot_curve(instruments)
    forward_curve = derive_forward_curve(spot_curve)
    write_spot_curve_csv(spot_curve, out_spot)
    write_forward_curve_csv(forward_curve, out_fwd)
    console.print(f"Wrote spot curve to {out_spot}")
    console.print(f"Wrote forward curve to {out_fwd}")


@app.command("risk-report")
def risk_report_command(
    portfolio: Path = typer.Option(..., exists=True, readable=True),
    curve: Path = typer.Option(..., exists=True, readable=True),
    settlement: str = typer.Option(..., help="Settlement date YYYY-MM-DD"),
    output: Path = typer.Option(...),
) -> None:
    spot_frame = pd.read_csv(curve)
    required = {"tenor_years", "zero_rate", "discount_factor"}
    if required - set(spot_frame.columns):
        raise typer.BadParameter("Curve file missing required columns")

    from fixed_income_toolkit.types import CurvePoint

    curve_points = [
        CurvePoint(
            tenor_years=float(row.tenor_years),
            zero_rate=float(row.zero_rate),
            discount_factor=float(row.discount_factor),
        )
        for row in spot_frame.itertuples(index=False)
    ]

    bonds = read_bonds_csv(portfolio, settlement=date.fromisoformat(settlement))
    rows, summary = portfolio_risk_report(bonds, curve_points)
    report_frame = pd.DataFrame(
        {
            "instrument_id": [r.instrument_id for r in rows],
            "dv01": [r.dv01 for r in rows],
            "krd_2y": [r.krd_2y for r in rows],
            "krd_5y": [r.krd_5y for r in rows],
            "krd_10y": [r.krd_10y for r in rows],
            "krd_30y": [r.krd_30y for r in rows],
        }
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    report_frame.to_csv(output, index=False)

    console.print(f"Wrote instrument risk report to {output}")
    console.print(
        f"Portfolio totals -> DV01: {summary.total_dv01:.6f}, "
        f"KRD(2Y): {summary.total_krd_2y:.6f}, KRD(5Y): {summary.total_krd_5y:.6f}, "
        f"KRD(10Y): {summary.total_krd_10y:.6f}, KRD(30Y): {summary.total_krd_30y:.6f}"
    )


if __name__ == "__main__":
    app()
