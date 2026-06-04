-- Query 02: Year-over-year growth rate by country
-- PURPOSE:  Which bilateral relationship grew fastest, and when did growth accelerate?
-- OUTPUT:   YoY bar chart in Power BI Tab 1.
WITH yearly AS (
    SELECT year, partner, SUM(trade_value_usd) AS total_usd
    FROM clean_combined
    WHERE year BETWEEN 2015 AND 2024
    GROUP BY year, partner
)
SELECT
    c.year, c.partner,
    ROUND(c.total_usd / 1e9, 3)                         AS exports_billion,
    ROUND((c.total_usd - p.total_usd) * 100.0
          / NULLIF(p.total_usd, 0), 2)                  AS yoy_growth_pct
FROM yearly c
LEFT JOIN yearly p ON c.partner = p.partner AND c.year = p.year + 1
ORDER BY c.partner, c.year;
