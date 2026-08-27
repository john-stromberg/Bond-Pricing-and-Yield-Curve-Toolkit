# Repo #1 Learning Checklist (Finance + Programming)

## Progress Dashboard
- [ ] Week 1 complete
- [ ] Week 2 complete
- [ ] Week 3 complete
- [ ] Week 4 complete
- [ ] Final reflection complete

---

## Week 1 - Bond Valuation + Risk Basics

### Module 1: Bond Pricing Basics
- [ ] Read finance concepts: clean/dirty price, accrued interest, YTM
- [ ] Review `src/fixed_income_toolkit/pricing.py`
- [ ] Run CLI pricing command at least 2 times with different inputs
- [ ] Write 5-bullet finance summary
- [ ] Write 5-bullet code summary
- [ ] Commit changes/notes

### Module 2: Single-Bond Risk Measures
- [ ] Study Macaulay duration, modified duration, convexity, DV01
- [ ] Trace where DV01 is calculated in code
- [ ] Compare DV01 across short/intermediate/long maturity examples
- [ ] Document one practical interpretation ("what higher DV01 means")
- [ ] Add or update one test in `tests/test_pricing.py`
- [ ] Commit changes/notes

### Week 1 Deliverables
- [ ] 1 finance note file created
- [ ] 1 code note file created
- [ ] 1 test added/updated
- [ ] CLI output screenshot saved

---

## Week 2 - Spot + Forward Curves

### Module 3: Spot Curve Construction
- [ ] Study bootstrap intuition and discount factors
- [ ] Review `src/fixed_income_toolkit/curve.py` spot logic
- [ ] Run curve build command with sample data
- [ ] Modify one yield in `data/sample/treasuries.csv`
- [ ] Re-run and compare output differences
- [ ] Commit changes/notes

### Module 4: Forward Curve Interpretation
- [ ] Study implied forward rates between tenors
- [ ] Trace forward-rate function in code
- [ ] Explain one forward segment (example: 5Y to 10Y)
- [ ] Add one chart or table in notebook
- [ ] Add or update one test in `tests/test_curve.py`
- [ ] Commit changes/notes

### Week 2 Deliverables
- [ ] Spot curve output file saved
- [ ] Forward curve output file saved
- [ ] 1 notebook updated with interpretation
- [ ] 1 test added/updated

---

## Week 3 - Portfolio Risk + Data Handling

### Module 5: Portfolio DV01 + KRD
- [ ] Study portfolio DV01 aggregation and key-rate duration buckets
- [ ] Review `src/fixed_income_toolkit/risk.py`
- [ ] Change portfolio weights in `data/sample/portfolio.csv`
- [ ] Run `risk-report` and interpret bucket changes
- [ ] Write a short "risk story" from results
- [ ] Commit changes/notes

### Module 6: Data Engineering Layer
- [ ] Review CSV schema expectations in `src/fixed_income_toolkit/io.py`
- [ ] Intentionally break one column to observe validation failure
- [ ] Restore valid schema and rerun successfully
- [ ] Document one data-quality lesson learned
- [ ] Add or update one test in `tests/test_risk.py` or `tests/test_cli.py`
- [ ] Commit changes/notes

### Week 3 Deliverables
- [ ] Risk report output saved
- [ ] 1 finance interpretation note saved
- [ ] 1 data-quality note saved
- [ ] 1 test added/updated

---

## Week 4 - Automation + Validation + Polish

### Module 7: End-to-End CLI Workflow
- [ ] Run full pipeline: price -> build-curve -> risk-report
- [ ] Record command sequence in personal notes
- [ ] Add one quality-of-life CLI improvement (optional)
- [ ] Commit changes/notes

### Module 8: Testing + Trust
- [ ] Run full tests locally
- [ ] Review why each test exists
- [ ] Add one edge-case test (near maturity, low coupon, etc.)
- [ ] Confirm all tests pass
- [ ] Commit changes/notes

### Week 4 Deliverables
- [ ] Test run evidence saved
- [ ] 1 edge-case test added
- [ ] README personal annotations complete
- [ ] Final weekly summary written

---

## Final Reflection (End of Month)

### Finance Mastery Check (1-5)
- [ ] I can explain bond pricing clearly
- [ ] I can explain duration/convexity/DV01
- [ ] I can explain spot vs forward curves
- [ ] I can explain KRD and curve-shape risk

### Programming Mastery Check (1-5)
- [ ] I can trace data flow across modules
- [ ] I can modify CLI behavior safely
- [ ] I can add meaningful tests
- [ ] I can debug failures quickly

### Capstone Actions
- [ ] Write 1-page "What I learned" summary
- [ ] List 3 improvements for Repo #1
- [ ] Choose next repo start date (Repo #2)

---

## Session Log Template (copy per study session)

**Date:**
**Module:**
**Finance concept learned (3-5 bullets):**
-
-
-

**Programming concept learned (3-5 bullets):**
-
-
-

**Command(s) run:**
-

**Files touched:**
-

**Test(s) run + result:**
-

**Commit hash/message:**
-

**Questions to revisit:**
-
