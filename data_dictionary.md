# Data Dictionary — Bluestock MF Capstone

## 01_fund_master.csv / dim_fund
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Unique AMFI scheme code (Primary Key) |
| fund_house | TEXT | AMC name e.g. SBI Mutual Fund |
| scheme_name | TEXT | Full official AMFI scheme name |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap etc. |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund launch date |
| benchmark | TEXT | Official benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio in % |
| exit_load_pct | REAL | Exit load percentage |
| fund_manager | TEXT | Primary fund manager name |
| risk_category | TEXT | Low / Moderate / High / Very High |

## 02_nav_history.csv / fact_nav
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | FK to dim_fund |
| date | DATE | NAV date (business days, forward-filled for holidays) |
| nav | REAL | Net Asset Value in Rs. |

## 07_scheme_performance.csv / fact_performance
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | FK to dim_fund |
| return_1yr_pct | REAL | 1-year absolute return % |
| return_3yr_pct | REAL | 3-year CAGR % |
| return_5yr_pct | REAL | 5-year CAGR % |
| alpha | REAL | Excess return above benchmark |
| beta | REAL | Market sensitivity (1.0 = same as market) |
| sharpe_ratio | REAL | Risk-adjusted return (higher is better) |
| sortino_ratio | REAL | Downside risk-adjusted return |
| max_drawdown_pct | REAL | Worst peak-to-trough decline (negative) |
| aum_crore | INTEGER | Assets under management in Rs. crore |

## 08_investor_transactions.csv / fact_transactions
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID (INV000001–INV005000) |
| transaction_date | DATE | Date of transaction |
| amfi_code | INTEGER | FK to dim_fund |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in rupees |
| state | TEXT | Investor's state |
| city_tier | TEXT | T30 (Top 30 cities) or B30 (Beyond Top 30) |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| kyc_status | TEXT | Verified / Pending |

## 03_aum_by_fund_house.csv / fact_aum
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Quarter end date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | AUM in Rs. lakh crore |
| aum_crore | INTEGER | AUM in Rs. crore |
| num_schemes | INTEGER | Number of schemes offered |

## 04_monthly_sip_inflows.csv / fact_sip_industry
| Column | Type | Description |
|--------|------|-------------|
| month | TEXT | YYYY-MM format |
| sip_inflow_crore | INTEGER | Monthly SIP inflows in Rs. crore |
| active_sip_accounts_crore | REAL | Active SIP accounts in crore |
| yoy_growth_pct | REAL | Year-on-year growth % (null for first 12 months) |

## 10_benchmark_indices.csv / fact_benchmark
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Trading date |
| index_name | TEXT | NIFTY50 / NIFTY100 / BSE SmallCap etc. |
| close_value | REAL | Closing index value |