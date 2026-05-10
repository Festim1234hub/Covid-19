"""K-Means Clustering me 3 grupe + StandardScaler."""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

CLUSTER_FEATURES = [
    "Cases_per_100k",
    "CFR",
    "total_vaccinations_per_hundred",
    "gdp_per_capita",
]


def kmeans_clustering(df: pd.DataFrame) -> pd.DataFrame:
    """Grupron 20 vendet në 3 cluster me K-Means.

    Hap 1: StandardScaler() për normalizim të features.
    Hap 2: KMeans(n_clusters=3, random_state=42) për grupim.
    Hap 3: Shton kolonën 'Cluster' në DataFrame.
    """
    df = df.copy()

    # Hap 1: Normalizim
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[CLUSTER_FEATURES])

    # Hap 2: K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    # Hap 3: Shto kolonën Cluster
    df["Cluster"] = labels

    return df

