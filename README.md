# Vietnam Export Dynamics: Japan, Netherlands & Italy (2015–2024)

> A 10-year bilateral trade analysis examining how Vietnam's export relationships with three key partners have evolved — and what the data reveals about Vietnam's value-chain position in each relationship.

---

## Research Question

**How have Vietnam's export relationships with Japan, the Netherlands, and Italy evolved between 2015 and 2024 — and what does the data reveal about Vietnam's value-chain position in each bilateral relationship?**

**Sub-questions:**
- **Japan:** Vietnam exports high volume but captures small value share — which sectors show the highest upside?
- **Netherlands:** How did EVFTA (August 2020) change Vietnam's export composition to the EU gateway?
- **Italy:** Where does Vietnam sit in Italy's premium manufacturing supply chains?

---

## Three-Country Framework

| Country | Role | Key Angle |
|---------|------|-----------|
| 🇯🇵 Japan | Asia-Pacific anchor | Electronics value chain, CPTPP tariff flows, FDI nexus |
| 🇳🇱 Netherlands | EU gateway | Rotterdam port, EVFTA before/after, largest EU partner (24.56% share) |
| 🇮🇹 Italy | EU contrast case | Supply-chain reversal: Italy sends leather → Vietnam ships back finished footwear |

---

## Key Findings

> ⚠️ *This section will be updated after SQL analysis is complete (Week 6).*

- **Japan:** TBD
- **Netherlands:** TBD
- **Italy:** TBD
- **Overall:** TBD

---

## Dashboard Preview

> ⚠️ *Screenshot to be added after Power BI dashboard is complete (Week 8).*

---

## Methodology

### Data Sources

| Source | What It Provides | URL |
|--------|-----------------|-----|
| UN Comtrade | Bilateral trade flows by HS product code, 2015–2024 | [comtradeplus.un.org](https://comtradeplus.un.org) |
| World Bank Open Data | GDP, trade as % of GDP, tariff data | [data.worldbank.org](https://data.worldbank.org) |
| Vietnam GSO | Vietnam-side export statistics | [gso.gov.vn/en](https://www.gso.gov.vn/en) |
| Eurostat Comext | EU–Vietnam trade flows 2014–2024 | [ec.europa.eu/eurostat](https://ec.europa.eu/eurostat) |
| IMF DOTS | Direction of Trade Statistics (cross-check) | [imf.org/en/Data](https://www.imf.org/en/Data) |

### Tools

| Layer | Tool |
|-------|------|
| Data cleaning | Microsoft Excel |
| Data analysis | SQLite + DB Browser for SQLite |
| Visualisation | Power BI Desktop |
| Portfolio | GitHub |
| Business memo | Google Docs → PDF |

### Process
1. Raw CSVs downloaded from UN Comtrade (HS 2-digit level, Vietnam as reporter)
2. Cleaned in Excel — standardised column names, removed blanks, added YoY growth columns
3. Imported into SQLite — 15 queries written to answer the research question
4. Power BI dashboard built from query outputs — 5 tabs with country and year slicers
5. 1-page business memo written summarising key findings and implications

See [`docs/methodology.md`](docs/methodology.md) for full data cleaning steps and limitations.

---

## Repository Structure

```
vietnam-trade-analysis/
│
├── README.md                     ← You are here
├── docs/
│   ├── methodology.md            ← Data sources, cleaning steps, limitations
│   └── masterplan.md             ← Project planning document
│
├── data/
│   ├── raw/                      ← Original CSV downloads — do not edit
│   │   ├── raw_VNM_JPN_2015_2024.csv
│   │   ├── raw_VNM_NLD_2015_2024.csv
│   │   ├── raw_VNM_ITA_2015_2024.csv
│   │   ├── raw_WB_VNM_GDP.csv
│   │   ├── raw_WB_VNM_tariffs.csv
│   │   └── raw_Eurostat_VNM_2014_2024.csv
│   │
│   └── cleaned/                  ← Excel-cleaned files ready for SQLite
│       ├── clean_VNM_JPN.csv
│       ├── clean_VNM_NLD.csv
│       ├── clean_VNM_ITA.csv
│       └── clean_WB_indicators.csv
│
├── data/queries/                 ← All 15 SQL query files
│   ├── 01_overview_total_exports.sql
│   ├── 02_overview_yoy_growth.sql
│   ├── 03_overview_vietnam_share.sql
│   ├── 04_japan_top_categories.sql
│   ├── 05_japan_cagr_categories.sql
│   ├── 06_japan_unit_value_trend.sql
│   ├── 07_nl_evfta_before_after.sql
│   ├── 08_nl_evfta_category_uplift.sql
│   ├── 09_nl_eu_gateway_share.sql
│   ├── 10_italy_categories_all_years.sql
│   ├── 11_italy_textiles_footwear.sql
│   ├── 12_italy_eu_share.sql
│   ├── 13_comparative_top_categories.sql
│   ├── 14_comparative_structural_shift.sql
│   └── 15_synthesis_primary_question.sql
│
├── dashboard/
│   └── vietnam_trade.pbix        ← Power BI file (add after Week 8)
│
└── memo/
    └── business_memo.pdf         ← 1-page insight document (add after Week 8)
```

---

## How to Use This Repository

**To view the SQL queries:** Open any `.sql` file in the `data/queries/` folder in any text editor.

**To run the analysis yourself:**
1. Install [DB Browser for SQLite](https://sqlitebrowser.org) (free)
2. Import the cleaned CSV files from `data/cleaned/`
3. Run the `.sql` files in order (01 → 15)

**To open the dashboard:**
1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Open `dashboard/vietnam_trade.pbix`

---

## About

Built as a personal research project for college applications (2026–2027 intake).

**Author:** [Your Name] | Grade 11 | Hanoi, Vietnam
**Contact:** [Your email or LinkedIn — optional]
**Status:** 🟡 In progress — target completion August 1, 2026
