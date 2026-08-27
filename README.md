# Bond Pricing & Yield Curve Toolkit

Fixed-income analytics toolkit: bond pricing, Treasury spot/forward curve construction, DV01, and key-rate duration buckets.

## Why this project matters

This repository demonstrates practical fixed-income skills used in rates and credit workflows: valuation, term-structure construction, and portfolio risk decomposition.

## MVP Features

- Bond pricing via yield or clean price input
- Clean price, dirty price, accrued interest, YTM, duration, convexity, and DV01
- Treasury spot curve build from market yield inputs
- Forward curve derivation across tenor segments
- Portfolio DV01 and key-rate duration (2Y/5Y/10Y/30Y) report
- CLI + sample datasets + starter notebooks + tests + CI

## Tech Stack

- Python 3.11
- QuantLib (with fallback to pure Python analytics)
- pandas, numpy, scipy
- Typer + Rich (CLI)
- pytest, ruff, black
- GitHub Actions CI

## Repository Structure

- `src/fixed_income_toolkit/` core analytics modules
- `cli/main.py` command-line entrypoint
- `data/sample/` sample treasury and portfolio inputs
- `notebooks/` walkthrough notebooks
- `tests/` pricing, curve, risk, and CLI tests

## Personal Learning

- [Learning Checklist](./LEARNING_CHECKLIST.md)

## Quickstart

1. Install dependencies
   - `poetry install`

2. Price a bond
   - `poetry run fitool price-bond --coupon 0.045 --maturity 2032-06-30 --settlement 2026-09-15 --freq 2 --ytm 0.041`

3. Build spot and forward curves
   - `poetry run fitool build-curve --input data/sample/treasuries.csv --out-spot outputs/spot_curve.csv --out-fwd outputs/forward_curve.csv`

4. Generate portfolio risk report
   - `poetry run fitool risk-report --portfolio data/sample/portfolio.csv --curve outputs/spot_curve.csv --settlement 2026-09-15 --output outputs/risk_report.csv`

## Sample Input Schemas

### Treasuries (`data/sample/treasuries.csv`)
- `tenor_years`
- `instrument_type` (`bill`, `note`, `bond`)
- `coupon`
- `market_yield`

### Portfolio (`data/sample/portfolio.csv`)
- `id`
- `face`
- `coupon`
- `maturity` (YYYY-MM-DD)
- `freq`
- `position`

## Validation

- Run tests: `poetry run pytest`
- Lint checks: `poetry run ruff check .` and `poetry run black --check .`

## Notes and assumptions

- Curve construction is simplified for portfolio demo clarity.
- KRD uses nearest-bucket allocation for transparent exposure reporting.
- QuantLib is preferred when available; fallback logic supports environments without it.
