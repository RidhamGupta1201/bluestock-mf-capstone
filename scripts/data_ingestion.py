"""
Bluestock MF Capstone — data_ingestion.py
Loads all 10 provided CSV datasets and prints shape, dtypes, head()
for each to understand the data structure.
Run: python scripts/data_ingestion.py
"""

from pathlib import Path
import pandas as pd

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

print("=" * 50)
print("CSV DATA INSPECTION")
print("=" * 50)

csv_files = list(RAW_DIR.glob("*.csv"))

for file in csv_files:
    print(f"\nProcessing: {file.name}")

    try:
        df = pd.read_csv(file)

        print(f"Shape: {df.shape}")

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        print("-" * 50)

    except Exception as e:
        print(f"Error reading {file.name}: {e}")