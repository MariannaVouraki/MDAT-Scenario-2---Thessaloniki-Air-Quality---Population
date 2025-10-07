#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full pipeline for Thessaloniki air-quality workflow (Scenario 2)

Παράγει:
1. Mapping σταθμών–δημοτικών κοινοτήτων
2. Μέσους όρους ανά έτος και συνολικά (2010–2013)
3. Υπολογισμό ρύπων ανά κάτοικο (μόνο για συνολικό μέσο)
4. Έλεγχο υπέρβασης ΠΟΥ/ΕΕ
5. Excel + Γραφήματα ανά ρύπο και ανά κάτοικο

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

# ---------------- ΣΥΝΑΡΤΗΣΕΙΣ ---------------- #
def normalize_columns(df):
    colmap = {}
    for c in df.columns:
        c_clean = str(c).replace("\n", " ").strip()
        c_clean = c_clean.replace("Ημερο -", "Ημερο-").replace("PM2,5", "PM2.5")
        colmap[c] = c_clean
    return df.rename(columns=colmap)


def read_population(pop_path):
    pop_raw = pd.read_excel(pop_path)
    pop = normalize_columns(pop_raw)

    name_col = next((c for c in pop.columns if "Unnamed: 3" in c), None)
    pop_col = next((c for c in pop.columns if "Unnamed: 4" in c), None)

    pop = pop[[name_col, pop_col]].dropna()
    pop = pop[pop[name_col].astype(str).str.startswith("Δημοτική Κοινότητα")]
    pop = pop.rename(columns={name_col: "Δημοτική Κοινότητα", pop_col: "Πληθυσμός"})
    pop["Πληθυσμός"] = pd.to_numeric(pop["Πληθυσμός"], errors="coerce").astype("Int64")

    # ✅ Καθαρισμός ονόματος: κρατάμε μόνο “4ο Διαμέρισμα”
    pop["Δημοτική Κοινότητα"] = (
        pop["Δημοτική Κοινότητα"]
        .str.extract(r"(Δημοτική Κοινότητα\s*(\d+)[ου]*)")[1]
        .astype(str)
        .apply(lambda x: f"{x}ο Διαμέρισμα")
    )
    return pop


def read_pollution_sheets(poll_path):
    dfs = []
    for sheet in STATION_SHEETS:
        df = pd.read_excel(poll_path, sheet_name=sheet)
        df = normalize_columns(df)
        df["_sheet"] = sheet
        dfs.append(df)
    return dfs


def compute_yearly_means(dfs):
    all_long = []
    for df in dfs:
        sheet = df["_sheet"].iloc[0]
        date_col = next((c for c in df.columns if "Ημερο" in c), None)
        pollutant_cols = [c for c in df.columns if any(p in c for p in ["SO2", "PM10", "PM2.5", "CO", "NO2", "NO ", "O3"])]
        if not pollutant_cols or date_col is None:
            continue
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["Έτος"] = df[date_col].dt.year
        for col in pollutant_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        long = df.melt(id_vars=["Έτος"], value_vars=pollutant_cols, var_name="Ρύπος_raw", value_name="Τιμή")
        long["Ρύπος"] = long["Ρύπος_raw"].str.replace("μg/m3", "").str.replace("mg/m3", "").str.strip()
        long["Σταθμός"] = sheet
        all_long.append(long)
    long_all = pd.concat(all_long, ignore_index=True)
    long_all["Τιμή"] = pd.to_numeric(long_all["Τιμή"], errors="coerce")
    return long_all.groupby(["Σταθμός", "Έτος", "Ρύπος"], as_index=False)["Τιμή"].mean(numeric_only=True)


def compute_overall_means(dfs):
    records = []
    for df in dfs:
        sheet = df["_sheet"].iloc[0]
        pollutant_cols = [c for c in df.columns if any(p in c for p in ["SO2", "PM10", "PM2.5", "CO", "NO", "O3"])]
        if not pollutant_cols:
            continue
        use = df[pollutant_cols].apply(pd.to_numeric, errors="coerce")
        means = use.mean().reset_index()
        means.columns = ["Ρύπος_raw", "Μέσος Όρος 2010–2013"]
        means["Ρύπος"] = means["Ρύπος_raw"].str.replace("μg/m3", "").str.replace("mg/m3", "").str.strip()
        means["Σταθμός"] = sheet
        records.append(means)
    return pd.concat(records, ignore_index=True)


def check_pollutant_status(row):
    pollutant = row["Ρύπος"]
    value = row["Μέσος Όρος 2010–2013"]
    if pollutant not in LIMITS:
        return "Άγνωστο"
    limit = LIMITS[pollutant]
    return "🔴 Υπέρβαση Ορίων" if value > limit else "🟢 Εντός Ορίων"


