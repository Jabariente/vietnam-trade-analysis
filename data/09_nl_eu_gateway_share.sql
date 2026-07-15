-- Query 09: Netherlands as % of Vietnam's total EU exports, by year
-- PURPOSE:  Does Rotterdam's gateway share grow or shrink over the decade?
-- NOTE:     Requires eurostat_vnm_totals table (load from Eurostat Comext CSV).
WITH nl AS (
    SELECT year, SUM(trade_value_usd) AS nl_exports
    FROM clean_combined WHERE partner = 'Netherlands' GROUP BY year
)
SELECT
    nl.year,
    ROUND(nl.nl_exports/1e9, 2)                         AS nl_exports_billion,
    ROUND(e.total_eu_imports_usd/1e9, 2)                AS eu_total_billion,
    ROUND(nl.nl_exports * 100.0
          / NULLIF(e.total_eu_imports_usd, 0), 2)       AS nl_share_of_eu_pct
FROM nl JOIN eurostat_vnm_totals e ON nl.year = e.year
ORDER BY nl.year;
