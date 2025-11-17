#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – merge_and_compute_per_capita

Κάνει:
- mapping Σταθμός -> Δημοτική Κοινότητα
- merge env & demo δεδομένων
- υπολογισμό "Ρύποι ανά κάτοικο"
"""

import pandas as pd


def merge_and_compute_per_capita(
    env_df: pd.DataFrame,
    demo_df: pd.DataFrame,
    station_to_area_admin: dict
) -> pd.DataFrame:
    """
    Public function (ίδιο όνομα με το αρχικό script).

    Parameters
    ----------
    env_df : DataFrame
        Μέσοι ρύποι ανά σταθμό.
    demo_df : DataFrame
        Πληθυσμός ανά Δημοτική Κοινότητα.
    station_to_area_admin : dict
        Mapping Σταθμός -> Δημοτική Κοινότητα.

    Returns
    -------
    DataFrame
        Συγχωνευμένος πίνακας με "Ρύποι ανά κάτοικο".
    """
    env_df = env_df.copy()
    env_df["Δημοτική Κοινότητα"] = env_df["Σταθμός"].map(station_to_area_admin)

    merged = env_df.merge(demo_df, on="Δημοτική Κοινότητα", how="left")
    merged["Ρύποι ανά κάτοικο"] = (
        merged["Μέσος Όρος 2010–2013"] / merged["Πληθυσμός"]
    )
    return merged
