# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### In Progress
- Denmark data pipeline development
- SEAS5 seasonal forecast integration
- MVP dashboard design

## [0.2.0] - 2024-10-17

### Added
- Oslo validation complete (r=0.33, p=0.066)
- Real NASK insurance claims data integration (78.3M NOK, 32 quarters)
- ERA5 observed precipitation analysis
- Correlation analysis and statistical validation
- Event detection scorecard (2015-Q3 flooding correctly identified)
- Complete documentation suite
- Geographic market analysis
- BD lead prioritization
- MVP roadmap (8-10 weeks)
- Decision logs (quarterly-vs-annual, norway-vs-denmark, real-vs-synthetic)

### Changed
- Switched from synthetic to real claims data
- Fixed negative correlation artifact (r=-0.78 → r=+0.33)
- Refined product positioning (quarterly strategic vs. 72-hour operational)

### Technical
- 32 quarters analyzed (2014-2021)
- 3 visualizations generated
- Complete reproducible pipeline

## [0.1.0] - 2024-10

### Added
- Initial ECMWF infrastructure setup
- CDS API integration
- Synthetic claims data generation (thesis-based)
- NetCDF processing pipeline
- Basic correlation framework

### Research
- Norwegian School of Economics thesis analysis
- Literature review
- ECMWF SEAS5 capabilities assessment

## [0.0.1] - 2024-10

### Initial Concept
- 72-hour operational forecasting idea
- Based on NHH thesis (AUC 0.65-0.79)
- Strategic pivot to quarterly forecasting

---

## Version Naming

- **0.0.x:** Concept and research
- **0.1.x:** Infrastructure development
- **0.2.x:** Oslo validation (current)
- **0.3.x:** Denmark MVP (planned)
- **1.0.0:** First commercial pilot (Q1 2025 target)
