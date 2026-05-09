"""Modul për ngarkimin e dataset-it CSV."""

import pandas as pd
from src.config import DATA_RAW, COUNTRIES, COLUMNS


def load_data() -> pd.DataFrame:
    """Ngarkon dataset-in dhe filtron 20 vendet evropiane."""
    df = pd.read_csv(DATA_RAW, usecols=COLUMNS, parse_dates=["date"])
    df = df[df["location"].isin(COUNTRIES)].copy()
    df = df.sort_values(["location", "date"]).reset_index(drop=True)
    return df


def get_latest(df: pd.DataFrame) -> pd.DataFrame:
    """Merr rreshtin e fundit (datën max) për çdo vend."""
    return (
        df.sort_values("date")
        .groupby("location", as_index=False)
        .last()
        .reset_index(drop=True)
    )
