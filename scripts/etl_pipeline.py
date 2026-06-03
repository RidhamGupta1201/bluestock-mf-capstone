"""
Bluestock MF Capstone — ETL Pipeline
Loads all cleaned CSVs into SQLite database (bluestock_mf.db)
"""

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# ── Paths ──────────────────────────────────────────────────────
BASE   = Path(__file__).resolve().parent.parent
PROC   = BASE / "data" / "processed"
DB_DIR = BASE / "data" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "bluestock_mf.db"

# ── Engine ─────────────────────────────────────────────────────
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# ── Run schema.sql ─────────────────────────────────────────────
with engine.connect() as conn:
    schema_sql = (BASE / "sql" / "schema.sql").read_text()
    for statement in schema_sql.split(";"):
        stmt = statement.strip()
        if stmt and not stmt.startswith("--"):
            try:
                conn.execute(text(stmt))
            except Exception as e:
                print(f"Schema warning: {e}")
    conn.commit()
print("✓ Schema created")

# ── Load helper ────────────────────────────────────────────────
def load(filename, table, if_exists="replace"):
    df = pd.read_csv(PROC / filename)
    df.to_sql(table, engine, if_exists=if_exists, index=False)
    # Verify
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
    print(f"✓ {table:<30} {count:>8} rows  (source: {len(df)} rows)")
    assert count == len(df), f"Row count mismatch for {table}!"

# ── Load all tables ────────────────────────────────────────────
print("\nLoading tables into SQLite...")
print("-" * 55)

load("clean_fund_master.csv",              "dim_fund")
load("clean_nav_history.csv",              "fact_nav")
load("clean_investor_transactions.csv",    "fact_transactions")
load("clean_scheme_performance.csv",       "fact_performance")
load("clean_aum_by_fund_house.csv",        "fact_aum")
load("clean_monthly_sip_inflows.csv",      "fact_sip_industry")
load("clean_portfolio_holdings.csv",       "fact_portfolio")
load("clean_category_inflows.csv",         "fact_category_inflows")
load("clean_industry_folio_count.csv",     "fact_folio_count")
load("clean_benchmark_indices.csv",        "fact_benchmark")

print("-" * 55)
print(f"\n✓ Database saved to: {DB_PATH}")