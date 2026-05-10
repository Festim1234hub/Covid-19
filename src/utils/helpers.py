"""Funksione ndihmëse: save_figure, save_table."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_figure(fig: plt.Figure, path: Path) -> None:
    """Ruan figurën si PNG me dpi=300."""
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Figura ruajtur: {path}")


def save_table(df: pd.DataFrame, path: Path) -> None:
    """Ruan DataFrame si CSV."""
    df.to_csv(path, index=True)
    print(f"Tabela ruajtur: {path}")

