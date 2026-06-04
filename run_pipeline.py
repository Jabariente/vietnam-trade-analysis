"""
run_pipeline.py
===============
ONE COMMAND to run the entire Vietnam Trade Analysis pipeline.

Usage:  python run_pipeline.py
        python run_pipeline.py --skip-collect   (if data already downloaded)
        python run_pipeline.py --only-analysis  (skip collect + clean)

Steps:
  1. Collect  — pulls data from UN Comtrade, World Bank, Eurostat APIs
  2. Clean    — standardises, enriches, and validates all raw CSVs
  3. Analyse  — runs all 15 SQL queries, saves results to data/results/
"""

import subprocess
import sys
import os
from datetime import datetime

BASE    = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(BASE, "scripts")

def run_step(script_name, label):
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"{'='*60}")
    path = os.path.join(SCRIPTS, script_name)
    result = subprocess.run([sys.executable, path], cwd=BASE)
    if result.returncode != 0:
        print(f"\n  ✗ {label} failed. Check logs and retry.")
        sys.exit(1)
    print(f"\n  ✓ {label} complete.")

def main():
    args = sys.argv[1:]
    print("\n" + "="*60)
    print("  🇻🇳  VIETNAM TRADE ANALYSIS — Full Pipeline")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    if "--only-analysis" in args:
        run_step("03_run_analysis.py", "SQL Analysis (15 queries)")
    elif "--skip-collect" in args:
        run_step("02_clean_data.py",   "Data Cleaning")
        run_step("03_run_analysis.py", "SQL Analysis (15 queries)")
    else:
        run_step("01_collect_data.py", "Data Collection (APIs)")
        run_step("02_clean_data.py",   "Data Cleaning")
        run_step("03_run_analysis.py", "SQL Analysis (15 queries)")

    print("\n" + "="*60)
    print("  ✅  PIPELINE COMPLETE")
    print("  Results saved to: data/results/")
    print("  Next: open Power BI Desktop → import data/results/*.csv")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
