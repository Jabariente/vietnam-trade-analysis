"""
03_run_analysis.py
==================
Loads cleaned CSVs into an in-memory SQLite database and runs all 15 queries.
Saves each query result as a CSV in data/results/ for Power BI import.

Run:    python scripts/03_run_analysis.py
Input:  data/cleaned/*.csv
Output: data/results/q01_*.csv … q15_*.csv  +  results_summary.md
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED = os.path.join(BASE, "data", "cleaned")
QUERIES = os.path.join(BASE, "data", "queries")
RESULTS = os.path.join(BASE, "data", "results")
os.makedirs(RESULTS, exist_ok=True)

LOG = []
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG.append(line)

# ─────────────────────────────────────────────────────────────────────────────
# Load cleaned data into SQLite
# ─────────────────────────────────────────────────────────────────────────────
def build_database():
    log("Building SQLite database from cleaned CSVs...")
    conn = sqlite3.connect(":memory:")   # in-memory, no file needed

    # Main trade table
    trade_path = os.path.join(CLEANED, "clean_combined.csv")
    if os.path.exists(trade_path):
        df = pd.read_csv(trade_path)
        df.to_sql("clean_combined", conn, if_exists="replace", index=False)
        log(f"  ✓ clean_combined: {len(df)} rows loaded")
    else:
        log("  ✗ clean_combined.csv not found — run 01 and 02 first")
        return None

    # Eurostat totals (used in queries 09, 12)
    eu_path = os.path.join(CLEANED, "clean_eurostat_eu_vnm_totals.csv")
    if os.path.exists(eu_path):
        df_eu = pd.read_csv(eu_path)
        df_eu.to_sql("eurostat_vnm_totals", conn, if_exists="replace", index=False)
        log(f"  ✓ eurostat_vnm_totals: {len(df_eu)} rows loaded")

    # World Bank indicators
    wb_path = os.path.join(CLEANED, "clean_wb_indicators.csv")
    if os.path.exists(wb_path):
        df_wb = pd.read_csv(wb_path)
        df_wb.to_sql("wb_indicators", conn, if_exists="replace", index=False)
        log(f"  ✓ wb_indicators: {len(df_wb)} rows loaded")

    # Partner total imports proxy (build from WB merchandise exports, inverted)
    # This is a simplified proxy — refine with WITS data if available
    try:
        partner_imports_sql = """
            SELECT country AS partner, year,
                   value AS total_imports
            FROM wb_indicators
            WHERE label = 'merchandise_exports_usd'
              AND country IN ('JPN','NLD','ITA')
        """
        df_pi = pd.read_sql(partner_imports_sql, conn)
        country_map = {"JPN": "Japan", "NLD": "Netherlands", "ITA": "Italy"}
        df_pi["partner"] = df_pi["partner"].map(country_map)
        df_pi.to_sql("partner_total_imports", conn, if_exists="replace", index=False)
        log(f"  ✓ partner_total_imports proxy: {len(df_pi)} rows")
    except Exception as e:
        log(f"  ! partner_total_imports skipped: {e}")

    return conn

# ─────────────────────────────────────────────────────────────────────────────
# All 15 queries — defined inline for robustness
# (mirrors the .sql files but runs directly in Python)
# ─────────────────────────────────────────────────────────────────────────────
QUERIES_DEF = [

    ("01_overview_total_exports",
     """
     SELECT year, partner,
            SUM(trade_value_usd)               AS total_exports_usd,
            ROUND(SUM(trade_value_usd)/1e9,3)  AS total_exports_billion
     FROM clean_combined
     WHERE year BETWEEN 2015 AND 2024
     GROUP BY year, partner
     ORDER BY partner, year
     """),

    ("02_overview_yoy_growth",
     """
     WITH y AS (
         SELECT year, partner, SUM(trade_value_usd) AS total
         FROM clean_combined WHERE year BETWEEN 2015 AND 2024
         GROUP BY year, partner
     )
     SELECT c.year, c.partner,
            ROUND(c.total/1e9,3) AS exports_billion,
            ROUND((c.total-p.total)*100.0/NULLIF(p.total,0),2) AS yoy_growth_pct
     FROM y c LEFT JOIN y p ON c.partner=p.partner AND c.year=p.year+1
     ORDER BY c.partner, c.year
     """),

    ("03_overview_vietnam_share",
     """
     SELECT v.year, v.partner,
            ROUND(v.vnm/1e9,3) AS vietnam_exports_billion,
            ROUND(p.total_imports/1e9,3) AS partner_total_imports_billion,
            ROUND(v.vnm*100.0/NULLIF(p.total_imports,0),3) AS vietnam_share_pct
     FROM (SELECT year,partner,SUM(trade_value_usd) AS vnm
           FROM clean_combined GROUP BY year,partner) v
     JOIN partner_total_imports p ON v.year=p.year AND v.partner=p.partner
     ORDER BY v.partner, v.year
     """),

    ("04_japan_top_categories_2024",
     """
     SELECT hs2_code, hs2_description,
            ROUND(SUM(trade_value_usd)/1e9,3) AS value_billion,
            ROUND(SUM(trade_value_usd)*100.0/SUM(SUM(trade_value_usd)) OVER(),2) AS share_pct
     FROM clean_combined
     WHERE partner='Japan' AND year=2024
     GROUP BY hs2_code, hs2_description
     ORDER BY value_billion DESC LIMIT 10
     """),

    ("05_japan_cagr_categories",
     """
     WITH e AS (
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
     HAVING cagr_pct>10 ORDER BY cagr_pct DESC
     """),

    ("06_japan_unit_value_trend",
     """
     SELECT year, hs2_code, hs2_description,
            ROUND(SUM(trade_value_usd)/1e6,1) AS value_million,
            ROUND(SUM(trade_value_usd)/NULLIF(SUM(net_weight_kg),0),4) AS unit_value_usd_per_kg
     FROM clean_combined
     WHERE partner='Japan'
       AND hs2_code IN (
           SELECT hs2_code FROM clean_combined
           WHERE partner='Japan' AND year=2024
           GROUP BY hs2_code ORDER BY SUM(trade_value_usd) DESC LIMIT 5
       )
       AND year BETWEEN 2015 AND 2024
     GROUP BY year, hs2_code, hs2_description
     ORDER BY hs2_code, year
     """),

    ("07_nl_evfta_before_after",
     """
     SELECT hs2_code, hs2_description,
            ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END)/1e6,1)
                AS avg_pre_evfta_million,
            ROUND(AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END)/1e6,1)
                AS avg_post_evfta_million,
            ROUND(
                (AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END)
                -AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END))*100.0
                /NULLIF(AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END),0)
            ,2) AS change_pct
     FROM clean_combined WHERE partner='Netherlands'
     GROUP BY hs2_code, hs2_description
     ORDER BY change_pct DESC
     """),

    ("08_nl_evfta_category_uplift",
     """
     WITH pa AS (
         SELECT hs2_code, hs2_description,
                AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN trade_value_usd END) AS pre,
                AVG(CASE WHEN year BETWEEN 2021 AND 2024 THEN trade_value_usd END) AS post
         FROM clean_combined WHERE partner='Netherlands'
         GROUP BY hs2_code, hs2_description
     )
     SELECT hs2_code, hs2_description,
            ROUND(pre/1e6,1) AS pre_evfta_million,
            ROUND(post/1e6,1) AS post_evfta_million,
            ROUND((post-pre)/1e6,1) AS uplift_million
     FROM pa WHERE pre IS NOT NULL AND post IS NOT NULL
     ORDER BY uplift_million DESC LIMIT 10
     """),

    ("09_nl_eu_gateway_share",
     """
     WITH nl AS (
         SELECT year, SUM(trade_value_usd) AS nl_exports
         FROM clean_combined WHERE partner='Netherlands' GROUP BY year
     )
     SELECT nl.year,
            ROUND(nl.nl_exports/1e9,2) AS nl_exports_billion,
            ROUND(e.total_eu_imports_usd/1e9,2) AS eu_total_billion,
            ROUND(nl.nl_exports*100.0/NULLIF(e.total_eu_imports_usd,0),2) AS nl_share_of_eu_pct
     FROM nl JOIN eurostat_vnm_totals e ON nl.year=e.year
     ORDER BY nl.year
     """),

    ("10_italy_categories_all_years",
     """
     SELECT year, hs2_code, hs2_description,
            ROUND(SUM(trade_value_usd)/1e6,1) AS value_million
     FROM clean_combined
     WHERE partner='Italy' AND year BETWEEN 2015 AND 2024
     GROUP BY year, hs2_code, hs2_description
     ORDER BY year, value_million DESC
     """),

    ("11_italy_textiles_footwear",
     """
     SELECT year, hs2_code, hs2_description,
            ROUND(SUM(trade_value_usd)/1e6,1) AS value_million
     FROM clean_combined
     WHERE partner='Italy'
       AND CAST(hs2_code AS INTEGER) BETWEEN 61 AND 64
       AND year BETWEEN 2015 AND 2024
     GROUP BY year, hs2_code, hs2_description
     ORDER BY hs2_code, year
     """),

    ("12_italy_eu_share",
     """
     WITH it AS (
         SELECT year, SUM(trade_value_usd) AS italy_exports
         FROM clean_combined WHERE partner='Italy' GROUP BY year
     )
     SELECT it.year,
            ROUND(it.italy_exports/1e9,2) AS italy_billion,
            ROUND(e.total_eu_imports_usd/1e9,2) AS eu_total_billion,
            ROUND(it.italy_exports*100.0/NULLIF(e.total_eu_imports_usd,0),2) AS italy_share_pct
     FROM it JOIN eurostat_vnm_totals e ON it.year=e.year
     ORDER BY it.year
     """),

    ("13_comparative_top_categories",
     """
     WITH ranked AS (
         SELECT year, partner, hs2_code, hs2_description,
                SUM(trade_value_usd) AS total_usd,
                RANK() OVER (PARTITION BY year,partner ORDER BY SUM(trade_value_usd) DESC) AS rnk
         FROM clean_combined WHERE year IN (2015,2024)
         GROUP BY year, partner, hs2_code, hs2_description
     )
     SELECT partner, year, rnk, hs2_code, hs2_description,
            ROUND(total_usd/1e9,3) AS value_billion
     FROM ranked WHERE rnk<=3
     ORDER BY partner, year, rnk
     """),

    ("14_comparative_structural_shift",
     """
     WITH shares AS (
         SELECT year, partner, hs2_code, hs2_description,
                SUM(trade_value_usd)*100.0
                /SUM(SUM(trade_value_usd)) OVER (PARTITION BY year,partner) AS share_pct
         FROM clean_combined WHERE year IN (2015,2024)
         GROUP BY year, partner, hs2_code, hs2_description
     ),
     pivot AS (
         SELECT partner, hs2_code, hs2_description,
                MAX(CASE WHEN year=2015 THEN share_pct END) AS share_2015,
                MAX(CASE WHEN year=2024 THEN share_pct END) AS share_2024
         FROM shares GROUP BY partner, hs2_code, hs2_description
     )
     SELECT partner, hs2_code, hs2_description,
            ROUND(share_2015,2) AS share_2015_pct,
            ROUND(share_2024,2) AS share_2024_pct,
            ROUND(share_2024-share_2015,2) AS share_change_ppt
     FROM pivot WHERE share_2015 IS NOT NULL AND share_2024 IS NOT NULL
     ORDER BY partner, ABS(share_2024-share_2015) DESC
     """),

    ("15_synthesis_primary_question",
     """
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
                    RANK() OVER (PARTITION BY partner ORDER BY SUM(trade_value_usd) DESC) AS rnk
             FROM clean_combined WHERE year=2024
             GROUP BY partner, hs2_description
         ) WHERE rnk=1
     ),
     top_share AS (
         SELECT partner, ROUND(MAX(share_pct),1) AS top_cat_share_pct
         FROM (
             SELECT partner,
                    SUM(trade_value_usd)*100.0
                    /SUM(SUM(trade_value_usd)) OVER (PARTITION BY partner) AS share_pct
             FROM clean_combined WHERE year=2024
             GROUP BY partner, hs2_code
         ) GROUP BY partner
     )
     SELECT t.partner,
            ROUND(t.v2015/1e9,2) AS exports_2015_billion,
            ROUND(t.v2024/1e9,2) AS exports_2024_billion,
            ROUND((POWER(CAST(t.v2024 AS FLOAT)/NULLIF(t.v2015,0),1.0/9)-1)*100,2) AS cagr_pct,
            c.top_category,
            s.top_cat_share_pct
     FROM totals t
     JOIN top_cat c   ON t.partner=c.partner
     JOIN top_share s ON t.partner=s.partner
     ORDER BY t.v2024 DESC
     """),
]

# ─────────────────────────────────────────────────────────────────────────────
# Run all queries and save results
# ─────────────────────────────────────────────────────────────────────────────
def run_all_queries(conn):
    log("\n" + "─"*55)
    log("  Running all 15 SQL queries...")
    log("─"*55)
    summary = []

    for name, sql in QUERIES_DEF:
        try:
            df = pd.read_sql_query(sql.strip(), conn)
            out = os.path.join(RESULTS, f"{name}.csv")
            df.to_csv(out, index=False)
            log(f"  ✓ {name}: {len(df)} rows")
            summary.append({"query": name, "rows": len(df), "status": "OK"})
        except Exception as e:
            log(f"  ✗ {name}: {e}")
            summary.append({"query": name, "rows": 0, "status": str(e)})

    return summary

# ─────────────────────────────────────────────────────────────────────────────
# Generate results summary markdown (goes in docs/)
# ─────────────────────────────────────────────────────────────────────────────
def write_summary_md(summary):
    lines = [
        "# Analysis Results Summary",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n## Query Results\n",
        "| Query | Rows | Status |",
        "|-------|------|--------|",
    ]
    for s in summary:
        lines.append(f"| {s['query']} | {s['rows']} | {s['status']} |")

    lines += [
        "\n## Key Findings\n",
        "> Fill in after reviewing query results — especially Q15 (synthesis).\n",
        "- **Japan:** TBD after Q04–Q06",
        "- **Netherlands:** TBD after Q07–Q09",
        "- **Italy:** TBD after Q10–Q12",
        "- **Overall structural shift:** TBD after Q14–Q15",
        "\n## Next Step\n",
        "Import the CSVs from `data/results/` into Power BI Desktop.",
        "Build the 5-tab dashboard following the plan in `docs/masterplan.md`.",
    ]

    path = os.path.join(BASE, "docs", "results_summary.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    log(f"\n  ✓ Results summary saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    log("="*55)
    log("  Vietnam Trade Analysis — SQL Analysis Pipeline")
    log(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("="*55)

    conn = build_database()
    if conn is None:
        log("  Aborting — database could not be built.")
        return

    summary = run_all_queries(conn)
    write_summary_md(summary)
    conn.close()

    ok    = sum(1 for s in summary if s["status"] == "OK")
    failed = len(summary) - ok

    log("\n" + "="*55)
    log(f"  ANALYSIS COMPLETE — {ok}/15 queries successful, {failed} failed")
    log("  Results in: data/results/")
    log("  Next: open Power BI Desktop → import from data/results/")
    log("="*55)

    with open(os.path.join(RESULTS, "analysis_log.txt"), "w") as f:
        f.write("\n".join(LOG))

if __name__ == "__main__":
    main()
