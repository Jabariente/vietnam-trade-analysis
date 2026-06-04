# Methodology

## Data Collection

All trade flow data was sourced from UN Comtrade Plus (comtradeplus.un.org) using Vietnam (VNM) as the reporter country. Data was downloaded at the HS 2-digit level for the years 2015–2024, with Japan (JPN), the Netherlands (NLD), and Italy (ITA) as partner countries.

Macroeconomic context data (GDP, trade openness, tariff rates) was sourced from the World Bank Open Data portal. EU-level trade flows were cross-checked against Eurostat Comext.

## Data Cleaning Steps

1. **Standardised column names** — renamed all headers to snake_case (e.g. `reporter_code`, `partner_code`, `trade_value_usd`, `hs2_code`, `year`)
2. **Removed null rows** — dropped rows where `trade_value_usd` was blank or zero
3. **Unified currency** — all values in USD; World Bank conversion rates applied where source used EUR
4. **Added derived columns:**
   - `yoy_growth` — year-on-year % change in trade value
   - `share_of_total` — each HS category as % of total exports to that partner in that year
5. **Merged files** — combined three country files into a single `clean_combined.csv` for comparative queries, with a `partner` column as the country identifier

## Limitations

- **HS 2-digit level only:** Unit price analysis is not possible at this level of aggregation. CEPII BACI data (HS 6-digit) would be needed to test value-chain upgrading directly.
- **Reporter vs. mirror data:** Some discrepancies exist between Vietnam-reported and partner-reported figures. This analysis uses Vietnam as reporter throughout for consistency.
- **EVFTA measurement:** The EVFTA came into force August 1, 2020. The 2020 annual figure therefore includes 7 months pre-EVFTA. The before/after split treats 2015–2019 as pre-EVFTA and 2021–2024 as post-EVFTA to avoid the partial year.
- **Causality:** Trade volume changes post-EVFTA cannot be attributed solely to the agreement. COVID-19 (2020–2021), global supply chain disruptions, and Vietnam's broader export growth all coincide with this period.

## What I Would Study Next

If I had access to HS 6-digit data and unit price records, I would test whether Vietnam's exports to Japan and Italy are increasing in unit value over time — a direct proxy for value-chain upgrading. I would also isolate the EVFTA tariff schedule to quantify which specific HS categories received the largest preferential margin and whether export growth in those categories is statistically correlated with the tariff change.
