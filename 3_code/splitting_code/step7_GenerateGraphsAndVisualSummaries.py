import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def run_step_7(step6_output):
    df = pd.read_csv(step6_output)

    root = Path(__file__).resolve().parents[2]
    out_dir = root / "4_Outputs"

    pollutants = ["SO2","NO2","NO","O3","PM10","PM2.5","CO"]

    for pollutant in pollutants:
        if pollutant not in df.columns:
            continue

        plt.figure(figsize=(10,6))
        plt.bar(df["Δημοτική Κοινότητα"], df[pollutant])
        plt.title(f"{pollutant} by district")

        out = out_dir / f"{pollutant}_by_district.png"
        plt.savefig(out, dpi=300)
        plt.close()

    print("Step7 complete → graphs saved")
