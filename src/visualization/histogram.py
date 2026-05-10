"""Figura 4: Histogram i CFR me mean/median lines."""

import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style


def plot_histogram(df: pd.DataFrame) -> None:
    """Gjeneron histogram të CFR me 10 bins + vija për mesataren dhe medianën."""
    apply_style()

    cfr = df["CFR"].dropna()
    mean_val   = cfr.mean()
    median_val = cfr.median()

    fig, ax = plt.subplots()

    ax.hist(cfr, bins=10, color="#4C72B0", edgecolor="white", alpha=0.85)

    # Vija vertikale për mesataren (e kuqe)
    ax.axvline(mean_val, color="#C44E52", linewidth=2,
               linestyle="--", label=f"Mesatare: {mean_val:.2f}%")

    # Vija vertikale për medianën (jeshile)
    ax.axvline(median_val, color="#55A868", linewidth=2,
               linestyle="-", label=f"Mediana: {median_val:.2f}%")

    ax.set_xlabel("Case Fatality Rate — CFR (%)")
    ax.set_ylabel("Numri i Vendeve")
    ax.set_title("Figura 4: Shpërndarja e CFR — 20 Vende Evropiane")
    ax.legend(fontsize=10)
    plt.tight_layout()

    path = OUTPUT_FIGURES / "fig4_histogram.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura 4 ruajtur: {path}")

