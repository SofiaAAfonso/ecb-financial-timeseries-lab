# ECB Financial Time Series Lab

This repository contains a small Python project focused on time-series analysis of official monetary and financial statistics published by the European Central Bank (ECB).

The project is designed as a realistic, reproducible pipeline for:
- retrieving ECB datasets programmatically,
- performing quality checks on time-indexed data,
- transforming and analysing financial time series,
- producing basic analytical outputs and diagnostic charts.

It reflects the type of statistical and analytical tasks typically carried out in the context of ECB monetary and financial statistics (e.g. interest rates, balance sheet indicators, and structural financial indicators).

## Scope and focus

The current implementation focuses on **Monetary Financial Institutions (MIR)** interest rate statistics, with planned extensions to:

- **BSI** – Balance Sheet Items (banking stocks and flows),
- **SSI** – Structural Financial Indicators (banking structure and concentration),
- country vs euro area comparisons,
- additional time-series indicators and diagnostics.

The project intentionally prioritises:
- clarity of data handling,
- reproducibility,
- explicit quality checks,
- transparent time-series transformations.

## Data sources

All data used in this project come from the official **ECB Data Portal** and are accessed via the ECB SDMX REST interface.

Initial dataset:
- **MIR – MFI Interest Rate Statistics**  
  Monthly interest rates on new business for housing loans to households (Portugal).

Planned extensions:
- **BSI – Balance Sheet Items** (loans, deposits, stocks and growth rates)
- **SSI – Banking structural indicators** (market concentration, number of institutions, etc.)

No data is manually downloaded; all datasets are retrieved programmatically through the ECB API.

## Project structure

```text
src/ecb_ts_lab/
    ecb_api.py          # ECB Data Portal client (CSV via SDMX API)
    run_mir_pt.py       # First working pipeline: MIR Portugal
    __init__.py

data/
    raw/                # Raw downloads (optional)
    processed/          # Cleaned time-series outputs

reports/
    figures/            # Plots and diagnostics
    quality/            # Data quality reports

notebooks/              # Exploratory work (future use)
requirements.txt        # Python dependencies
