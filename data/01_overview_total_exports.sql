-- Query 01: Total Vietnam export value by destination country, each year 2015–2024
-- PURPOSE:  Baseline trend — the foundation of every other query.
-- OUTPUT:   Main line chart data for Power BI Tab 1 (Overview).
SELECT
    year,
    partner,
    SUM(trade_value_usd)                            AS total_exports_usd,
    ROUND(SUM(trade_value_usd) / 1e9, 3)            AS total_exports_billion_usd
FROM clean_combined
WHERE year BETWEEN 2015 AND 2024
GROUP BY year, partner
ORDER BY partner, year;
