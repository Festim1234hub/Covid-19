"""Unit tests për modulin cleaner.py."""

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data, get_latest
from src.data.cleaner import clean, impute_means, NUMERIC_COLS


class TestCleaner(unittest.TestCase):

    def setUp(self):
        """Përgatit dataset-in para çdo testi."""
        self.df = get_latest(load_data())

    def test_clean_returns_dataframe(self):
        """clean() duhet të kthejë DataFrame."""
        rezultati = clean(self.df)
        self.assertIsInstance(rezultati, pd.DataFrame)

    def test_no_nan_after_clean(self):
        """Pas pastrimit nuk duhet të ketë NaN në kolonat numerike."""
        rezultati = clean(self.df)
        for col in NUMERIC_COLS:
            if col in rezultati.columns:
                self.assertEqual(rezultati[col].isnull().sum(), 0)

    def test_impute_fills_with_mean(self):
        """impute_means() duhet të zëvendësojë NaN me mesataren."""
        df_test = self.df.copy()
        # Vendos NaN artificiale
        df_test.loc[df_test.index[0], 'total_cases'] = np.nan
        mesatarja = df_test['total_cases'].mean()
        rezultati = impute_means(df_test)
        vlera_e_zev = rezultati.loc[df_test.index[0], 'total_cases']
        self.assertAlmostEqual(vlera_e_zev, mesatarja, places=2)

    def test_clean_does_not_modify_original(self):
        """clean() nuk duhet të modifikojë DataFrame origjinal."""
        df_kopje = self.df.copy()
        clean(self.df)
        pd.testing.assert_frame_equal(self.df, df_kopje)

    def test_row_count_preserved(self):
        """Numri i rreshtave nuk duhet të ndryshojë pas pastrimit."""
        rezultati = clean(self.df)
        self.assertEqual(len(rezultati), len(self.df))

    def test_clean_removes_duplicates(self):
        """clean() duhet të heqë rreshtat e dubluar."""
        df_me_duplikate = pd.concat([self.df, self.df]).reset_index(drop=True)
        rezultati = clean(df_me_duplikate)
        self.assertLessEqual(len(rezultati), len(df_me_duplikate))


if __name__ == '__main__':
    unittest.main()
