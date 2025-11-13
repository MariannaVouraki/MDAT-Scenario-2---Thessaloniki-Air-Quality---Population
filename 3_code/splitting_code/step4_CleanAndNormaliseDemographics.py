import pandas as pd
from pathlib import Path

def run_step_4(step3_output):
    df = pd.read_csv(step3_output)

    name_col = [c for c in df.columns if "Unnamed: 3" in c][0]
    pop_col  = [c for c in df.columns if "Unnamed: 4" in c][0]

    df = df[[name_col, pop_col]].dropna()
    df = df[df[name_col].astype(str).str.startswith("Δημοτική Κοινότητα")]

    df = df.rename(columns={name_col:"Δημοτική Κοινότητα", pop_col:"Πληθυσμός"})
    df["Πληθυσμός"] = pd.to_numeric(df["Πληθυσμός"], errors="coerce")

    df["Δημοτική Κοινότητα"] = (
        df["Δημοτική Κοινότητα"]
        .str.extract(r"(Δημοτική Κοινότητα\s*(\d+))")[1]
        .astype(str)
        .apply(lambda x: f"{x}ο Διαμέρισμα")
    )

    root = Path(__file__).resolve().parents[2]
    out_file = root / "4_Outputs" / "Step4_demo_clean.csv"
    df.to_csv(out_file, index=False)

    print("Step4 complete →", out_file)
    return out_file
