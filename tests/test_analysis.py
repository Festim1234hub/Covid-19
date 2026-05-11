"""Unit tests."""

import pandas as pd
import numpy as np
import pytest

from src.analysis.clustering  import kmeans_clustering
from src.analysis.correlation import pearson_gdp_vaccination


@pytest.fixture
def sample_df():
    """DataFrame minimal me 6 vende për testim."""
    return pd.DataFrame({
        "location":                       ["A", "B", "C", "D", "E", "F"],
        "total_cases":                    [100_000, 500_000, 1_000_000,
                                           200_000, 800_000, 300_000],
        "total_deaths":                   [1_000, 8_000, 12_000,
                                           3_000, 10_000, 4_500],
        "CFR":                            [1.0, 1.6, 1.2, 1.5, 1.25, 1.5],
        "Cases_per_100k":                 [2_000, 8_000, 15_000,
                                           4_000, 12_000, 5_000],
        "total_vaccinations_per_hundred": [80, 130, 160, 95, 145, 110],
        "gdp_per_capita":                 [10_000, 35_000, 55_000,
                                           15_000, 45_000, 20_000],
        "population":                     [5_000_000] * 6,
    })


class TestKMeans:
    def test_returns_exactly_3_cluster_labels(self, sample_df):
        """Cluster-et duhet të jenë saktësisht {0, 1, 2}."""
        result = kmeans_clustering(sample_df)
        unique_labels = set(result["Cluster"].unique())
        assert unique_labels == {0, 1, 2}

    def test_cluster_column_added(self, sample_df):
        """Kolona 'Cluster' duhet të ekzistojë pas clustering."""
        result = kmeans_clustering(sample_df)
        assert "Cluster" in result.columns

    def test_all_rows_assigned(self, sample_df):
        """Çdo rresht duhet të ketë një cluster label (pa NaN)."""
        result = kmeans_clustering(sample_df)
        assert result["Cluster"].notna().all()

    def test_original_df_unchanged(self, sample_df):
        """Funksioni nuk duhet të modifikojë DataFrame-in origjinal."""
        kmeans_clustering(sample_df)
        assert "Cluster" not in sample_df.columns


class TestCorrelation:
    def test_pearson_r_between_minus1_and_1(self, sample_df):
        """Pearson r duhet të jetë ndërmjet -1 dhe 1."""
        r, _ = pearson_gdp_vaccination(sample_df)
        assert -1.0 <= r <= 1.0

    def test_pearson_p_value_non_negative(self, sample_df):
        """p-value duhet të jetë jo-negativ."""
        _, p = pearson_gdp_vaccination(sample_df)
        assert p >= 0.0

    def test_pearson_returns_floats(self, sample_df):
        """Funksioni duhet të kthejë dy float."""
        r, p = pearson_gdp_vaccination(sample_df)
        assert isinstance(r, float)
        assert isinstance(p, float)

    def test_perfect_correlation(self):
        """Korrelacioni i një vargu me vetveten duhet të jetë 1.0."""
        df_perfect = pd.DataFrame({
            "gdp_per_capita":                 [1.0, 2.0, 3.0, 4.0, 5.0],
            "total_vaccinations_per_hundred": [1.0, 2.0, 3.0, 4.0, 5.0],
        })
        r, _ = pearson_gdp_vaccination(df_perfect)
        assert abs(r - 1.0) < 1e-9

