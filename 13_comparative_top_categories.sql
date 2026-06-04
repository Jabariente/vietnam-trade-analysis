-- Query 13: Side-by-side top 3 export categories per country — 2015 vs 2024
-- PURPOSE:  Has the specialisation of each bilateral relationship changed?
-- OUTPUT:   Comparative summary table in Power BI Tab 5.
WITH ranked AS (
    SELECT year, partner, hs2_code, hs2_description,
        SUM(trade_value_usd) AS total_usd,
        RANK() OVER (PARTITION BY year, partner
                     ORDER BY SUM(trade_value_usd) DESC) AS rnk
    FROM clean_combined WHERE year IN (2015, 2024)
    GROUP BY year, partner, hs2_code, hs2_description
)
SELECT partner, year, rnk, hs2_code, hs2_description,
    ROUND(total_usd/1e9, 3) AS value_billion
FROM ranked WHERE rnk <= 3
ORDER BY partner, year, rnk;
