-- Query 12: Italy's share of Vietnam's total EU exports, by year
-- PURPOSE:  How significant is Italy vs Netherlands? Is the share stable or growing?
WITH it AS (
    SELECT year, SUM(trade_value_usd) AS italy_exports
    FROM clean_combined WHERE partner = 'Italy' GROUP BY year
)
SELECT
    it.year,
    ROUND(it.italy_exports/1e9, 2)                      AS italy_billion,
    ROUND(e.total_eu_imports_usd/1e9, 2)                AS eu_total_billion,
    ROUND(it.italy_exports * 100.0
          / NULLIF(e.total_eu_imports_usd, 0), 2)       AS italy_share_of_eu_pct
FROM it JOIN eurostat_vnm_totals e ON it.year = e.year
ORDER BY it.year;
