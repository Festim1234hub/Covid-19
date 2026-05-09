"""Figura 1: Bar Chart i 10 vendeve kryesore."""

import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style


def plot_bar_chart(df: pd.DataFrame) -> None:
    """Gjeneron bar chart horizontal për 10 vendet me rastet më të larta."""
    apply_style()

    top10 = (
        df.nlargest(10, "total_cases")[["location", "total_cases"]]
        .sort_values("total_cases")
    )

    fig, ax = plt.subplots()
    bars = ax.barh(top10["location"], top10["total_cases"] / 1_000_000,
                   color="#4C72B0", edgecolor="white")

    # Shto vlerat në fund të çdo shtylle
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}M", va="center", fontsize=9)

    ax.set_xlabel("Rastet totale (milionë)")
    ax.set_title("Figura 1: 10 Vendet Evropiane me Rastet më të Larta COVID-19")
    ax.grid(axis="x", alpha=0.4)
    plt.tight_layout()

    path = OUTPUT_FIGURES / "fig1_bar_chart.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura 1 ruajtur: {path}")
