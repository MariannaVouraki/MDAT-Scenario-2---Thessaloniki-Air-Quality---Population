#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – assess_compliance_with_eu_limits

Ελέγχει για κάθε ρύπο αν είναι εντός / εκτός ορίων ΕΕ.
"""

import pandas as pd


def _check_pollutant_status(row, limits: dict) -> str:
    pollutant = row["Ρύπος"]
    value = row["Μέσος Όρος 2010–2013"]
    if pollutant not in limits:
        return "Άγνωστο"
    limit = limits[pollutant]
    return "🔴 Υπέρβαση Ορίων" if value > limit else "🟢 Εντός Ορίων"


def assess_compliance_with_eu_limits(df: pd.DataFrame, limits: dict) -> pd.DataFrame:
    """
    Public function (ίδιο όνομα με το αρχικό script).

    Parameters
    ----------
    df : DataFrame
        Πίνακας με μέσους ρύπους & πληθυσμό.
    limits : dict
        Λεξικό {ρύπος: όριο}.

    Returns
    -------
    DataFrame
        Όπως df + στήλη "Κατάσταση".
    """
    out = df.copy()
    out["Κατάσταση"] = out.apply(_check_pollutant_status, axis=1, limits=limits)
    return out
