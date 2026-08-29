from datetime import date

from fixed_income_toolkit.curve import bootstrap_spot_curve
from fixed_income_toolkit.risk import portfolio_risk_report, scenario_risk_report
from fixed_income_toolkit.types import BondSpec, TreasuryInstrument


def test_portfolio_risk_report_aggregates() -> None:
    instruments = [
        TreasuryInstrument(2.0, "note", 0.03, 0.04),
        TreasuryInstrument(5.0, "bond", 0.04, 0.041),
        TreasuryInstrument(10.0, "bond", 0.045, 0.043),
        TreasuryInstrument(30.0, "bond", 0.047, 0.044),
    ]
    spot_curve = bootstrap_spot_curve(instruments)
    bonds = [
        BondSpec("B1", 100.0, 0.04, date(2028, 9, 15), date(2026, 9, 15), 2),
        BondSpec("B2", 100.0, 0.0425, date(2031, 9, 15), date(2026, 9, 15), 2),
    ]

    rows, summary = portfolio_risk_report(bonds, spot_curve)
    assert len(rows) == 2
    assert summary.total_dv01 > 0.0
    assert summary.total_krd_2y + summary.total_krd_5y + summary.total_krd_10y + summary.total_krd_30y > 0.0


def test_scenario_risk_report_matches_notebook_pattern() -> None:
    instruments = [
        TreasuryInstrument(2.0, "note", 0.03, 0.04),
        TreasuryInstrument(5.0, "bond", 0.04, 0.041),
        TreasuryInstrument(10.0, "bond", 0.045, 0.043),
        TreasuryInstrument(30.0, "bond", 0.047, 0.044),
    ]
    spot_curve = bootstrap_spot_curve(instruments)
    bonds = [
        BondSpec("B1", 100.0, 0.04, date(2028, 9, 15), date(2026, 9, 15), 2),
        BondSpec("B2", 100.0, 0.0425, date(2031, 9, 15), date(2026, 9, 15), 2),
    ]
    scenarios = {"base": 0.0, "up_25bp": 25.0, "down_25bp": -25.0}

    report = scenario_risk_report(bonds, spot_curve, scenarios)
    assert len(report) == 3
    assert [row["scenario"] for row in report] == ["base", "up_25bp", "down_25bp"]

    base = next(r for r in report if r["scenario"] == "base")
    up = next(r for r in report if r["scenario"] == "up_25bp")
    down = next(r for r in report if r["scenario"] == "down_25bp")
    assert down["total_dv01"] > base["total_dv01"] > up["total_dv01"]
