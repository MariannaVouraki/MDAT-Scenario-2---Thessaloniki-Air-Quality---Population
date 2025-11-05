#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thessaloniki Air Quality Workflow (Scenario 2) — Modular by Processes
Paths aligned to repo structure:
  2_data/     (inputs)
  3_code/     (this script)
  4_Output/   (outputs)

Απαιτεί:
    pip install pandas matplotlib openpyxl
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- ΡΥΘΜΙΣΕΙΣ ---------------- #
STATION_SHEETS = [
    "Στ. ΕΓΝΑΤΙΑΣ", "Στ. 25ης ΜΑΡΤΙΟΥ", "Στ. ΛΑΓΚΑΔΑ",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ", "Στ. ΜΑΛΑΚΟΠΗΣ", "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ"
]

STATION_TO_AREA_ADMIN = {
    "Στ. ΕΓΝΑΤΙΑΣ": "1ο Διαμέρισμα",
    "Στ. ΛΑΓΚΑΔΑ": "2ο Διαμέρισμα",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ": "3ο Διαμέρισμα",
    "Στ. 25ης ΜΑΡΤΙΟΥ": "4ο Διαμέρισμα",
    "Στ. ΜΑΛΑΚΟΠΗΣ": "4ο Διαμέρισμα",
    "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ": "5ο Διαμέρισμα"
}

LIMITS = {
    "SO2": 125, "NO2": 40, "NO": 100, "O3": 120,
    "PM10": 40, "PM2.5": 25, "CO": 10
}

# ---------------- ΒΟΗΘΗΤΙΚΑ ---------------- #
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    colmap = {}
    for c in df.columns:
        c_clean = str(c).replace("\n", " ").strip()
        c_clean = c_clean.replace("Ημερο -", "Ημερο-").replace("PM2,5", "PM2.5")
        colmap[c] = c_clean
    return df.rename(columns=colmap)

def read_pollution_sheets(pollution_path: Path) -> list[pd.DataFrame]:
    dfs = []
    for sheet in STATION_SHEETS:
        df = pd.read_excel(pollution_path, sheet_name=sheet)
        df = normalize_columns(df)
        df["_sheet"] = sheet
        dfs.append(df)
    return dfs

def compute_overall_means(pollution_dfs: list[pd.DataFrame]) -> pd.DataFrame:
    records = []
    for df in pollution_dfs:
        sheet = df["_sheet"].iloc[0]
        pollutant_cols = [c for c in df.columns if any(p in c for p in ["SO2", "PM10", "PM2.5", "CO", "NO", "O3"])]
        if not pollutant_cols:
            continue
        use = df[pollutant_cols].apply(pd.to_numeric, errors="coerce")
        means = use.mean().reset_index()
        means.columns = ["Ρύπος_raw", "Μέσος Όρος 2010–2013"]
        means["Ρύπος"] = (
            means["Ρύπος_raw"]
            .str.replace("μg/m3", "", regex=False)
            .str.replace("mg/m3", "", regex=False)
            .str.strip()
        )
        means["Σταθμός"] = sheet
        records.append(means)
    return pd.concat(records, ignore_index=True)

def read_population(pop_path: Path) -> pd.DataFrame:
    pop_raw = pd.read_excel(pop_path)
    pop = normalize_columns(pop_raw)
    name_col = next((c for c in pop.columns if "Unnamed: 3" in c), None)
    pop_col  = next((c for c in pop.columns if "Unnamed: 4" in c), None)

    pop = pop[[name_col, pop_col]].dropna()
    pop = pop[pop[name_col].astype(str).str.startswith("Δημοτική Κοινότητα")]
    pop = pop.rename(columns={name_col: "Δημοτική Κοινότητα", pop_col: "Πληθυσμός"})
    pop["Πληθυσμός"] = pd.to_numeric(pop["Πληθυσμός"], errors="coerce").astype("Int64")

    # "Δημοτική Κοινότητα Χο" -> "Χο Διαμέρισμα"
    pop["Δημοτική Κοινότητα"] = (
        pop["Δημοτική Κοινότητα"]
        .str.extract(r"(Δημοτική Κοινότητα\s*(\d+)[ου]*)")[1]
        .astype(str)
        .apply(lambda x: f"{x}ο Διαμέρισμα")
    )
    return pop

