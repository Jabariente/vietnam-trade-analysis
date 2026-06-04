-- Query 03: Vietnam's share of each partner country's total imports, by year
-- PURPOSE:  How important is Vietnam as a supplier — and is that share growing?
-- NOTE:     Requires partner_total_imports table (World Bank WITS data).
SELECT
    v.year, v.partner,
    ROUND(v.vnm_exports / 1e9, 3)                       AS vietnam_exports_billion,
    ROUND(p.total_imports / 1e9, 3)                     AS partner_total_imports_billion,
    ROUND(v.vnm_exports * 100.0 / NULLIF(p.total_imports, 0), 3) AS vietnam_share_pct
FROM (
    SELECT year, partner, SUM(trade_value_usd) AS vnm_exports
    FROM clean_combined GROUP BY year, partner
) v
JOIN partner_total_imports p ON v.year = p.year AND v.partner = p.partner
ORDER BY v.partner, v.year;
