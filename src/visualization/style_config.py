"""Konfigurimi i stilit global të grafikëve."""

import matplotlib.pyplot as plt
import seaborn as sns


def apply_style() -> None:
    """Aplikon stilin global për të gjithë grafikët e projektit."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.figsize":    (12, 7),
        "figure.dpi":        150,
        "font.size":         11,
        "axes.titlesize":    14,
        "axes.titleweight":  "bold",
        "axes.labelsize":    12,
        "xtick.labelsize":   10,
        "ytick.labelsize":   10,
    })
