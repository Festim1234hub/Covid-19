"""Korrelacioni Pearson GDP vs Vaksinim."""

import numpy as np
import pandas as pd
from scipy import stats


def pearson_gdp_vaccination(df: pd.DataFrame) -> tuple:
    """Llogarit korrelacionin Pearson midis GDP dhe vaksinimit."""
    df_clean = df[["gdp_per_capita", "total_vaccinations_per_hundred"]].dropna()
    r, p = stats.pearsonr(
        df_clean["gdp_per_capita"],
        df_clean["total_vaccinations_per_hundred"]
    )
    return round(float(r), 4), round(float(p), 4)


def print_results(df: pd.DataFrame) -> None:
    """Shfaq rezultatin e korrelacionit në terminal."""
    r, p = pearson_gdp_vaccination(df)
    fuqi = "i fortë" if abs(r) > 0.6 else "i mesëm" if abs(r) > 0.3 else "i dobët"
    dom  = "domethënës" if p < 0.05 else "jo domethënës statistikisht"
    print(f"Pearson r = {r}")
    print(f"p-value   = {p}")
    print(f"Korrelacion {fuqi}, {dom} (alfa = 0.05)")
