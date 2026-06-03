-- ============================================================
-- Bluestock MF Capstone — 10 Analytical SQL Queries
-- ============================================================

-- Q1: Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Q2: Average NAV per month for each fund
SELECT amfi_code,
       STRFTIME('%Y-%m', date) AS month,
       ROUND(AVG(nav), 4)      AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- Q3: SIP inflow YoY growth
SELECT month,
       sip_inflow_crore,
       ROUND(yoy_growth_pct, 2) AS yoy_growth_pct
FROM fact_sip_industry
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;

-- Q4: Total transaction amount by state
SELECT state,
       COUNT(*)             AS total_transactions,
       SUM(amount_inr)      AS total_amount_inr,
       ROUND(AVG(amount_inr), 2) AS avg_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- Q5: Funds with expense_ratio < 1%
SELECT f.scheme_name, f.fund_house, f.expense_ratio_pct, f.plan
FROM dim_fund f
WHERE f.expense_ratio_pct < 1.0
ORDER BY f.expense_ratio_pct ASC;

-- Q6: Top 5 funds by Sharpe ratio
SELECT scheme_name, fund_house, sharpe_ratio, return_3yr_pct, risk_grade
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;

-- Q7: AUM growth by fund house over time
SELECT fund_house,
       STRFTIME('%Y', date) AS year,
       ROUND(AVG(aum_lakh_crore), 2) AS avg_aum_lakh_crore
FROM fact_aum
GROUP BY fund_house, year
ORDER BY fund_house, year;

-- Q8: Transaction split by type (SIP vs Lumpsum vs Redemption)
SELECT transaction_type,
       COUNT(*)                        AS count,
       SUM(amount_inr)                 AS total_amount,
       ROUND(AVG(amount_inr), 2)       AS avg_amount
FROM fact_transactions
GROUP BY transaction_type;

-- Q9: Top sectors by total portfolio weight
SELECT sector,
       ROUND(SUM(weight_pct), 2)  AS total_weight_pct,
       COUNT(DISTINCT amfi_code)  AS num_funds
FROM fact_portfolio
GROUP BY sector
ORDER BY total_weight_pct DESC
LIMIT 10;

-- Q10: Best performing funds (1yr return) vs their benchmark
SELECT p.scheme_name,
       p.return_1yr_pct,
       p.benchmark_3yr_pct,
       p.alpha,
       p.sharpe_ratio,
       f.benchmark
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 10;