# ---- ΓΡΑΦΗΜΑΤΑ ---- #
def plot_pollutant_by_district(df, outdir):
    df = df.dropna(subset=["Μέσος Όρος 2010–2013"])
    pollutants = df["Ρύπος"].unique()
    for pollutant in pollutants:
        sub = df[df["Ρύπος"] == pollutant].copy()
        if sub.empty:
            continue
        sub["Χρώμα"] = sub.apply(lambda r: "red" if "Υπέρβαση" in str(r["Κατάσταση"]) else "green", axis=1)
        plt.figure(figsize=(10,6))
        bars = plt.bar(sub["Δημοτική Κοινότητα"], sub["Μέσος Όρος 2010–2013"], color=sub["Χρώμα"], alpha=0.8)
        for bar, val in zip(bars, sub["Μέσος Όρος 2010–2013"]):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"{val:.1f}", ha="center", va="bottom", fontsize=9)
        if pollutant in LIMITS:
            plt.axhline(LIMITS[pollutant], color="orange", linestyle="--", label=f"Όριο ΠΟΥ/ΕΕ: {LIMITS[pollutant]} {'mg/m³' if pollutant=='CO' else 'μg/m³'}")
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


def plot_pollutant_per_capita(df, outdir):
    df = df.dropna(subset=["Ρύποι ανά κάτοικο"])
    pollutants = df["Ρύπος"].unique()
    for pollutant in pollutants:
        sub = df[df["Ρύπος"] == pollutant].copy()
        if sub.empty:
            continue
        plt.figure(figsize=(10,6))
        plt.bar(sub["Δημοτική Κοινότητα"], sub["Ρύποι ανά κάτοικο"], color="teal", alpha=0.8)
        for bar, val in zip(plt.gca().patches, sub["Ρύποι ανά κάτοικο"]):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.000001,
                     f"{val:.8f}", ha="center", va="bottom", fontsize=8)
        plt.title(f"{pollutant} – Ρύποι ανά Κάτοικο (Μέσος Όρος 2010–2013)")
        plt.ylabel("Αναλογία (μονάδες συγκέντρωσης ανά κάτοικο)")
        plt.xlabel("Δημοτική Κοινότητα")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        save_path = outdir / f"{pollutant}_per_capita.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"👤 Αποθηκεύτηκε γράφημα ανά κάτοικο: {save_path}")


# ---------------- ΚΥΡΙΟ SCRIPT ---------------- #
def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    pollution_path = data_dir / "metriseis_atmosfairikis_rypansis_dimotikoy_diktyoy_2010_2013.xlsx"
    population_path = data_dir / "resident_population_census2011-extended thessaloniki.xlsx"
    outxlsx = output_dir / "atmospheric_analysis_thessaloniki.xlsx"

    print("📂 Χρήση αρχείων:")
    print("Ρύπανση:", pollution_path)
    print("Πληθυσμός:", population_path)
    print("Output:", outxlsx)

    dfs = read_pollution_sheets(pollution_path)
    pop = read_population(population_path)

    # Ετήσιοι μέσοι όροι (μόνο για αναφορά)
    means_yearly = compute_yearly_means(dfs)
    means_yearly["Δημοτική Κοινότητα"] = means_yearly["Σταθμός"].map(STATION_TO_AREA_ADMIN)

    # Συνολικοί μέσοι όροι (2010–2013)
    overall_means = compute_overall_means(dfs)
    overall_means["Δημοτική Κοινότητα"] = overall_means["Σταθμός"].map(STATION_TO_AREA_ADMIN)
    overall_means = overall_means.merge(pop, on="Δημοτική Κοινότητα", how="left")

    # Υπολογισμός ρύπων ανά κάτοικο (μόνο συνολικά)
    overall_means["Ρύποι ανά κάτοικο"] = overall_means["Μέσος Όρος 2010–2013"] / overall_means["Πληθυσμός"]

    # Έλεγχος υπέρβασης ΠΟΥ/ΕΕ
    overall_means["Κατάσταση"] = overall_means.apply(check_pollutant_status, axis=1)

    mapping_df = pd.DataFrame({
        "Σταθμός": list(STATION_TO_AREA_ADMIN.keys()),
        "Δημοτική Κοινότητα": list(STATION_TO_AREA_ADMIN.values())
    })

    # Εξαγωγή Excel
    with pd.ExcelWriter(outxlsx) as writer:
        mapping_df.to_excel(writer, sheet_name="Mapping", index=False)
        means_yearly.rename(columns={"Τιμή": "Μέσος Όρος Ρύπου"}).to_excel(writer, sheet_name="Μέσοι Όροι 2010-2013", index=False)
        overall_means.to_excel(writer, sheet_name="Συνολικοί Μέσοι & Ανά Κάτοικο", index=False)

    # Παραγωγή γραφημάτων
    plot_pollutant_by_district(overall_means, output_dir)
    plot_pollutant_per_capita(overall_means, output_dir)

    print(f"✅ Ολοκληρώθηκε. Αποτελέσματα στον φάκελο: {output_dir}")


if __name__ == "__main__":
    main()
