"""
Simple fund recommendation engine.
Input : investor risk appetite (Low/Moderate/Moderately High/High/Very High)
Output: Top 3 funds by Sharpe ratio within matching risk_grade
Run   : python scripts/recommender.py
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "data" / "processed"

def load_data():
    sharpe = pd.read_csv(PROC / "sharpe_values.csv")
    perf   = pd.read_csv(PROC / "clean_scheme_performance.csv")
    return sharpe.merge(
        perf[["amfi_code","risk_grade","return_3yr_pct",
              "expense_ratio_pct","max_drawdown_pct"]],
        on="amfi_code"
    )

def recommend(risk_appetite: str, data: pd.DataFrame, top_n: int = 3):
    valid = ["Low","Moderate","Moderately High","High","Very High"]
    if risk_appetite not in valid:
        print(f"❌ Invalid. Choose from: {valid}")
        return

    filtered = (data[data["risk_grade"] == risk_appetite]
                .sort_values("sharpe_ratio", ascending=False)
                .head(top_n))

    if filtered.empty:
        print(f"No funds found for: {risk_appetite}")
        return

    print(f"\n{'─'*60}")
    print(f"Top {top_n} Recommended Funds — Risk: {risk_appetite}")
    print(f"{'─'*60}")
    for i, (_, row) in enumerate(filtered.iterrows(), 1):
        name = (row["scheme_name"]
                .replace(" - Regular Plan - Growth","")
                .replace(" - Direct Plan - Growth","")
                .replace(" Fund",""))
        print(f"{i}. {name}")
        print(f"   Category    : {row['category']} | {row['plan']}")
        print(f"   Sharpe Ratio: {row['sharpe_ratio']:.4f}")
        print(f"   3yr CAGR    : {row['ann_return']:.2f}%")
        print(f"   Expense     : {row['expense_ratio_pct']}%")
        print(f"   Max Drawdown: {row['max_drawdown_pct']}%")

if __name__ == "__main__":
    print("=" * 60)
    print("BLUESTOCK MF — FUND RECOMMENDATION ENGINE")
    print("=" * 60)

    data = load_data()

    for risk in ["Low","Moderate","Moderately High","High","Very High"]:
        recommend(risk, data)

    print(f"\n{'─'*60}")
    print("Usage: import and call recommend(risk_appetite, data)")
    print("Example: recommend('High', data)")