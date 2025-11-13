import pandas as pd
from pathlib import Path

# ==== embedded helper ====
def normalize_columns(df):
    colmap = {}
    for c in df.columns:
        clean = str(c).replace("\n", " ").strip()
        clean = clean.replace("PM2,5", "PM2.5").replace("Ημερο -", "Ημερο-")
        colmap[c] = clean
    return df.rename(columns=colmap)

STATION_SHEETS = [
    "Στ. ΕΓΝΑΤΙΑΣ", "Στ. 25ης ΜΑΡΤΙΟΥ", "Στ. ΛΑΓΚΑΔΑ",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ", "Στ. ΜΑΛΑΚΟΠΗΣ", "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ"
]

def run_step_1():
    root = Path(__file__).resolve().parents[2]
    data_dir = root / "2_data"
    out_dir = root / "4_Outputs"

    in_file = data_dir / "metriseis_atmosfairikis_rypansis_dimotikoy_diktyoy_2010_2013.xlsx"
    out_file = out_dir / "Step1_env_data.csv"

    dfs = []
    for sheet in STATION_SHEETS:
        df = pd.read_excel(in_file, sheet_name=sheet)
        df = normalize_columns(df)
        df["_sheet"] = sheet
        dfs.append(df)

    final = pd.concat(dfs, ignore_index=True)
    final.to_csv(out_file, index=False)

    print("Step1 complete →", out_file)
    return out_file
