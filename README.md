# INE Health Data Analysis

An in-progress, reproducible health-data analysis project using public microdata
from Spain's National Statistics Institute (INE). It is intended to develop
practical skills in health-data extraction, validation, cleaning, documentation,
and exploratory analysis.

## Status

Initial project setup. The data-acquisition and processing pipeline is under
development.

## Planned workflow

1. Obtain the official INE source archives.
2. Extract and validate the source files reproducibly.
3. Create documented, analysis-ready datasets.
4. Perform exploratory analysis and communicate findings with appropriate
   limitations.

## Setup

This project uses Python 3.13. From the project root in Windows Command Prompt:

```bat
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.bat
python -m pip install -r requirements.txt
```

## Data

Source microdata are intentionally not included in this repository. Downloaded
archives belong in `data/raw/`; extracted and intermediate files belong in
`data/interim/`; and analysis-ready datasets belong in `data/processed/`.
All contents of `data/` are excluded from version control.

The official source, download instructions, and data-handling notes will be
documented before the analysis is published.

## Repository structure

```text
ine_health_data/  Reusable Python code for extraction, validation, and analysis.
notebooks/        Exploratory analysis notebooks.
references/       Data dictionaries, source documentation, and methodology notes.
reports/          Generated analysis outputs and figures.
```
