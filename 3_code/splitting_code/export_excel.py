#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – export_excel

Εξαγωγή:
- Mapping Σταθμός -> Δημοτική Κοινότητα
- Αποτελέσματα με μέσους & ανά κάτοικο
σε ένα Excel αρχείο.
"""

from pathlib import Path
import pandas as pd


def export_excel(mapping_df: pd.DataFrame,
                 results_df: pd.DataFrame,
                 outxlsx: Path) -> None:
    """
    Public function (ίδιο όνομα με το αρχικό script στο κομμάτι ΕΞΑΓΩΓΕΣ).
    """
    with pd.ExcelWriter(outxlsx) as writer:
        mapping_df.to_excel(writer, sheet_name="Mapping", index=False)
        results_df.to_excel(
            writer,
            sheet_name="Συνολικοί Μέσοι & Ανά Κάτοικο",
            index=False
        )
    print(f"📄 Αποθήκευση Excel: {outxlsx}")