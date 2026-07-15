-- Query 10: Vietnam exports to Italy by HS category, 2015–2024
-- PURPOSE:  Full picture — broadcasting equipment, iron, coffee dominate. Where is apparel?
-- OUTPUT:   Feeds Power BI Tab 4 (Italy: Premium Markets).
SELECT year, hs2_code, hs2_description,
    ROUND(SUM(trade_value_usd)/1e6, 1) AS value_million
FROM clean_combined
WHERE partner = 'Italy' AND year BETWEEN 2015 AND 2024
GROUP BY year, hs2_code, hs2_description
ORDER BY year, value_million DESC;
