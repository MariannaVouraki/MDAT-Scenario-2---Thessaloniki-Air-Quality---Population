import pandas as pd
from pathlib import Path

# helper embedded
def normalize_columns(df):
    colmap = {}
    for c in df.columns:
        clean = str(c).replace("\n"," ").strip()
        clean = clean.replace("PM2,5","PM2.5").replace("Ημερο -","Ημερο-")
        colmap[c] = clean
    return df.rename(columns=colmap)

def run_step_3():
    root = Path(__file__).resolve().parents[2]
    data_dir = root / "2_data"
    out_dir = root / "4_Outputs"

    in_file = data_dir / "resident_population_census2011-extended thessaloniki.xlsx"
    out_file = out_dir / "Step3_demo_raw.csv"

    df = pd.read_excel(in_file)
    df = normalize_columns(df)

    df.to_csv(out_file, index=False)
    print("Step3 complete →", out_file)
    return out_file
