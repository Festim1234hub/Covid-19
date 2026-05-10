"""Figura 5: Vizualizimi i K-Means clustering."""

import matplotlib.pyplot as plt
import pandas as pd
from src.config import OUTPUT_FIGURES
from src.visualization.style_config import apply_style

CLUSTER_COLORS = ["#4C72B0", "#C44E52", "#55A868"]
CLUSTER_LABELS = ["Grup 0", "Grup 1", "Grup 2"]


def plot_kmeans(df: pd.DataFrame) -> None:
    """Gjeneron scatter plot të 3 grupeve K-Means (Cases_per_100k vs CFR).

    Kërkon që df të ketë kolonën 'Cluster' nga kmeans_clustering().
    """
    apply_style()

    fig, ax = plt.subplots()

    for cluster_id in sorted(df["Cluster"].unique()):
        subset = df[df["Cluster"] == cluster_id]
        ax.scatter(
            subset["Cases_per_100k"],
            subset["CFR"],
            color=CLUSTER_COLORS[cluster_id],
            s=120,
            edgecolors="white",
            linewidths=0.8,
            label=CLUSTER_LABELS[cluster_id],
            zorder=3,
        )

        # Etiketat e vendeve
        for _, row in subset.iterrows():
            ax.annotate(
                row["location"],
                xy=(row["Cases_per_100k"], row["CFR"]),
                xytext=(5, 4),
                textcoords="offset points",
                fontsize=7.5,
                color=CLUSTER_COLORS[cluster_id],
            )

    ax.set_xlabel("Rastet për 100,000 Banorë")
    ax.set_ylabel("Case Fatality Rate — CFR (%)")
    ax.set_title("Figura 5: K-Means Clustering — 20 Vende Evropiane (3 Grupe)")
    ax.legend(title="Cluster", fontsize=10)
    plt.tight_layout()

    path = OUTPUT_FIGURES / "fig5_kmeans.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Figura 5 ruajtur: {path}")

