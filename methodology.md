Methodology

Data Sources

UN Comtrade: primary trade flow data. All bilateral export records downloaded at HS 2-digit level using Vietnam (VNM, reporter code 704) as the reporting country. Partner countries: Japan (JPN, 392), Netherlands (NLD, 528), Italy (ITA, 380). Coverage: 2015–2024, ten annual observations per HS2 chapter per partner. Downloaded via the UN Comtrade Plus API (comtradeplus.un.org).

World Bank Open Data: macroeconomic context indicators (GDP, trade openness). Used for contextual reference only; not used in primary trade calculations.

Eurostat Comext: EU-level aggregate trade flows between the EU and Vietnam. Used to calculate the Netherlands' share of total Vietnam-EU export volume (24.56% in 2024). Cross-checked against UN Comtrade figures for consistency.

Pipeline

01_collect_data.py   Pull bilateral trade records from UN Comtrade API
02_clean_data.py     Standardise, filter, derive calculated columns
03_run_analysis.py   Execute 15 SQL queries against clean_combined.csv
run_pipeline.py      Entry point: runs all three scripts in sequence

All intermediate outputs saved as CSV. Final tables loaded into Power BI Desktop for visualisation.

Data Cleaning Steps


Column standardisation — all headers renamed to snake_case (reporter_code, partner_code, trade_value_usd, hs2_code, year)
Null removal — rows where trade_value_usd was blank or zero were dropped
Currency — all values in USD; Eurostat EUR figures converted using World Bank annual average exchange rates
Derived columns added:

yoy_growth_pct — year-on-year percentage change in trade value
share_of_total_pct — each HS2 category as a percentage of total exports to that partner in that year
trade_value_billion — trade_value_usd divided by 1,000,000,000 for display



File merge — three country-level files combined into clean_combined.csv with a partner column as the country identifier


Key Calculations

CAGR formula:

CAGR = (End Value / Start Value) ^ (1 / n) - 1

Where n = number of years between start and end observation.
Applied to USD nominal trade values. No inflation adjustment. All figures in current USD.

Electronics concentration:

Share = HS85 trade value / total bilateral trade value for that partner and year

HS2 code 85 = Electrical and electronic equipment.

Post-EVFTA period definition:

The EVFTA entered force 1 August 2020. The 2020 annual figure therefore includes 7 months pre-EVFTA. The before/after comparison treats 2015–2019 as pre-EVFTA and 2021–2024 as post-EVFTA to avoid the partial year. The 51% growth figure cited in the analysis covers 2020–2024 inclusive.

Limitations

HS 2-digit aggregation only. Unit price analysis is not possible at this level. CEPII BACI data at HS 6-digit would be needed to test value-chain upgrading through unit value trends directly.

Reporter vs mirror data. Discrepancies exist between Vietnam-reported and partner-reported figures. This analysis uses Vietnam as the reporter throughout for internal consistency.

Rotterdam Effect. Netherlands figures reflect port-of-entry registration. Goods clearing Rotterdam customs are recorded as Dutch imports regardless of their final EU destination. The 24.56% share measures Rotterdam's gateway function, not Dutch domestic absorption of Vietnamese goods.

Causality. Trade volume changes post-EVFTA cannot be attributed solely to the agreement. COVID-19 (2020–2021), global supply chain disruptions, and Vietnam's broader export growth all coincide with the post-2020 period.

Italy electronics share. The ~26.7% figure is calculated from HS85 value against total bilateral 2024 exports. Verify against the primary dataset before external citation.
