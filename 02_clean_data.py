"""
02_clean_data.py
================
Cleans and standardises all raw CSVs produced by 01_collect_data.py.
Outputs analysis-ready CSVs to data/cleaned/.

Run:    python scripts/02_clean_data.py
Input:  data/raw/*.csv
Output: data/cleaned/*.csv
"""

import pandas as pd
import os
import json
from datetime import datetime

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW     = os.path.join(BASE, "data", "raw")
CLEANED = os.path.join(BASE, "data", "cleaned")
os.makedirs(CLEANED, exist_ok=True)

LOG = []
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG.append(line)

# HS2 description lookup — standardises descriptions across API responses
HS2_LABELS = {
    "01":"Live animals", "02":"Meat & offal", "03":"Fish & seafood",
    "04":"Dairy & eggs", "06":"Live plants", "07":"Vegetables",
    "08":"Fruit & nuts", "09":"Coffee, tea, spices", "10":"Cereals",
    "16":"Meat/fish preparations", "18":"Cocoa & products",
    "21":"Misc food preparations", "22":"Beverages",
    "27":"Mineral fuels & oils", "28":"Inorganic chemicals",
    "29":"Organic chemicals", "32":"Tanning & dyeing",
    "38":"Misc chemical products", "39":"Plastics",
    "40":"Rubber & articles", "44":"Wood & articles",
    "47":"Pulp of wood", "48":"Paper & paperboard",
    "51":"Wool & animal hair", "52":"Cotton",
    "54":"Man-made filaments", "55":"Man-made staple fibres",
    "57":"Carpets", "60":"Knitted fabrics",
    "61":"Apparel — knit", "62":"Apparel — non-knit",
    "63":"Textile articles", "64":"Footwear",
    "72":"Iron & steel", "73":"Iron/steel articles",
    "74":"Copper & articles", "76":"Aluminium",
    "84":"Machinery & mechanical appliances",
    "85":"Electrical & electronic equipment",
    "87":"Motor vehicles & parts", "90":"Optical & medical instruments",
    "94":"Furniture & bedding", "95":"Toys & games",
    "TOTAL":"All commodities",
}

# ─────────────────────────────────────────────────────────────────────────────
# Clean Comtrade data
# ─────────────────────────────────────────────────────────────────────────────
def clean_comtrade():
    log("\n[1/3]  Cleaning Comtrade data...")
    path = os.path.join(RAW, "raw_comtrade_all_partners.csv")

    if not os.path.exists(path):
        log("  ✗ raw_comtrade_all_partners.csv not found — run 01_collect_data.py first")
        return pd.DataFrame()

    df = pd.read_csv(path)
    log(f"  Raw rows: {len(df)}")

    # Drop rows with missing trade value
    df = df.dropna(subset=["trade_value_usd"])
    df = df[df["trade_value_usd"] > 0]

    # Standardise hs2_code as string, zero-padded to 2 digits
    df["hs2_code"] = df["hs2_code"].astype(str).str.strip().str.zfill(2)

    # Fill in cleaner descriptions where API description is missing/generic
    df["hs2_description"] = df.apply(
        lambda r: HS2_LABELS.get(r["hs2_code"], r["hs2_description"]), axis=1
    )

    # Add year-on-year growth within each partner+hs2 group
    df = df.sort_values(["partner", "hs2_code", "year"])
    df["yoy_growth_pct"] = (
        df.groupby(["partner", "hs2_code"])["trade_value_usd"]
        .pct_change() * 100
    ).round(2)

    # Add share of total exports to that partner in that year
    yearly_totals = (
        df.groupby(["partner", "year"])["trade_value_usd"]
        .sum().reset_index().rename(columns={"trade_value_usd": "year_total"})
    )
    df = df.merge(yearly_totals, on=["partner", "year"])
    df["share_of_total_pct"] = (
        df["trade_value_usd"] / df["year_total"] * 100
    ).round(3)
    df = df.drop(columns=["year_total"])

    # Add billion USD column for readability
    df["trade_value_billion"] = (df["trade_value_usd"] / 1e9).round(4)

    # Reorder columns
    cols = [
        "year", "partner", "hs2_code", "hs2_description",
        "trade_value_usd", "trade_value_billion",
        "share_of_total_pct", "yoy_growth_pct",
        "net_weight_kg", "qty",
        "reporter_code", "partner_code",
    ]
    df = df[[c for c in cols if c in df.columns]]

    out = os.path.join(CLEANED, "clean_combined.csv")
    df.to_csv(out, index=False)
    log(f"  ✓ Clean rows: {len(df)}")
    log(f"  ✓ Partners: {sorted(df['partner'].unique().tolist())}")
    log(f"  ✓ Years: {sorted(df['year'].unique().tolist())}")
    log(f"  ✓ Saved: {out}")
    return df

