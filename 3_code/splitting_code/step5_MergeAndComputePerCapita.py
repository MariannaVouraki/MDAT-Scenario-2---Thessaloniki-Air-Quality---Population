import pandas as pd
from pathlib import Path

STATION_TO_AREA_ADMIN = {
    "Στ. ΕΓΝΑΤΙΑΣ": "1ο Διαμέρισμα",
    "Στ. ΛΑΓΚΑΔΑ": "2ο Διαμέρισμα",
    "Στ. ΕΠΤΑΠΥΡΓΙΟΥ": "3ο Διαμέρισμα",
    "Στ. 25ης ΜΑΡΤΙΟΥ": "4ο Διαμέρισμα",
    "Στ. ΜΑΛΑΚΟΠΗΣ": "4ο Διαμέρισμα",
    "Στ. ΝΕΟΥ ΔΗΜΑΡΧΕΙΟΥ": "5ο Διαμέρισμα"
}

def run_step_5(step2_output, step4_output):
    env = pd.read_csv(step2_output)
    demo = pd.read_csv(step4_output)

    env["Δημοτική Κοινότητα"] = env["_sheet"].map(STATION_TO_AREA_ADMIN)

    merged = env.merge(demo, on="Δημοτική Κοινότητα", how="left")

    merged["Ρύποι ανά κάτοικο"] = (
        merged.drop(columns=["_sheet","Πληθυσμός","Δημοτική Κοινότητα"], errors="ignore").mean(axis=1)
        / merged["Πληθυσμός"]
    )

    root = Path(__file__).resolve().parents[2]
    out_file = root / "4_Outputs" / "Step5_merged.csv"
    merged.to_csv(out_file, index=False)

    print("Step5 complete →", out_file)
    return out_file
