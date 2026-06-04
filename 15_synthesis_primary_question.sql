-- Query 15: SYNTHESIS — Primary research question answered in one result set
-- PURPOSE:  Headline output for Power BI Tab 5 and the business memo.
--           One row per country: 2024 total, 10-yr CAGR, top category, top share.
WITH totals AS (
    SELECT partner,
        SUM(CASE WHEN year=2015 THEN trade_value_usd END) AS v2015,
        SUM(CASE WHEN year=2024 THEN trade_value_usd END) AS v2024
    FROM clean_combined GROUP BY partner
),
top_cat AS (
    SELECT partner, hs2_description AS top_category
    FROM (
        SELECT partner, hs2_description,
            RANK() OVER (PARTITION BY partner
                         ORDER BY SUM(trade_value_usd) DESC) AS rnk
        FROM clean_combined WHERE year=2024
        GROUP BY partner, hs2_description
    ) WHERE rnk = 1
),
top_share AS (
    SELECT partner,
        ROUND(MAX(share_pct), 1) AS top_cat_share_pct
    FROM (
        SELECT partner,
            SUM(trade_value_usd) * 100.0
            / SUM(SUM(trade_value_usd)) OVER (PARTITION BY partner) AS share_pct
        FROM clean_combined WHERE year=2024
        GROUP BY partner, hs2_code
    ) GROUP BY partner
)
SELECT
    t.partner,
    ROUND(t.v2015/1e9, 2)   AS exports_2015_billion,
    ROUND(t.v2024/1e9, 2)   AS exports_2024_billion,
    ROUND((POWER(CAST(t.v2024 AS FLOAT)/NULLIF(t.v2015,0), 1.0/9)-1)*100, 2)
                             AS cagr_pct,
    c.top_category,
    s.top_cat_share_pct
FROM totals t
JOIN top_cat c   ON t.partner = c.partner
JOIN top_share s ON t.partner = s.partner
ORDER BY t.v2024 DESC;
