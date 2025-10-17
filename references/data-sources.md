# Data Sources

## Insurance Claims

### NASK (Finance Norway)
- **URL:** https://nask.finansnorge.no/
- **Description:** Norwegian Natural Perils Pool claims database
- **Coverage:** 1980-present, quarterly aggregates, municipality-level
- **Access:** Public (free)
- **Used for:** Oslo validation (2014-2021)

### EIOPA (European Insurance Authority)
- **URL:** https://www.eiopa.europa.eu/
- **Description:** European insurance statistics
- **Coverage:** EU member states, annual aggregates
- **Planned for:** Denmark validation

## Climate Data

### ERA5 (ECMWF Reanalysis)
- **URL:** https://cds.climate.copernicus.eu/
- **Description:** ECMWF's reanalysis dataset (observations)
- **Coverage:** 1940-present, global, hourly
- **Resolution:** 0.25° (~25km)
- **Access:** Free via CDS API
- **Used for:** Oslo observed precipitation (2014-2021)

### SEAS5 (ECMWF Seasonal Forecasts)
- **URL:** https://cds.climate.copernicus.eu/
- **Description:** Seasonal forecasts (1-7 months ahead)
- **Coverage:** 1993-present (hindcasts), current (operational)
- **Access:** Free via CDS API
- **Planned for:** Denmark MVP forecasts

## CDS API Setup

```bash
# Install
pip install cdsapi

# Configure
cat > ~/.cdsapirc << 'CREDENTIALS'
url: https://cds.climate.copernicus.eu/api/v2
key: {UID}:{API_KEY}
CREDENTIALS

# Accept terms on CDS website before first download
```

## References

**Primary Research:**
- Gorji, M., & Rødal, S. L. (2021). *Can Weather Forecasts Predict Norwegian Home Insurance Claims?* Norwegian School of Economics.

**ECMWF Documentation:**
- SEAS5 User Guide: https://www.ecmwf.int/en/forecasts/documentation-and-support/long-range-forecasting
- CDS API Guide: https://cds.climate.copernicus.eu/api-how-to
