#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process – generate_graphs_and_visual_summaries

Παράγει:
- Γραφήματα ρύπου ανά Δημοτική Κοινότητα
- Γράφημα συνολικών ρύπων ανά κάτοικο
και τα αποθηκεύει στον φάκελο outputs.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def _plot_pollutant_by_district(df: pd.DataFrame, outdir: Path, limits: dict) -> None:
    df = df.dropna(subset=["Μέσος Όρος 2010–2013"])
    pollutants = df["Ρύπος"].unique()

    for pollutant in pollutants:
        sub = df[df["Ρύπος"] == pollutant].copy()
        if sub.empty:
            continue

        sub["Χρώμα"] = sub.apply(
            lambda r: "red" if "Υπέρβαση" in str(r["Κατάσταση"]) else "green",
            axis=1
        )

        plt.figure(figsize=(10, 6))
        bars = plt.bar(
            sub["Δημοτική Κοινότητα"],
            sub["Μέσος Όρος 2010–2013"],
            color=sub["Χρώμα"],
            alpha=0.8
        )

        for bar, val in zip(bars, sub["Μέσος Όρος 2010–2013"]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        if pollutant in limits:
            plt.axhline(
                limits[pollutant],
                color="orange",
                linestyle="--",
                label=f"Όριο ΕΕ: {limits[pollutant]} {'mg/m³' if pollutant=='CO' else 'μg/m³'}"
            )

        plt.title(f"{pollutant} – Μέσος Όρος 2010–2013 ανά Δημοτική Κοινότητα")
        plt.ylabel("Συγκέντρωση")
        plt.xlabel("Δημοτική Κοινότητα")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()

        save_path = outdir / f"{pollutant}_by_district.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"📊 Αποθηκεύτηκε γράφημα: {save_path}")


def _plot_total_pollution_per_capita(df: pd.DataFrame, outdir: Path) -> None:
    df = df.dropna(subset=["Ρύποι ανά κάτοικο"])
    total_per_district = (
        df.groupby("Δημοτική Κοινότητα", as_index=False)["Ρύποι ανά κάτοικο"].sum()
    )

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        total_per_district["Δημοτική Κοινότητα"],
        total_per_district["Ρύποι ανά κάτοικο"],
        color="royalblue",
        alpha=0.8
    )

    for bar, val in zip(bars, total_per_district["Ρύποι ανά κάτοικο"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.00001,
            f"{val:.6f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.title("Συνολικοί Ρύποι Ανά Κάτοικο (2010–2013) ανά Δημοτική Κοινότητα")
    plt.ylabel("Συνολικοί Ρύποι ανά Κάτοικο (μονάδες συγκέντρωσης)")
    plt.xlabel("Δημοτική Κοινότητα")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    save_path = outdir / "Total_Pollutants_per_Capita.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"📊 Αποθηκεύτηκε συνολικό γράφημα: {save_path}")


def generate_graphs_and_visual_summaries(
    df: pd.DataFrame,
    output_dir: Path,
    limits: dict
) -> None:
    """
    Public function (ίδιο όνομα με το αρχικό script).
    """
    _plot_pollutant_by_district(df, output_dir, limits)
    _plot_total_pollution_per_capita(df, output_dir)
