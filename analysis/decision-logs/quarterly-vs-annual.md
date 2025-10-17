# Decision: Quarterly vs. Annual Forecasting

## Context

Initial concept was 72-hour operational forecasting for insurance claims. Advisor (Etienne) suggested longer timeframe for strategic value.

## Analysis

| Timeframe | ECMWF Product | Lead Time | Uncertainty | Validation Speed | Business Value | Decision |
|-----------|---------------|-----------|-------------|------------------|----------------|----------|
| **72-hour** | IFS Deterministic | 3 days | ±10% | Days | Low (operational) | ❌ |
| **Weekly** | IFS Extended | 7-10 days | ±15% | Weeks | Low-Medium | ❌ |
| **Monthly** | SEAS5 | 1 month | ±20% | 1-2 months | Medium | ⚠️ |
| **Quarterly** | SEAS5 | 1-3 months | ±25% | 3 months | **High** | ✅ |
| **Seasonal** | SEAS5 | 3-6 months | ±35% | 6 months | High | ⚠️ |
| **Annual** | SEAS5/Decadal | 6-12 months | ±45% | 12-15 months | Medium | ❌ |

## Reasoning

### Why NOT 72-hour?

**Pros:**
- Low uncertainty (±10%)
- Fast validation (days)
- High confidence forecasts

**Cons:**
- ❌ Limited business value (operational adjustments only)
- ❌ Can't change pricing in 3 days
- ❌ Can't adjust reserves meaningfully
- ❌ Market not interested in ultra-short-term

**Etienne Feedback:**
> "72 hours too short for strategic decisions. Insurers need lead time to adjust pricing, reserves, and reinsurance."

### Why Quarterly?

**Pros:**
- ✅ Matches insurance business cycles (quarterly reporting)
- ✅ Sufficient lead time for pricing adjustments (1-3 months)
- ✅ Fast validation cycle (3 months to test accuracy)
- ✅ SEAS5 forecasts designed for this timeframe
- ✅ Balances uncertainty (±25%) with usability
- ✅ Enables advance reserves planning
- ✅ Supports quarterly reinsurance negotiations

**Cons:**
- ⚠️ Higher uncertainty than short-term (±25% vs ±10%)
- ⚠️ Requires longer validation period
- ⚠️ More complex modeling

**Business Impact:**
- Quarterly pricing reviews (standard industry practice)
- Reserve allocation planning
- Customer risk communication
- Reinsurance optimization

### Why NOT Annual?

**Pros:**
- Strategic timeframe
- Aligns with annual budgeting

**Cons:**
- ❌ Too high uncertainty (±45%)
- ❌ 12-15 months to validate accuracy (too slow)
- ❌ SEAS5 skill degrades significantly beyond 6 months
- ❌ Insurers can't lock in annual pricing (competitive pressure)

**Key Insight:**
Annual forecasts take 15+ months to validate (12-month lead + 3-month observation). Too slow for iterative product development.

## Decision

**Quarterly climate risk outlooks (1-3 months ahead)**

### Specific Implementation

**Forecast Delivery:**
- Q1 forecast: Issued in December (1-month lead)
- Q2 forecast: Issued in March
- Q3 forecast: Issued in June
- Q4 forecast: Issued in September

**Lead Times:**
- **1-month lead:** Primary product (highest skill)
- **2-month lead:** Secondary (medium skill)
- **3-month lead:** Strategic planning (lower skill)

**Validation Cycle:**
- Issue forecast: Month 0
- Observe quarter: Months 1-3
- Calculate accuracy: Month 4
- **Full feedback loop: 4 months**

## Date

Week 1 (After initial Etienne conversation)

## Impact

### Product Transformation

**Before:**
- 72-hour operational forecasts
- "Tell us if rain is coming this week"
- Tactical adjustments only

**After:**
- Quarterly strategic outlooks
- "Tell us if Q3 will have high claims"
- Pricing and reserves decisions

### Value Proposition Change

**Before (72-hour):**
- €50-100K/year (operational efficiency)
- Limited differentiation

**After (Quarterly):**
- €150-500K/year (strategic advantage)
- Clear competitive differentiation
- Measurable ROI (improved combined ratio)

### Development Timeline

**Before:**
- Validate in weeks
- Launch in 1-2 months

**After:**
- Validate in quarters (3-6 months)
- Launch in 6-9 months
- **Trade-off accepted:** Slower validation but higher value

## Validation

### Oslo Results

**Quarterly Approach Performance:**
- r = 0.33 (moderate correlation)
- 2015-Q3 event correctly identified
- 3-month validation cycle working
- **✅ Concept validated**

**Comparison to Thesis (Daily):**
- Thesis: AUC 0.65-0.79 (daily predictions)
- Our: r = 0.33 (quarterly)
- **Expected degradation** due to temporal aggregation
- Still commercially viable

## Lessons Learned

### Key Insights

1. **Timeframe drives value, not accuracy**
   - 72-hour forecasts very accurate but low value
   - Quarterly forecasts moderately accurate but high value
   - Sweet spot: 1-3 months

2. **Validation speed matters for iteration**
   - Annual: 15 months to validate
   - Quarterly: 4 months to validate
   - **3.75x faster learning cycle**

3. **Match forecast to business cycle**
   - Insurers think quarterly (reporting, pricing reviews)
   - Product aligned with customer workflow
   - Natural integration point

4. **ECMWF product alignment**
   - SEAS5 designed for 1-7 month lead times
   - Optimal skill at 1-3 months
   - Using product as intended (not forcing misfit)

## Alternative Considered: Hybrid Approach

**Could offer multiple timeframes:**
- Monthly: €150K/year
- Quarterly: €300K/year
- Seasonal (6-month): €500K/year

**Decision:** Start with quarterly only, add monthly/seasonal later based on demand

## Next Actions

- [x] Validate quarterly approach (Oslo complete)
- [ ] Build quarterly forecast delivery for Denmark
- [ ] Test 1-month, 2-month, 3-month lead times
- [ ] Measure skill degradation by lead time
- [ ] Offer tiered products based on lead time

---

**Decision Owner:** Giulio Pagnacco
**Date:** Week 1 (October 2024)
**Status:** ✅ Validated (Oslo r=0.33)
**Impact:** High (transformed product positioning)