def check_pollutant_status(row) -> str:
    pollutant = row["Ρύπος"]
    value = row["Μέσος Όρος 2010–2013"]
    if pollutant not in LIMITS:
        return "Άγνωστο"
    limit = LIMITS[pollutant]
    return "🔴 Υπέρβαση Ορίων" if value > limit else "🟢 Εντός Ορίων"

# ---- ΓΡΑΦΗΜΑΤΑ ---- #
def plot_pollutant_by_district(df: pd.DataFrame, outdir: Path) -> None:
    df = df.dropna(subset=["Μέσος Όρος 2010–2013"])
    pollutants = df["Ρύπος"].unique()
    for pollutant in pollutants:
        sub = df[df["Ρύπος"] == pollutant].copy()
        if sub.empty:
            continue
        sub["Χρώμα"] = sub.apply(
            lambda r: "red" if "Υπέρβαση" in str(r["Κατάσταση"]) else "green", axis=1
        )
        plt.figure(figsize=(10,6))
        bars = plt.bar(
            sub["Δημοτική Κοινότητα"],
            sub["Μέσος Όρος 2010–2013"],
            color=sub["Χρώμα"], alpha=0.8
        )
        for bar, val in zip(bars, sub["Μέσος Όρος 2010–2013"]):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     f"{val:.1f}", ha="center", va="bottom", fontsize=9)
        if pollutant in LIMITS:
            plt.axhline(
                LIMITS[pollutant], color="orange", linestyle="--",
                label=f"Όριο ΕΕ: {LIMITS[pollutant]} {'mg/m³' if pollutant=='CO' else 'μg/m³'}"
            )
        plt.title(f"{pollutant} – Μέσος Όρος 2010–2013 ανά Δημοτική Κοινότητα")
        plt.ylabel("Συγκέντρωση")
        plt.xlabel("Δημοτική Κοινότητα")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        save_path = outdir / f"{pollutant}_by_district.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"📊 Αποθηκεύτηκε γράφημα: {save_path}")

def plot_total_pollution_per_capita(df: pd.DataFrame, outdir: Path) -> None:
    df = df.dropna(subset=["Ρύποι ανά κάτοικο"])
    total_per_district = (
        df.groupby("Δημοτική Κοινότητα", as_index=False)["Ρύποι ανά κάτοικο"].sum()
    )

    plt.figure(figsize=(10,6))
    bars = plt.bar(
        total_per_district["Δημοτική Κοινότητα"],
        total_per_district["Ρύποι ανά κάτοικο"],
        color="royalblue", alpha=0.8
    )
    for bar, val in zip(bars, total_per_district["Ρύποι ανά κάτοικο"]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.00001,
                 f"{val:.6f}", ha="center", va="bottom", fontsize=9)

    plt.title("Συνολικοί Ρύποι Ανά Κάτοικο (2010–2013) ανά Δημοτική Κοινότητα")
    plt.ylabel("Συνολικοί Ρύποι ανά Κάτοικο (μονάδες συγκέντρωσης)")
    plt.xlabel("Δημοτική Κοινότητα")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    save_path = outdir / "Total_Pollutants_per_Capita.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"📊 Αποθηκεύτηκε συνολικό γράφημα: {save_path}")

# ---------------- PROCESSES ---------------- #
def aggregate_and_compute_mean_pollutant_levels(pollution_path: Path) -> pd.DataFrame:
    """Process #1 – Environmental Data (Aggregate & Compute Mean Levels)."""
    pollution_dfs = read_pollution_sheets(pollution_path)
    overall_means = compute_overall_means(pollution_dfs)
    return overall_means

def clean_and_normalize_demographic_data(population_path: Path) -> pd.DataFrame:
    """Process #2 – Demographic Data (Clean & Normalize)."""
    return read_population(population_path)

