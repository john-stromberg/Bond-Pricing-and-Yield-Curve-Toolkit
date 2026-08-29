# Bond Pricing & Yield Curve Toolkit

Fixed-income analytics toolkit for bond pricing, Treasury spot/forward curve construction, and portfolio risk metrics (DV01 + key-rate duration).

## What you can do with this toolkit

- Price a bond from yield or infer yield from clean price
- Compute clean/dirty price, accrued, duration, convexity, DV01
- Build a simplified Treasury spot curve and derived forward curve
- Run portfolio DV01 and KRD (2Y/5Y/10Y/30Y) reports from CSV inputs
- Use notebooks for full end-to-end walkthroughs

## Project structure

- `src/fixed_income_toolkit/pricing.py` bond pricing and risk measures
- `src/fixed_income_toolkit/curve.py` spot and forward curve logic
- `src/fixed_income_toolkit/risk.py` portfolio DV01 and KRD aggregation
- `src/fixed_income_toolkit/io.py` CSV input/output helpers
- `cli/main.py` command-line interface (`fitool`)
- `data/sample/` ready-to-run datasets
- `notebooks/` guided examples

## Setup

1. Install dependencies:
   - `poetry install`
2. Optional: verify environment:
   - `poetry run pytest`

## CLI usage guide

### 1) Price a single bond

```bash
poetry run fitool price-bond --coupon 0.045 --maturity 2032-06-30 --settlement 2026-09-15 --freq 2 --ytm 0.041
```

Use when you want pricing/risk for one instrument.

Key inputs:
- `--coupon` annual coupon rate (decimal)
- `--maturity` maturity date `YYYY-MM-DD`
- `--settlement` settlement date `YYYY-MM-DD`
- `--freq` coupon frequency (`1|2|4`)
- one of:
  - `--ytm` to price from yield
  - `--clean-price` to solve implied yield

### 2) Build spot and forward curves

```bash
poetry run fitool build-curve --input data/sample/treasuries.csv --out-spot outputs/spot_curve.csv --out-fwd outputs/forward_curve.csv
```

Use when you need discount/forward inputs for downstream risk analysis.

Outputs:
- `spot_curve.csv`: tenor, zero rate, discount factor
- `forward_curve.csv`: start tenor, end tenor, forward rate

### 3) Run portfolio risk report

```bash
poetry run fitool risk-report --portfolio data/sample/portfolio.csv --curve outputs/spot_curve.csv --settlement 2026-09-15 --output outputs/risk_report.csv
```

Use when you want instrument-level and aggregated portfolio risk under the curve.

Output includes:
- `dv01` per instrument
- `krd_2y`, `krd_5y`, `krd_10y`, `krd_30y` bucket attribution

### 4) Run parallel-shift scenario risk (notebook-aligned)

```bash
poetry run fitool scenario-risk --portfolio data/sample/portfolio.csv --curve outputs/spot_curve.csv --settlement 2026-09-15 --output outputs/scenario_risk_report.csv --shock-bps 25
```

Use when you want the same base/up/down parallel-shift comparison used in Notebook 03.

Output includes:
- `scenario` (`base`, `up_shock`, `down_shock`)
- `curve_shift_bps`
- `total_dv01`, `krd_2y`, `krd_5y`, `krd_10y`, `krd_30y`

## Typical workflow (recommended)

1. Build curve from Treasury data
2. Run portfolio risk report on that curve
3. Use notebook 03 to compare shifted-curve scenarios

In commands:

```bash
poetry run fitool build-curve --input data/sample/treasuries.csv --out-spot outputs/spot_curve.csv --out-fwd outputs/forward_curve.csv
poetry run fitool risk-report --portfolio data/sample/portfolio.csv --curve outputs/spot_curve.csv --settlement 2026-09-15 --output outputs/risk_report.csv
poetry run fitool scenario-risk --portfolio data/sample/portfolio.csv --curve outputs/spot_curve.csv --settlement 2026-09-15 --output outputs/scenario_risk_report.csv --shock-bps 25
```

## Notebook guide

- `notebooks/01_pricing_basics.ipynb`
  - price-yield sensitivity, DV01 behavior, implied yield from clean price
- `notebooks/02_curve_bootstrap_forward.ipynb`
  - load Treasury data, build spot/forward curves, export curve files
- `notebooks/03_dv01_krd_scenarios.ipynb`
  - portfolio DV01/KRD and scenario comparison under curve shifts

## Analytical use cases

- **Valuation sensitivity:** explain how rate regimes affect bond pricing and risk metrics.
- **Term-structure diagnostics:** compare spot and forward views to discuss curve shape and implied expectations.
- **Portfolio risk decomposition:** identify DV01/KRD concentration and scenario sensitivity by tenor bucket.

## Decision-ready outputs

- `outputs/spot_curve.csv` and `outputs/forward_curve.csv` for downstream risk workflows.
- `outputs/risk_report.csv` for instrument-level DV01/KRD review.
- `outputs/scenario_risk_report.csv` for base/up/down shift comparison.
- Notebook scenario tables/charts for quick what-if analysis and hedge discussion.

## Input schemas

### `data/sample/treasuries.csv`
- `tenor_years`
- `instrument_type` (`bill`, `note`, `bond`)
- `coupon`
- `market_yield`

### `data/sample/portfolio.csv`
- `id`
- `face`
- `coupon`
- `maturity` (`YYYY-MM-DD`)
- `freq`
- `position`

## Personal learning

- [Learning Checklist](./LEARNING_CHECKLIST.md)

## Notes

- Curve construction is intentionally simplified for transparency.
- KRD currently maps each bond to the nearest bucket.
- QuantLib is used when available; fallback analytics are included.
