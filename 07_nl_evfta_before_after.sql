-- Query 07: Netherlands — pre-EVFTA (2015–2019) vs post-EVFTA (2021–2024) avg
-- PURPOSE:  Core before/after question. Your Netherlands headline finding.
-- NOTE:     2020 excluded — EVFTA in force Aug 1; partial year distorts comparison.
SELECT
    hs2_code, hs2_description,
    ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END)/1e6,1)
        AS avg_pre_evfta_million,
    ROUND(AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END)/1e6,1)
        AS avg_post_evfta_million,
    ROUND(
        (AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END)
         - AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END)) * 100.0
        / NULLIF(AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END), 0)
    , 2) AS change_pct
FROM clean_combined
WHERE partner = 'Netherlands'
GROUP BY hs2_code, hs2_description
ORDER BY change_pct DESC;
