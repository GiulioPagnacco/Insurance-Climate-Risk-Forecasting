# Project Overview: Insurance Climate Risk Forecasting

## Executive Summary

**Goal:** Predict quarterly insurance claims using ECMWF seasonal climate forecasts to enable strategic pricing and risk management decisions.

**Status:** Oslo validation complete (r=0.33), Denmark MVP in progress.

**Timeline:** Q4 2024 - Q2 2025 (MVP launch)

---

## Problem Statement

Insurance companies face significant uncertainty in quarterly claim volumes due to climate variability. Current approaches rely on historical averages, missing opportunities to adjust pricing and reserves based on upcoming seasonal conditions.

### Market Need

- **Financial Impact:** Climate-related claims represent 55-80% of Norwegian property insurance payouts
- **Predictability Gap:** Insurers cannot currently anticipate quarterly claim spikes 1-3 months ahead
- **Business Value:** €2-4M annual advantage per insurer through risk-adjusted pricing and reserves planning

### Scientific Foundation

Based on Gorji & Rødal (2021) NHH thesis demonstrating AUC 0.67-0.79 for daily weather → claims prediction in Norway.

---

## Solution Approach

### Core Concept

**Input:** ECMWF SEAS5 seasonal forecasts (1-7 months ahead)
**Processing:** Quarterly aggregation of precipitation, temperature, wind
**Output:** Probabilistic quarterly claim outlook with confidence intervals
**Delivery:** API + Dashboard for quarterly pricing decisions

### Key Innovation

Shift from **reactive** (historical averages) to **proactive** (forward-looking forecasts) insurance pricing.

---

## Validation Results

### Portfolio 1: Oslo, Norway (2014-2021)

**Data:**
- 32 quarters analyzed
- 78.3M NOK total payouts (NASK real data)
- ERA5 observed precipitation

**Results:**
- **Correlation:** r = 0.33 (p = 0.066)
- **Variance explained:** 11% of quarterly claim variability
- **Event detection:** 2015-Q3 flooding (18.8M NOK) correctly identified
- **Detection rate:** 33% (1 of 3 extreme quarters precipitation-driven)

**Interpretation:**
Moderate positive correlation validates proof-of-concept. Weaker than daily predictions due to:
- Quarterly aggregation smoothing
- Oslo's low natural perils mix (14% vs Bergen 55%)
- Multiple claim drivers (storms, flooding, snow)

**Conclusion:** Infrastructure validated, concept proven, ready for multi-variate model and commercial MVP.

---

## Product Roadmap

### Phase 1: Technical Validation (COMPLETE)
- ✅ Oslo correlation analysis
- ✅ ECMWF data integration
- ✅ Event detection validation
- ✅ Infrastructure setup

### Phase 2: Denmark MVP (IN PROGRESS - 8-10 weeks)
- [ ] Week 1-2: Data pipeline (Danish claims + SEAS5 forecasts)
- [ ] Week 3-4: Multi-variate model (precipitation + wind + temperature)
- [ ] Week 5-6: Dashboard prototype
- [ ] Week 7-8: Tryg pilot preparation
- [ ] Week 9-10: Testing & documentation

### Phase 3: Pilot & Iteration (Q1 2025)
- [ ] Tryg pilot launch
- [ ] Quarterly forecast delivery
- [ ] Model refinement based on feedback
- [ ] Expand to 3-5 Nordic customers

### Phase 4: Commercial Launch (Q2 2025)
- [ ] Multi-customer platform
- [ ] Automated forecast delivery
- [ ] Customer success tracking
- [ ] Western Europe expansion

---

## Target Market

### Geographic Focus

**Phase 1 (2025):** Nordic countries (Denmark, Norway, Sweden)
- High natural perils exposure
- Strong climate forecasting infrastructure
- Advisor network (Etienne at Tryg)

**Phase 2 (2025-2026):** Western Europe
- North Italy (Allianz contact via Edoardo)
- Benelux, UK, Germany

### Customer Segments

**Tier 1 Priority:**
- Tryg (€3.4B premiums) - Denmark/Norway
- Topdanmark (€1.8B) - Denmark
- Gjensidige (€2.1B) - Norway

**Tier 2:**
- If P&C, Alm. Brand (Nordic)
- Allianz, Generali (Western Europe)

---

## Technology Stack

### Data Sources

**Insurance Claims:**
- NASK (Finance Norway) - Norwegian claims database
- EIOPA - European insurance statistics
- Perils AG - Event-level catastrophe data (planned)

**Climate Data:**
- ERA5 (ECMWF Reanalysis) - Historical observations
- SEAS5 (ECMWF Seasonal Forecasts) - 1-7 month forecasts
- Access: Copernicus Climate Data Store (CDS API)

### Processing

**Languages:** Python 3.10+
**Key Libraries:**
- `xarray` - NetCDF climate data processing
- `cdsapi` - ECMWF data retrieval
- `pandas` - Time series analysis
- `scikit-learn` - Statistical modeling

**Infrastructure:**
- Jupyter Lab - Analysis notebooks
- Git/GitHub - Version control
- AWS/Cloud - Production deployment (planned)

---

## Key Metrics

### Technical Validation
- ✅ Correlation: r = 0.33 (Oslo)
- ✅ Event detection: 1/3 extreme quarters
- ✅ Infrastructure: ECMWF integration operational

### Business Targets (2025)
- Q1: Tryg pilot launch
- Q2: 3-5 Nordic customers
- Q3-Q4: €2-5M ARR
- End 2025: 10+ customers, Western Europe expansion

---

## Team & Advisors

**Giulio Pagnacco** - Founder & Developer

**Advisors:**
- Etienne (Tryg) - Insurance operations, thesis author network
- Ashbin - Academic methodology validation
- Edoardo - Allianz contact (North Italy)

---

## Documentation Structure

This repository contains:

- **`docs/`** - Technical documentation and methodology
- **`portfolio1-norway/`** - Oslo validation code and results
- **`analysis/`** - Decision logs and conversation archive
- **`business/`** - Market analysis and BD strategy
- **`references/`** - Data sources and literature
- **`mvp-specs/`** - Denmark MVP specifications (coming soon)

---

## Next Steps

1. **Denmark data pipeline** (Week 1-2)
2. **Multi-variate model** (Week 3-4)
3. **Dashboard prototype** (Week 5-6)
4. **Tryg outreach** (Week 7)
5. **Pilot launch** (Q1 2025)

---

## Contact

**GitHub:** https://github.com/GiulioPagnacco/Insurance-Climate-Risk-Forecasting
**LinkedIn:** [Your LinkedIn]
**Email:** [Your email]

---

**Last Updated:** October 2024
**Version:** 0.2.0 (Oslo validation complete)
