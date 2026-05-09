"""Pastrimi i të dhënave - mean imputation për NaN."""

import pandas as pd

# Kolonat numerike që pastrohen
NUMERIC_COLS = [
    "total_cases", "total_deaths",
    "total_vaccinations_per_hundred", "gdp_per_capita"
]


def impute_means(df: pd.DataFrame) -> pd.DataFrame:
    """Zëvendëson NaN me mesataren globale të çdo kolone."""
    df = df.copy()
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Pastrimi i plotë: mean imputation + heqja e duplikateve."""
    df = impute_means(df)
    df = df.drop_duplicates().reset_index(drop=True)
    return df
