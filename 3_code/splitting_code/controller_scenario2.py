#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller για Thessaloniki Air Quality Workflow (Scenario 2)

- Κρατάει όλα τα CONFIG (paths, σταθμούς, όρια ρύπων)
- Καλεί τα processes με τη σειρά
- Γράφει όλα τα outputs στον φάκελο 4_Outputs
"""

from pathlib import Path
import pandas as pd


# Πλέον πάμε δύο επίπεδα πάνω: splitting_code -> 3_code -> ROOT
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "2_data"
OUTPUT_DIR = ROOT_DIR / "4_Outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Φύλλα Excel με σταθμούς μέτρησης
STATION_SHEETS = [
    "Στ. ΕΓΝΑΤΙΑΣ", "Στ. 25ης ΜΑΡΤΙΟΥ", "Στ. ΛΑΓΚΑΔΑ",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ", "Στ. ΜΑΛΑΚΟΠΗΣ", "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ"
]

# Mapping σταθμών -> διοικητικά διαμερίσματα
STATION_TO_AREA_ADMIN = {
    "Στ. ΕΓΝΑΤΙΑΣ": "1ο Διαμέρισμα",
    "Στ. ΛΑΓΚΑΔΑ": "2ο Διαμέρισμα",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ": "3ο Διαμέρισμα",
    "Στ. 25ης ΜΑΡΤΙΟΥ": "4ο Διαμέρισμα",
    "Στ. ΜΑΛΑΚΟΠΗΣ": "4ο Διαμέρισμα",
    "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ": "5ο Διαμέρισμα"
}

# Όρια ρύπων (ΕΕ/Οδηγίες)
LIMITS = {
    "SO2": 125,
    "NO2": 40,
    "NO": 100,
    "O3": 120,
    "PM10": 40,
    "PM2.5": 25,
    "CO": 10
}

# Αρχεία εισόδου/εξόδου
POLLUTION_XLSX = DATA_DIR / "metriseis_atmosfairikis_rypansis_dimotikoy_diktyoy_2010_2013.xlsx"
POPULATION_XLSX = DATA_DIR / "resident_population_census2011-extended thessaloniki.xlsx"
OUTPUT_EXCEL = OUTPUT_DIR / "atmospheric_analysis_thessaloniki.xlsx"


# ---------------- IMPORT PROCESSES ---------------- #

from aggregate_and_compute_mean_pollutant_levels import (
    aggregate_and_compute_mean_pollutant_levels,
)
from clean_and_normalize_demographic_data import (
    clean_and_normalize_demographic_data,
)
from merge_and_compute_per_capita import merge_and_compute_per_capita
from assess_compliance_with_eu_limits import assess_compliance_with_eu_limits
from generate_graphs_and_visual_summaries import (
    generate_graphs_and_visual_summaries,
)
from export_excel import export_excel


# ---------------- CONTROLLER LOGIC ---------------- #

def main():
    print("📂 Paths εισόδου / εξόδου:")
    print(f"  Ρύπανση:      {POLLUTION_XLSX}")
    print(f"  Πληθυσμός:    {POPULATION_XLSX}")
    print(f"  Output dir:   {OUTPUT_DIR}")
    print(f"  Output Excel: {OUTPUT_EXCEL}")

    # --- Process #1: Environmental (Aggregate & Mean) ---
    print("\n▶ Process #1 – aggregate_and_compute_mean_pollutant_levels")
    env_means = aggregate_and_compute_mean_pollutant_levels(
        POLLUTION_XLSX,
        STATION_SHEETS
    )

    # --- Process #2: Demographic (Clean & Normalize) ---
    print("\n▶ Process #2 – clean_and_normalize_demographic_data")
    demo_clean = clean_and_normalize_demographic_data(POPULATION_XLSX)

    # --- Process #3: Merge & Per-Capita ---
    print("\n▶ Process #3 – merge_and_compute_per_capita")
    merged_per_capita = merge_and_compute_per_capita(
        env_means,
        demo_clean,
        STATION_TO_AREA_ADMIN
    )

    # --- Process #4: Assess Compliance with EU limits ---
    print("\n▶ Process #4 – assess_compliance_with_eu_limits")
    assessed = assess_compliance_with_eu_limits(merged_per_capita, LIMITS)

    # --- Export Excel ---
    print("\n▶ Export – export_excel")
    mapping_df = pd.DataFrame({
        "Σταθμός": list(STATION_TO_AREA_ADMIN.keys()),
        "Δημοτική Κοινότητα": list(STATION_TO_AREA_ADMIN.values()),
    })
    export_excel(mapping_df, assessed, OUTPUT_EXCEL)

    # --- Process #5: Visuals ---
    print("\n▶ Process #5 – generate_graphs_and_visual_summaries")
    generate_graphs_and_visual_summaries(assessed, OUTPUT_DIR, LIMITS)

    print(f"\n✅ Ολοκληρώθηκε. Δες αποτελέσματα στον φάκελο: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
