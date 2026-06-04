# Analysis Results Summary

Generated: 2026-06-03 02:06:25

## Query Results

| Query | Rows | Status |
|-------|------|--------|
| 01_overview_total_exports | 30 | OK |
| 02_overview_yoy_growth | 30 | OK |
| 03_overview_vietnam_share | 0 | Execution failed on sql 'SELECT v.year, v.partner,
            ROUND(v.vnm/1e9,3) AS vietnam_exports_billion,
            ROUND(p.total_imports/1e9,3) AS partner_total_imports_billion,
            ROUND(v.vnm*100.0/NULLIF(p.total_imports,0),3) AS vietnam_share_pct
     FROM (SELECT year,partner,SUM(trade_value_usd) AS vnm
           FROM clean_combined GROUP BY year,partner) v
     JOIN partner_total_imports p ON v.year=p.year AND v.partner=p.partner
     ORDER BY v.partner, v.year': no such table: partner_total_imports |
| 04_japan_top_categories_2024 | 10 | OK |
| 05_japan_cagr_categories | 0 | Execution failed on sql 'WITH e AS (
         SELECT hs2_code, hs2_description,
                SUM(CASE WHEN year=2015 THEN trade_value_usd ELSE 0 END) AS v2015,
                SUM(CASE WHEN year=2024 THEN trade_value_usd ELSE 0 END) AS v2024
         FROM clean_combined WHERE partner='Japan'
         GROUP BY hs2_code, hs2_description
     )
     SELECT hs2_code, hs2_description,
            ROUND(v2015/1e6,1) AS value_2015_million,
            ROUND(v2024/1e6,1) AS value_2024_million,
            ROUND((POWER(CAST(v2024 AS FLOAT)/NULLIF(v2015,0),1.0/9)-1)*100,2) AS cagr_pct
     FROM e WHERE v2015>0 AND v2024>0
     HAVING cagr_pct>10 ORDER BY cagr_pct DESC': HAVING clause on a non-aggregate query |
| 06_japan_unit_value_trend | 50 | OK |
| 07_nl_evfta_before_after | 10 | OK |
| 08_nl_evfta_category_uplift | 10 | OK |
| 09_nl_eu_gateway_share | 10 | OK |
| 10_italy_categories_all_years | 100 | OK |
| 11_italy_textiles_footwear | 30 | OK |
| 12_italy_eu_share | 10 | OK |
| 13_comparative_top_categories | 18 | OK |
| 14_comparative_structural_shift | 30 | OK |
| 15_synthesis_primary_question | 3 | OK |

## Key Findings

> Fill in after reviewing query results — especially Q15 (synthesis).

- **Japan:** TBD after Q04–Q06
- **Netherlands:** TBD after Q07–Q09
- **Italy:** TBD after Q10–Q12
- **Overall structural shift:** TBD after Q14–Q15

## Next Step

Import the CSVs from `data/results/` into Power BI Desktop.
Build the 5-tab dashboard following the plan in `docs/masterplan.md`.