"""Figura 3: Scatter Plot GDP vs Vaksinimi me trend line."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style


def plot_scatter(df: pd.DataFrame) -> None:
    """Gjeneron scatter plot: GDP per capita vs Vaksinim për 100 banorë.

    - Madhësia e pikave proporcionale me total_cases.
    - Vija e trendit me np.polyfit() (regresion linear).
    - Etiketat e vendeve pranë çdo pike.
    """
    apply_style()

    x = df["gdp_per_capita"]
    y = df["total_vaccinations_per_hundred"]

    # Madhësia e pikave: normalizim ndërmjet 60 dhe 600
    sizes = (df["total_cases"] / df["total_cases"].max()) * 540 + 60

    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, color="#4C72B0", alpha=0.7, edgecolors="white", linewidths=0.8)

    # Vija e trendit
    coeffs = np.polyfit(x, y, deg=1)
    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = np.polyval(coeffs, x_line)
    ax.plot(x_line, y_line, color="#C44E52", linewidth=1.8, linestyle="--", label="Trend linear")

    # Etiketat e vendeve
    for _, row in df.iterrows():
        ax.annotate(
            row["location"],
            xy=(row["gdp_per_capita"], row["total_vaccinations_per_hundred"]),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7.5,
        )

    ax.set_xlabel("GDP per Capita (USD)")
    ax.set_ylabel("Vaksinime për 100 Banorë")
    ax.set_title("Figura 3: GDP per Capita vs Vaksinimi — 20 Vende Evropiane")
    ax.legend(fontsize=9)
    plt.tight_layout()

    path = OUTPUT_FIGURES / "fig3_scatter_plot.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura 3 ruajtur: {path}")

