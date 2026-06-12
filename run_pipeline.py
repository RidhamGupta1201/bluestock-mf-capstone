"""
Bluestock MF Capstone — run_pipeline.py
Master script — runs the entire ETL + analytics pipeline end-to-end.
Run: python run_pipeline.py
"""

import subprocess
import sys

steps = [
    ("scripts/etl_pipeline.py",   "Loading data into SQLite database"),
    ("scripts/compute_metrics.py","Computing performance metrics (Sharpe, CAGR, etc.)"),
    ("scripts/recommender.py",    "Running fund recommendation engine"),
]

print("=" * 55)
print("BLUESTOCK MF CAPSTONE — MASTER PIPELINE")
print("=" * 55)

for script, description in steps:
    print(f"\n▶ {description}")
    print(f"  Running: {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\n✗ Pipeline failed at: {script}")
        sys.exit(1)
    print(f"  ✓ Done")

print("\n" + "=" * 55)
print("✓ PIPELINE COMPLETE — all metrics and database ready")
print("=" * 55)
print("\nNext steps:")
print("  1. Open dashboard/bluestock_mf.pbix in Power BI Desktop")
print("  2. Click 'Refresh' to load latest data/processed/ CSVs")