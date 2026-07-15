-- Query 14: Structural shift — category share change 2015 → 2024, all three countries
-- PURPOSE:  Which country shows highest compositional change? Answers primary question.
-- METHOD:   Compare share_pct per HS category between 2015 and 2024.
--           Large absolute share_change = high structural shift.
WITH shares AS (
    SELECT year, partner, hs2_code, hs2_description,
        SUM(trade_value_usd) * 100.0
        / SUM(SUM(trade_value_usd)) OVER (PARTITION BY year, partner) AS share_pct
    FROM clean_combined WHERE year IN (2015, 2024)
    GROUP BY year, partner, hs2_code, hs2_description
),
pivot AS (
    SELECT partner, hs2_code, hs2_description,
        MAX(CASE WHEN year=2015 THEN share_pct END) AS share_2015,
        MAX(CASE WHEN year=2024 THEN share_pct END) AS share_2024
    FROM shares GROUP BY partner, hs2_code, hs2_description
)
SELECT partner, hs2_code, hs2_description,
    ROUND(share_2015, 2) AS share_2015_pct,
    ROUND(share_2024, 2) AS share_2024_pct,
    ROUND(share_2024 - share_2015, 2) AS share_change_ppt
FROM pivot WHERE share_2015 IS NOT NULL AND share_2024 IS NOT NULL
ORDER BY partner, ABS(share_2024 - share_2015) DESC;