# ─────────────────────────────────────────────────────────────────────────────
# Clean World Bank data — pivot to wide format
# ─────────────────────────────────────────────────────────────────────────────
def clean_worldbank():
    log("\n[2/3]  Cleaning World Bank data...")
    path = os.path.join(RAW, "raw_worldbank_indicators.csv")

    if not os.path.exists(path):
        log("  ✗ raw_worldbank_indicators.csv not found")
        return pd.DataFrame()

    df = pd.read_csv(path)
    log(f"  Raw rows: {len(df)}")

    # Pivot: one row per country-year, one column per indicator
    df_wide = df.pivot_table(
        index=["country", "year"],
        columns="label",
        values="value",
        aggfunc="first"
    ).reset_index()
    df_wide.columns.name = None
    df_wide.columns = [c.replace(" ", "_") for c in df_wide.columns]

    out = os.path.join(CLEANED, "clean_wb_indicators.csv")
    df_wide.to_csv(out, index=False)
    log(f"  ✓ Clean rows: {len(df_wide)}")
    log(f"  ✓ Saved: {out}")
    return df_wide

# ─────────────────────────────────────────────────────────────────────────────
# Clean Eurostat data
# ─────────────────────────────────────────────────────────────────────────────
def clean_eurostat():
    log("\n[3/3]  Cleaning Eurostat data...")
    path = os.path.join(RAW, "raw_eurostat_eu_vnm_totals.csv")

    if not os.path.exists(path):
        log("  ✗ raw_eurostat_eu_vnm_totals.csv not found")
        return pd.DataFrame()

    df = pd.read_csv(path)
    df = df.dropna(subset=["total_eu_imports_usd"])
    df = df[df["total_eu_imports_usd"] > 0]
    df = df.sort_values("year")
    df["total_eu_imports_billion"] = (df["total_eu_imports_usd"] / 1e9).round(3)

    out = os.path.join(CLEANED, "clean_eurostat_eu_vnm_totals.csv")
    df.to_csv(out, index=False)
    log(f"  ✓ Clean rows: {len(df)}")
    log(f"  ✓ Saved: {out}")
    return df

# ─────────────────────────────────────────────────────────────────────────────
# Quality report
# ─────────────────────────────────────────────────────────────────────────────
def quality_report(df_trade, df_wb, df_eurostat):
    log("\n" + "─"*50)
    log("  DATA QUALITY REPORT")
    log("─"*50)

    if not df_trade.empty:
        for partner in ["Japan", "Netherlands", "Italy"]:
            sub = df_trade[df_trade["partner"] == partner]
            years_found = sorted(sub["year"].unique().tolist())
            missing = [y for y in range(2015, 2025) if y not in years_found]
            log(f"  {partner}:")
            log(f"    Years found:   {years_found}")
            log(f"    Years missing: {missing if missing else 'None'}")
            log(f"    HS2 chapters:  {sub['hs2_code'].nunique()}")
            log(f"    Total rows:    {len(sub)}")

    if not df_wb.empty:
        log(f"\n  World Bank: {len(df_wb)} country-year rows")

    if not df_eurostat.empty:
        log(f"  Eurostat: {len(df_eurostat)} annual EU totals")
        log(f"    Range: {df_eurostat['year'].min()}–{df_eurostat['year'].max()}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    log("="*50)
    log("  Vietnam Trade Analysis — Data Cleaning Pipeline")
    log(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("="*50)

    df_trade    = clean_comtrade()
    df_wb       = clean_worldbank()
    df_eurostat = clean_eurostat()

    quality_report(df_trade, df_wb, df_eurostat)

    log("\n" + "="*50)
    log("  CLEANING COMPLETE")
    log("  Next: python scripts/03_run_analysis.py")
    log("="*50)

    with open(os.path.join(CLEANED, "cleaning_log.txt"), "w") as f:
        f.write("\n".join(LOG))

if __name__ == "__main__":
    main()
