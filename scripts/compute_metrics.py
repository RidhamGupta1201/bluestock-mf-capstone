"""
Computes all performance metrics from NAV history:
  - Daily returns
  - CAGR (1yr, 3yr, full-range proxy)
  - Sharpe Ratio (Rf = 6.5%)
  - Sortino Ratio
  - Alpha & Beta (OLS vs NIFTY100)
  - Maximum Drawdown
  - Fund Scorecard (composite 0-100)
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

BASE  = Path(__file__).resolve().parent.parent
PROC  = BASE / "data" / "processed"
Rf    = 0.065 

def load_data():
    nav   = pd.read_csv(PROC / "clean_nav_history.csv")
    bench = pd.read_csv(PROC / "clean_benchmark_indices.csv")
    fm    = pd.read_csv(PROC / "clean_fund_master.csv")
    perf  = pd.read_csv(PROC / "clean_scheme_performance.csv")
    nav["date"]   = pd.to_datetime(nav["date"])
    bench["date"] = pd.to_datetime(bench["date"])
    return nav, bench, fm, perf

def compute_daily_returns(nav):
    """Compute daily returns: nav_t / nav_t-1 - 1"""
    nav = nav.sort_values(["amfi_code", "date"]).copy()
    nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()
    returns = nav.dropna(subset=["daily_return"])
    returns.to_csv(PROC / "returns_computed.csv", index=False)
    print(f"✓ returns_computed.csv — {len(returns):,} rows")
    return returns

def compute_cagr(nav, fm):
    """Compute CAGR: (NAV_end/NAV_start)^(1/n) - 1"""
    latest = nav["date"].max()
    start  = nav["date"].min()
    years_avail = (latest - start).days / 365.25

    nav_end   = nav.sort_values("date").groupby("amfi_code").last().reset_index()[["amfi_code","nav"]].rename(columns={"nav":"nav_end"})
    nav_start = nav.sort_values("date").groupby("amfi_code").first().reset_index()[["amfi_code","nav"]].rename(columns={"nav":"nav_start"})

    def get_nav_at(target):
        s = nav[nav["date"] >= target - pd.Timedelta(days=5)]
        return s.groupby("amfi_code").first().reset_index()[["amfi_code","nav"]]

    n1 = get_nav_at(latest - pd.DateOffset(years=1)).rename(columns={"nav":"nav_1yr"})
    n3 = get_nav_at(latest - pd.DateOffset(years=3)).rename(columns={"nav":"nav_3yr"})

    cagr = nav_end.merge(n1, on="amfi_code").merge(n3, on="amfi_code").merge(nav_start, on="amfi_code")
    cagr = cagr.merge(fm[["amfi_code","scheme_name","fund_house","category","plan"]], on="amfi_code")
    cagr["cagr_1yr_pct"]      = ((cagr["nav_end"] / cagr["nav_1yr"]) ** (1/1)          - 1) * 100
    cagr["cagr_3yr_pct"]      = ((cagr["nav_end"] / cagr["nav_3yr"]) ** (1/3)          - 1) * 100
    cagr["cagr_5yr_proxy_pct"]= ((cagr["nav_end"] / cagr["nav_start"]) ** (1/years_avail) - 1) * 100
    cagr.to_csv(PROC / "cagr_report.csv", index=False)
    print(f"✓ cagr_report.csv — {len(cagr)} funds (5yr uses {years_avail:.1f}yr proxy)")
    return cagr

def compute_sharpe(returns, fm):
    """Sharpe = (ann_return - Rf) / ann_std × √252"""
    rows = []
    for code, g in returns.groupby("amfi_code"):
        r = g["daily_return"]
        n = len(r)
        ann_r = (1 + r).prod() ** (252 / n) - 1
        ann_s = r.std() * np.sqrt(252)
        rows.append({"amfi_code": code,
                     "ann_return": round(ann_r*100,4),
                     "ann_std"   : round(ann_s*100,4),
                     "sharpe_ratio": round((ann_r - Rf)/ann_s, 4) if ann_s>0 else np.nan})
    df = pd.DataFrame(rows).merge(fm[["amfi_code","scheme_name","category","plan"]], on="amfi_code")
    df.sort_values("sharpe_ratio", ascending=False).to_csv(PROC / "sharpe_values.csv", index=False)
    print(f"✓ sharpe_values.csv — {len(df)} funds")
    return df

def compute_sortino(returns, fm):
    """Sortino = (ann_return - Rf) / downside_std"""
    rows = []
    for code, g in returns.groupby("amfi_code"):
        r = g["daily_return"]
        n = len(r)
        ann_r    = (1 + r).prod() ** (252 / n) - 1
        neg      = r[r < 0]
        down_std = neg.std() * np.sqrt(252) if len(neg) > 1 else np.nan
        rows.append({"amfi_code"    : code,
                     "ann_return"   : round(ann_r*100,4),
                     "downside_std" : round(down_std*100,4) if down_std else np.nan,
                     "sortino_ratio": round((ann_r-Rf)/down_std,4) if down_std and down_std>0 else np.nan,
                     "neg_days"     : len(neg)})
    df = pd.DataFrame(rows).merge(fm[["amfi_code","scheme_name","category","plan"]], on="amfi_code")
    df.sort_values("sortino_ratio", ascending=False).to_csv(PROC / "sortino_values.csv", index=False)
    print(f"✓ sortino_values.csv — {len(df)} funds")
    return df

def compute_alpha_beta(returns, bench, fm):
    """Alpha & Beta via OLS regression vs NIFTY100"""
    nifty = bench[bench["index_name"]=="NIFTY100"].sort_values("date").copy()
    nifty["bench_return"] = nifty["close_value"].pct_change()
    rows = []
    for code, g in returns.groupby("amfi_code"):
        m = g.merge(nifty[["date","bench_return"]], on="date").dropna()
        if len(m) < 30:
            continue
        slope, intercept, r_val, p_val, _ = stats.linregress(m["bench_return"], m["daily_return"])
        rows.append({"amfi_code"        : code,
                     "beta"             : round(slope, 4),
                     "alpha_annualised" : round(intercept*252*100, 4),
                     "r_squared"        : round(r_val**2, 4),
                     "n_obs"            : len(m)})
    df = pd.DataFrame(rows).merge(fm[["amfi_code","scheme_name","category","plan"]], on="amfi_code")
    df.sort_values("alpha_annualised", ascending=False).to_csv(PROC / "alpha_beta.csv", index=False)
    print(f"✓ alpha_beta.csv — {len(df)} funds")
    return df

def compute_max_drawdown(nav, fm):
    """Max Drawdown = min(NAV / running_max - 1)"""
    rows = []
    for code, g in nav.groupby("amfi_code"):
        g = g.sort_values("date").copy()
        g["running_max"] = g["nav"].cummax()
        g["drawdown"]    = g["nav"] / g["running_max"] - 1
        idx = g["drawdown"].idxmin()
        rows.append({"amfi_code"      : code,
                     "max_drawdown"   : round(g.loc[idx,"drawdown"]*100, 4),
                     "trough_date"    : g.loc[idx,"date"].date()})
    df = pd.DataFrame(rows).merge(fm[["amfi_code","scheme_name","category","plan"]], on="amfi_code")
    df.sort_values("max_drawdown").to_csv(PROC / "max_drawdown.csv", index=False)
    print(f"✓ max_drawdown.csv — {len(df)} funds")
    return df

def compute_scorecard(sharpe_df, cagr_df, sortino_df, ab_df, dd_df, fm):
    """Composite scorecard — uses our computed metrics, not pre-existing values"""
    df = sharpe_df[["amfi_code", "sharpe_ratio"]].copy()
    df = df.merge(cagr_df[["amfi_code", "cagr_3yr_pct"]], on="amfi_code")
    df = df.merge(sortino_df[["amfi_code", "sortino_ratio"]], on="amfi_code")
    df = df.merge(ab_df[["amfi_code", "alpha_annualised"]], on="amfi_code")
    df = df.merge(dd_df[["amfi_code", "max_drawdown"]], on="amfi_code")
    df = df.merge(fm[["amfi_code", "scheme_name", "fund_house",
                       "category", "plan", "expense_ratio_pct"]], on="amfi_code")

    n = len(df)
    df["rank_3yr_return"] = df["cagr_3yr_pct"].rank(ascending=True)       / n * 100
    df["rank_sharpe"]     = df["sharpe_ratio"].rank(ascending=True)        / n * 100
    df["rank_alpha"]      = df["alpha_annualised"].rank(ascending=True)    / n * 100
    df["rank_expense"]    = df["expense_ratio_pct"].rank(ascending=False)  / n * 100
    df["rank_max_dd"]     = df["max_drawdown"].rank(ascending=False)       / n * 100
    df["composite_score"] = (
        df["rank_3yr_return"] * 0.30 +
        df["rank_sharpe"]     * 0.25 +
        df["rank_alpha"]      * 0.20 +
        df["rank_expense"]    * 0.15 +
        df["rank_max_dd"]     * 0.10
    ).round(2)
    df = df.sort_values("composite_score", ascending=False).reset_index(drop=True)
    df["scorecard_rank"] = range(1, len(df) + 1)
    df.to_csv(PROC / "fund_scorecard.csv", index=False)
    print(f"✓ fund_scorecard.csv — {len(df)} funds ranked from our pipeline")
    return df

if __name__ == "__main__":
    print("=" * 50)
    print("Bluestock MF — Computing Performance Metrics")
    print("=" * 50)
    nav, bench, fm, perf = load_data()
    returns  = compute_daily_returns(nav)
    cagr     = compute_cagr(nav, fm)
    sharpe   = compute_sharpe(returns, fm)
    sortino  = compute_sortino(returns, fm)
    ab       = compute_alpha_beta(returns, bench, fm)
    dd       = compute_max_drawdown(nav, fm)
    scorecard = compute_scorecard(sharpe, cagr, sortino, ab, dd, fm)
    print("\n✓ All metrics computed and saved to data/processed/")