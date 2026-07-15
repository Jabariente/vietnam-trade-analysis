-- Query 05: Japan — categories with >10% CAGR over 2015–2024
-- PURPOSE:  Where is growth beyond electronics? Find the fast-rising sectors.
WITH endpoints AS (
    SELECT hs2_code, hs2_description,
        SUM(CASE WHEN year = 2015 THEN trade_value_usd ELSE 0 END) AS v2015,
        SUM(CASE WHEN year = 2024 THEN trade_value_usd ELSE 0 END) AS v2024
    FROM clean_combined WHERE partner = 'Japan'
    GROUP BY hs2_code, hs2_description
)
SELECT
    hs2_code, hs2_description,
    ROUND(v2015 / 1e6, 1)   AS value_2015_million,
    ROUND(v2024 / 1e6, 1)   AS value_2024_million,
    ROUND((POWER(CAST(v2024 AS FLOAT) / NULLIF(v2015, 0), 1.0/9) - 1) * 100, 2) AS cagr_pct
FROM endpoints
WHERE v2015 > 0 AND v2024 > 0
HAVING cagr_pct > 10
ORDER BY cagr_pct DESC;
