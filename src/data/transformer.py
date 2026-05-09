"""Llogaritja e CFR dhe Cases_per_100k."""

import pandas as pd


def add_cfr(df: pd.DataFrame) -> pd.DataFrame:
    """CFR (Case Fatality Rate) = vdekjet / rastet * 100."""
    df = df.copy()
    df["CFR"] = (df["total_deaths"] / df["total_cases"] * 100).round(2)
    return df


def add_cases_per_100k(df: pd.DataFrame) -> pd.DataFrame:
    """Cases_per_100k = rastet totale për 100,000 banorë."""
    df = df.copy()
    df["Cases_per_100k"] = (
        df["total_cases"] / df["population"] * 100_000
    ).round(2)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Aplikon të gjitha transformimet mbi dataset-in."""
    df = add_cfr(df)
    df = add_cases_per_100k(df)
    return df
