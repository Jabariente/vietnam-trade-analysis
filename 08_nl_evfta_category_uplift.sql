-- Query 08: Top 10 categories by absolute export uplift post-EVFTA (Netherlands)
-- PURPOSE:  Which sectors benefited most from tariff removal?
-- OUTPUT:   Waterfall chart in Power BI Tab 3.
WITH pa AS (
    SELECT hs2_code, hs2_description,
        AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END) AS pre,
        AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END) AS post
    FROM clean_combined WHERE partner = 'Netherlands'
    GROUP BY hs2_code, hs2_description
)
SELECT hs2_code, hs2_description,
    ROUND(pre/1e6,1)        AS pre_evfta_million,
    ROUND(post/1e6,1)       AS post_evfta_million,
    ROUND((post-pre)/1e6,1) AS uplift_million
FROM pa WHERE pre IS NOT NULL AND post IS NOT NULL
ORDER BY uplift_million DESC LIMIT 10;
