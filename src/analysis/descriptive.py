"""Statistikat përshkruese - Tabela 1."""

import pandas as pd
from src.config import OUTPUT_TABLES

# Kolonat për statistikat
STATS_COLS = [
    "total_cases", "total_deaths", "CFR",
    "Cases_per_100k", "total_vaccinations_per_hundred", "gdp_per_capita"
]


def compute_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Llogarit statistikat përshkruese për kolonat kryesore."""
    return df[STATS_COLS].describe().round(2)


def save_stats(df: pd.DataFrame) -> None:
    """Ruan tabelën e statistikave në outputs/tables/."""
    stats = compute_stats(df)
    path = OUTPUT_TABLES / "tabela1_statistikat_pershkruese.csv"
    stats.to_csv(path)
    print(f"Tabela 1 ruajtur: {path}")
