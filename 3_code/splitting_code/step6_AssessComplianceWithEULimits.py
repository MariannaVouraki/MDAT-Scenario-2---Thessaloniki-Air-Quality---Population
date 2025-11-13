import pandas as pd
from pathlib import Path

LIMITS = {"SO2":125,"NO2":40,"NO":100,"O3":120,"PM10":40,"PM2.5":25,"CO":10}

def run_step_6(step5_output):
    df = pd.read_csv(step5_output)

    def status(row):
        for pollutant, limit in LIMITS.items():
            if pollutant in row and pd.notna(row[pollutant]) and row[pollutant] > limit:
                return "🔴 Υπέρβαση Ορίων"
        return "🟢 Εντός Ορίων"

    df["Κατάσταση"] = df.apply(status, axis=1)

    root = Path(__file__).resolve().parents[2]
    out_file = root / "4_Outputs" / "Step6_assessed.csv"
    df.to_csv(out_file, index=False)

    print("Step6 complete →", out_file)
    return out_file
