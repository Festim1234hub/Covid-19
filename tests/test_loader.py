"""Unit tests për modulin loader.py."""

import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data, get_latest
from src.config import COUNTRIES


class TestLoader(unittest.TestCase):

    def setUp(self):
        """Ngarkon dataset-in një herë për të gjitha testet."""
        self.df_full = load_data()
        self.df_latest = get_latest(self.df_full)

    def test_load_returns_dataframe(self):
        """load_data() duhet të kthejë DataFrame."""
        self.assertIsInstance(self.df_full, pd.DataFrame)

    def test_load_not_empty(self):
        """Dataset-i nuk duhet të jetë bosh."""
        self.assertGreater(len(self.df_full), 0)

    def test_correct_number_of_countries(self):
        """Duhet të ketë saktësisht 20 vende."""
        self.assertEqual(self.df_full['location'].nunique(), 20)

    def test_all_countries_present(self):
        """Të gjitha 20 vendet duhet të jenë në dataset."""
        vendet_e_ngarkuara = set(self.df_full['location'].unique())
        for vend in COUNTRIES:
            self.assertIn(vend, vendet_e_ngarkuara)

    def test_get_latest_returns_one_row_per_country(self):
        """get_latest() duhet të kthejë 1 rresht për çdo vend."""
        self.assertEqual(len(self.df_latest), 20)

    def test_required_columns_exist(self):
        """Kolonat e nevojshme duhet të ekzistojnë."""
        kolonat = ['location', 'date', 'total_cases',
                   'total_deaths', 'gdp_per_capita', 'population']
        for kol in kolonat:
            self.assertIn(kol, self.df_full.columns)

    def test_date_column_is_datetime(self):
        """Kolona date duhet të jetë tip datetime."""
        self.assertIn('datetime64', str(self.df_full['date'].dtype))


if __name__ == '__main__':
    unittest.main()
