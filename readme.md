# Bluestock MF Capstone — Mutual Fund Analytics Platform

End-to-end data engineering and analytics project built during 
internship at Bluestock Fintech Pvt. Ltd., June 2026.

## Project Overview
Builds a full-stack Mutual Fund Analytics Platform that:
- Ingests 10 publicly available AMFI datasets (87,533 rows)
- Transforms data through a Python ETL pipeline
- Stores in a 10-table SQLite star schema database
- Analyses 40 fund schemes with 7 performance metrics
- Presents insights via a 4-page interactive Power BI dashboard

## Key Numbers
| Metric | Value |
|--------|-------|
| Fund Schemes | 40 |
| NAV Records | 46,000 |
| Investor Transactions | 32,778 |
| Database Rows | 87,533 |
| Dashboard Pages | 4 |
| States Covered | 12 |

## Tech Stack
Python 3.10 | Pandas | NumPy | SciPy | SQLite | SQLAlchemy
Matplotlib | Seaborn | Plotly | Power BI | Git

## Setup Instructions
```bash
# 1. Clone the repo
git clone https://github.com/RidhamGupta1201/bluestock-mf-capstone.git
cd bluestock-mf-capstone

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run ETL pipeline
python scripts/etl_pipeline.py

# 5. Compute performance metrics
python scripts/compute_metrics.py

# 6. Open dashboard
# Open dashboard/bluestock_mf.pbix in Power BI Desktop
```

## How to Run Each Day's Work
| Day | Notebook/Script | Output |
|-----|----------------|--------|
| Day 1 | notebooks/01_data_ingestion.ipynb | 15 raw CSVs |
| Day 2 | notebooks/02_data_cleaning.ipynb + scripts/etl_pipeline.py | SQLite DB |
| Day 3 | notebooks/03_eda_analysis.ipynb | 15+ charts |
| Day 4 | notebooks/04_performance_analytics.ipynb | 7 metric CSVs |
| Day 5 | dashboard/bluestock_mf.pbix | Power BI dashboard |
| Day 6 | notebooks/05_advanced_analytics.ipynb | VaR, HHI, recommender |
| Day 7 | reports/Bluestock_MF_Final_Report.pdf + Bluestock_MF_Presentation.pptx | Final Report and Presentation |


## Data Sources
- AMFI India: amfiindia.com
- mfapi.in: api.mfapi.in/mf/{amfi_code}
- NSE India: nseindia.com/reports

## Project Structure
Bluestock MF Capstone
│
├── Data/
│   ├── raw/  ← 15 original CSV files
│   ├── processed/  ← 17 cleaned + metric CSV files
│   └── db/  ← bluestock_mf.db (SQLite)
│
├── notebooks/  ← 6 Jupyter notebooks
|
├── scripts/  ← 6 Python scripts
│
├── sql/  ← schema.sql + queries.sql
│
├── dashboard/  ← bluestock_mf.pbix
│
├── reports/  ← charts + quality reports + final reports and presentations
|
├── data_dictionary.md
|
└── requirements.txt