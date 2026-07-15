-- Query 11: Textiles + footwear (HS 61–64) value trend — Italy
-- PURPOSE:  Italy exports leather → Vietnam processes → ships back finished footwear/apparel.
--           Track whether this finished-goods flow grows over the decade.
SELECT year, hs2_code, hs2_description,
    ROUND(SUM(trade_value_usd)/1e6, 1) AS value_million
FROM clean_combined
WHERE partner = 'Italy'
  AND CAST(hs2_code AS INTEGER) BETWEEN 61 AND 64
  AND year BETWEEN 2015 AND 2024
GROUP BY year, hs2_code, hs2_description
ORDER BY hs2_code, year;
