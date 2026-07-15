-- Query 06: Unit value trend for top 5 categories exported to Japan
-- PURPOSE:  Is Vietnam capturing more value per kg (moving up value chain)?
-- NOTE:     Requires net_weight_kg column. If absent, use value index (value/2015_value).
SELECT
    year, hs2_code, hs2_description,
    ROUND(SUM(trade_value_usd) / 1e6, 1)            AS value_million,
    ROUND(SUM(trade_value_usd)
          / NULLIF(SUM(net_weight_kg), 0), 4)       AS unit_value_usd_per_kg
FROM clean_combined
WHERE partner = 'Japan'
  AND hs2_code IN (
      SELECT hs2_code FROM clean_combined
      WHERE partner = 'Japan' AND year = 2024
      GROUP BY hs2_code ORDER BY SUM(trade_value_usd) DESC LIMIT 5
  )
  AND year BETWEEN 2015 AND 2024
GROUP BY year, hs2_code, hs2_description
ORDER BY hs2_code, year;