def merge_and_compute_per_capita(env_df: pd.DataFrame, demo_df: pd.DataFrame) -> pd.DataFrame:
    """Process #3 – Merge & Pollutant-per-Capita."""
    env_df = env_df.copy()
    env_df["Δημοτική Κοινότητα"] = env_df["Σταθμός"].map(STATION_TO_AREA_ADMIN)
    merged = env_df.merge(demo_df, on="Δημοτική Κοινότητα", how="left")
    merged["Ρύποι ανά κάτοικο"] = merged["Μέσος Όρος 2010–2013"] / merged["Πληθυσμός"]
    return merged

def assess_compliance_with_eu_limits(df: pd.DataFrame) -> pd.DataFrame:
    """Process #4 – Assess compliance with EU limits."""
    out = df.copy()
    out["Κατάσταση"] = out.apply(check_pollutant_status, axis=1)
    return out

def generate_graphs_and_visual_summaries(df: pd.DataFrame, output_dir: Path) -> None:
    """Process #5 – Generate graphs and visual summaries."""
    plot_pollutant_by_district(df, output_dir)
    plot_total_pollution_per_capita(df, output_dir)

# ---------------- ΕΞΑΓΩΓΕΣ ---------------- #
def export_excel(mapping_df: pd.DataFrame, results_df: pd.DataFrame, outxlsx: Path) -> None:
    with pd.ExcelWriter(outxlsx) as writer:
        mapping_df.to_excel(writer, sheet_name="Mapping", index=False)
        results_df.to_excel(writer, sheet_name="Συνολικοί Μέσοι & Ανά Κάτοικο", index=False)
    print(f"📄 Αποθήκευση Excel: {outxlsx}")

# ---------------- ΚΥΡΙΟ SCRIPT ---------------- #
def main():
    # === Paths με βάση τη δομή σου ===
    # Αυτό το αρχείο βρίσκεται στο: <root>/3_code/...
    root_dir   = Path(__file__).resolve().parents[1]     # πάει ένα επίπεδο πάνω από το 3_code
    data_dir   = root_dir / "2_data"
    output_dir = root_dir / "4_Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Αρχεία εισόδου όπως τα έχεις ονοματίσει στον φάκελο 2_data
    pollution_path  = data_dir / "metriseis_atmosfairikis_rypansis_dimotikoy_diktyoy_2010_2013.xlsx"
    population_path = data_dir / "resident_population_census2011-extended thessaloniki.xlsx"

    outxlsx = output_dir / "atmospheric_analysis_thessaloniki.xlsx"

    print("📂 Χρήση αρχείων:")
    print("  Ρύπανση:   ", pollution_path)
    print("  Πληθυσμός: ", population_path)
    print("  Output dir:", output_dir)

    # --- Process #1: Environmental (Aggregate & Mean) ---
    env_means = aggregate_and_compute_mean_pollutant_levels(pollution_path)

    # --- Process #2: Demographic (Clean & Normalize) ---
    demo_clean = clean_and_normalize_demographic_data(population_path)

    # --- Process #3: Merge & Per-Capita ---
    merged_per_capita = merge_and_compute_per_capita(env_means, demo_clean)

    # --- Process #4: Assess Compliance with EU limits ---
    assessed = assess_compliance_with_eu_limits(merged_per_capita)

    # Για το Excel χρειάζεται και ο mapping πίνακας:
    mapping_df = pd.DataFrame({
        "Σταθμός": list(STATION_TO_AREA_ADMIN.keys()),
        "Δημοτική Κοινότητα": list(STATION_TO_AREA_ADMIN.values())
    })
    export_excel(mapping_df, assessed, outxlsx)

    # --- Process #5: Generate Graphs & Visual Summaries ---
    generate_graphs_and_visual_summaries(assessed, output_dir)

    print(f"✅ Ολοκληρώθηκε. Δες αποτελέσματα στον φάκελο: {output_dir}")

if __name__ == "__main__":
    main()
