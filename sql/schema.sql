PRAGMA foreign_keys = ON;

-- ── Dimension: Fund ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT    NOT NULL,
    scheme_name         TEXT    NOT NULL,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      INTEGER,
    min_lumpsum_amount  INTEGER,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

-- ── Dimension: Date ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_date (
    date_id     TEXT PRIMARY KEY,
    year        INTEGER,
    month       INTEGER,
    quarter     INTEGER,
    month_name  TEXT,
    is_weekday  INTEGER
);

-- ── Fact: NAV History ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_nav (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code       INTEGER NOT NULL,
    date            TEXT    NOT NULL,
    nav             REAL    NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
CREATE INDEX IF NOT EXISTS idx_nav_code_date ON fact_nav(amfi_code, date);

-- ── Fact: Investor Transactions ─────────────────────────────
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    transaction_date    TEXT,
    amfi_code           INTEGER,
    transaction_type    TEXT,
    amount_inr          INTEGER,
    state               TEXT,
    city                TEXT,
    city_tier           TEXT,
    age_group           TEXT,
    gender              TEXT,
    annual_income_lakh  REAL,
    payment_mode        TEXT,
    kyc_status          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- ── Fact: Scheme Performance ────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code           INTEGER PRIMARY KEY,
    scheme_name         TEXT,
    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,
    benchmark_3yr_pct   REAL,
    alpha               REAL,
    beta                REAL,
    sharpe_ratio        REAL,
    sortino_ratio       REAL,
    std_dev_ann_pct     REAL,
    max_drawdown_pct    REAL,
    aum_crore           INTEGER,
    expense_ratio_pct   REAL,
    morningstar_rating  INTEGER,
    risk_grade          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- ── Fact: AUM by Fund House ─────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_aum (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT,
    fund_house      TEXT,
    aum_lakh_crore  REAL,
    aum_crore       INTEGER,
    num_schemes     INTEGER
);

-- ── Fact: SIP Industry Inflows ──────────────────────────────
CREATE TABLE IF NOT EXISTS fact_sip_industry (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    month                       TEXT,
    sip_inflow_crore            INTEGER,
    active_sip_accounts_crore   REAL,
    new_sip_accounts_lakh       REAL,
    sip_aum_lakh_crore          REAL,
    yoy_growth_pct              REAL
);

-- ── Fact: Portfolio Holdings ────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_portfolio (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           INTEGER,
    stock_symbol        TEXT,
    stock_name          TEXT,
    sector              TEXT,
    weight_pct          REAL,
    market_value_cr     REAL,
    current_price_inr   REAL,
    portfolio_date      TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- ── Fact: Category Inflows ──────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_category_inflows (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    month               TEXT,
    category            TEXT,
    net_inflow_crore    REAL
);

-- ── Fact: Industry Folio Count ──────────────────────────────
CREATE TABLE IF NOT EXISTS fact_folio_count (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    month                   TEXT,
    total_folios_crore      REAL,
    equity_folios_crore     REAL,
    debt_folios_crore       REAL,
    hybrid_folios_crore     REAL,
    others_folios_crore     REAL
);

-- ── Fact: Benchmark Indices ─────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_benchmark (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT,
    index_name  TEXT,
    close_value REAL
);