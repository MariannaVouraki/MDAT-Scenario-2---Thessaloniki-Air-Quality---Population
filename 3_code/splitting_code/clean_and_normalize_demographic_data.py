#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – clean_and_normalize_demographic_data

Διαβάζει το Excel απογραφής και επιστρέφει
πίνακα με Πληθυσμό ανά Δημοτική Κοινότητα (1ο, 2ο, κτλ Διαμέρισμα).
"""

from pathlib import Path
import pandas as pd


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    colmap = {}
    for c in df.columns:
        c_clean = str(c).replace("\n", " ").strip()
        c_clean = c_clean.replace("Ημερο -", "Ημερο-").replace("PM2,5", "PM2.5")
        colmap[c] = c_clean
    return df.rename(columns=colmap)


def _read_population(pop_path: Path) -> pd.DataFrame:
    pop_raw = pd.read_excel(pop_path)
    pop = _normalize_columns(pop_raw)

    name_col = next((c for c in pop.columns if "Unnamed: 3" in c), None)
    pop_col = next((c for c in pop.columns if "Unnamed: 4" in c), None)

    pop = pop[[name_col, pop_col]].dropna()
    pop = pop[pop[name_col].astype(str).str.startswith("Δημοτική Κοινότητα")]
    pop = pop.rename(columns={name_col: "Δημοτική Κοινότητα", pop_col: "Πληθυσμός"})
    pop["Πληθυσμός"] = pd.to_numeric(pop["Πληθυσμός"], errors="coerce").astype("Int64")

    pop["Δημοτική Κοινότητα"] = (
        pop["Δημοτική Κοινότητα"]
        .str.extract(r"(Δημοτική Κοινότητα\s*(\d+)[ου]*)")[1]
        .astype(str)
        .apply(lambda x: f"{x}ο Διαμέρισμα")
    )
    return pop


def clean_and_normalize_demographic_data(population_path: Path) -> pd.DataFrame:
    """
    Public function (ίδιο όνομα με το αρχικό script).
    """
    return _read_population(population_path)
