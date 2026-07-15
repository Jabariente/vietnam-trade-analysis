-- Query 04: Top 10 HS categories exported to Japan by value, 2024
-- PURPOSE:  Establish current composition — electronics at 26%. What else matters?
-- OUTPUT:   Treemap in Power BI Tab 2 (Japan Deep Dive).
SELECT
    hs2_code, hs2_description,
    ROUND(SUM(trade_value_usd) / 1e9, 3)                AS value_billion,
    ROUND(SUM(trade_value_usd) * 100.0
          / SUM(SUM(trade_value_usd)) OVER (), 2)       AS share_pct
FROM clean_combined
WHERE partner = 'Japan' AND year = 2024
GROUP BY hs2_code, hs2_description
ORDER BY value_billion DESC
LIMIT 10;
