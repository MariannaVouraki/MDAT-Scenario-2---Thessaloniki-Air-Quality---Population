import pandas as pd
from pathlib import Path

LIMIT_COLUMNS = ["SO2","NO2","NO","O3","PM10","PM2.5","CO"]

def run_step_2(step1_output):
    df = pd.read_csv(step1_output)

    pollutant_cols = [c for c in df.columns if any(p in c for p in LIMIT_COLUMNS)]
    df[pollutant_cols] = df[pollutant_cols].apply(pd.to_numeric, errors="coerce")

    means = df.groupby("_sheet")[pollutant_cols].mean().reset_index()

    root = Path(__file__).resolve().parents[2]
    out_file = root / "4_Outputs" / "Step2_mean_pollutants.csv"
    means.to_csv(out_file, index=False)

    print("Step2 complete →", out_file)
    return out_file
