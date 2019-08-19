import unittest as unittest
from wdpa import qa
import pandas as pd
import numpy as np
import os

# run test in root 
# python -m unittest
test_data = os.getcwd() + os.sep + 'tests' + os.sep + r'data.gdb\test'

wdpa_df = qa.arcgis_table_to_df(test_data, qa.INPUT_FIELDS_POLY)


class TestNull(unittest.TestCase):
    def test_nan_name(self):
        self.assertEqual(qa.nan_present_name(wdpa_df, True), np.array([40597.]))

    def test_nan_origin_name(self):
        self.assertEqual(qa.nan_present_orig_name(wdpa_df, True), np.array([40463.]))

    def test_nan_desig(self):
        self.assertEqual(qa.nan_present_desig(wdpa_df, True), np.array([64669.]))

    def test_nan_desig_eng(self):
        self.assertEqual(qa.nan_present_desig_eng(wdpa_df, True), np.array([315109.]))
    
    def test_mang_auth(self):
        self.assertFalse(qa.nan_present_mang_auth(wdpa_df))

if __name__ == '__main__':
    unittest.main()