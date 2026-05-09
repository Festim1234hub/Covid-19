"""Figura 2: Pie Chart i statusit global të pacientëve."""

import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style


def plot_pie_chart(df: pd.DataFrame) -> None:
    """Gjeneron pie chart: vdekjet vs të mbijetuarit (20 vende)."""
    apply_style()

    total_deaths  = df["total_deaths"].sum()
    total_cases   = df["total_cases"].sum()
    survived      = total_cases - total_deaths

    labels  = ["Të mbijetuar", "Vdekje"]
    sizes   = [survived, total_deaths]
    colors  = ["#55A868", "#C44E52"]
    explode = (0, 0.06)

    fig, ax = plt.subplots()
    ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct="%1.2f%%", startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 12}
    )
    ax.set_title(
        "Figura 2: Statusi Global i Pacientëve COVID-19\n(20 Vende Evropiane)",
        pad=20
    )

    path = OUTPUT_FIGURES / "fig2_pie_chart.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura 2 ruajtur: {path}")
