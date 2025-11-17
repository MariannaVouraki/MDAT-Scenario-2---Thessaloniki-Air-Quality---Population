#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – aggregate_and_compute_mean_pollutant_levels

Διαβάζει τα φύλλα ρύπανσης για όλους τους σταθμούς
και υπολογίζει τους μέσους όρους 2010–2013 ανά ρύπο/σταθμό.
"""

from pathlib import Path
from typing import List
import pandas as pd


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    colmap = {}
    for c in df.columns:
        c_clean = str(c).replace("\n", " ").strip()
        c_clean = c_clean.replace("Ημερο -", "Ημερο-").replace("PM2,5", "PM2.5")
        colmap[c] = c_clean
    return df.rename(columns=colmap)


def _read_pollution_sheets(pollution_path: Path,
                           station_sheets: List[str]) -> List[pd.DataFrame]:
    dfs = []
    for sheet in station_sheets:
        df = pd.read_excel(pollution_path, sheet_name=sheet)
        df = _normalize_columns(df)
        df["_sheet"] = sheet
        dfs.append(df)
    return dfs


def _compute_overall_means(pollution_dfs: List[pd.DataFrame]) -> pd.DataFrame:
    records = []
    for df in pollution_dfs:
        sheet = df["_sheet"].iloc[0]
        pollutant_cols = [
            c for c in df.columns
            if any(p in c for p in ["SO2", "PM10", "PM2.5", "CO", "NO", "O3"])
        ]
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


def aggregate_and_compute_mean_pollutant_levels(
    pollution_path: Path,
    station_sheets: List[str]
) -> pd.DataFrame:
    """
    Public function (ίδιο όνομα με το αρχικό script).

    Parameters
    ----------
    pollution_path : Path
        Διαδρομή στο Excel με τις μετρήσεις ρύπανσης.
    station_sheets : list[str]
        Λίστα με τα ονόματα των φύλλων (σταθμούς).

    Returns
    -------
    pd.DataFrame
        Μέσοι όροι ρύπων ανά σταθμό.
    """
    pollution_dfs = _read_pollution_sheets(pollution_path, station_sheets)
    overall_means = _compute_overall_means(pollution_dfs)
    return overall_means
