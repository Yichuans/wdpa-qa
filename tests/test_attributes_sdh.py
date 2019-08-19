# Test attributes
# Stijn den Haan
# 29 July 2019

import unittest as unittest
from wdpa import qas
import pandas as pd
import numpy as np
import os

# Set working directory
os.chdir(r"C:\Users\paintern\Desktop\Stijn\z. GitHub repo\wdpa-qa\dummyData")

# Load fields of the WDPA - polygon table
fields = [u'WDPAID', u'WDPA_PID', u'PA_DEF', u'NAME', u'ORIG_NAME', u'DESIG',
       u'DESIG_ENG', u'DESIG_TYPE', u'IUCN_CAT', u'INT_CRIT', u'MARINE',
       u'REP_M_AREA', u'GIS_M_AREA', u'REP_AREA', u'GIS_AREA', u'NO_TAKE',
       u'NO_TK_AREA', u'STATUS', u'STATUS_YR', u'GOV_TYPE', u'OWN_TYPE',
       u'MANG_AUTH', u'MANG_PLAN', u'VERIF', u'METADATAID', u'SUB_LOC',
       u'PARENT_ISO3', u'ISO3']

############################
#### 1. Load dummy data ####
############################

# The dummy data that is loaded to test the code, 
# was created using Excel.

## AP: create class to test data import and utility functions below?
#def test_arcgis_table_to_df
#def test_invalid_data_import
#def test_find_wdpa_rows

class TestHardcoded(unittest.TestCase):
    def test_invalid_nan(self):
        self.assertEqual(qas.invalid_nan(
            wdpa_df, 
            'WDPA_PID', True), 
            np.array([2, 5]))

    def test_invalid_nan_source(self):
        self.assertEqual(qas.invalid_nan(
            wdpa_df, 
            'METADATAID', True), 
            np.array([6, 7, 10, 16, 18, 19, 49, 53, 63]))

    def test_duplicate_wdpa_pid(self):
        self.assertEqual(qas.duplicate_wdpa_pid(
            wdpa_df, 
            True), 
            np.array([2,3,7,8]))

    def test_area_invalid_marine(self):
        self.assertEqual(qas.area_invalid_marine(
            wdpa_df, 
            True), 
            np.array([4, 7, 10]))

    def test_area_invalid_too_large_gis(self):
        self.assertEqual(qas.area_invalid_too_large_gis(
            wdpa_df, 
            True), 
            np.array([3,8]))

    def test_area_invalid_too_large_rep(self):
        self.assertEqual(qas.area_invalid_too_large_rep(
            wdpa_df, 
            True), 
            np.array([5,9,10]))

    def test_area_invalid_too_large_gis_m(self):
        self.assertEqual(qas.area_invalid_too_large_gis_m(
            wdpa_df, 
            True), 
            np.array([1,2]))

    def test_area_invalid_too_large_rep_m(self):
        self.assertEqual(qas.area_invalid_too_large_rep_m(
            wdpa_df, 
            True), 
            np.array([4,7]))

    def test_area_invalid_gis_area(self):
        self.assertEqual(qas.area_invalid_gis_area(
            wdpa_df, 
            True), 
            np.array([5,10]))

    def test_area_invalid_rep_m_area_marine12(self):
        self.assertEqual(qas.area_invalid_rep_m_area_marine12(
            wdpa_df, 
            True), 
            np.array([3,6,9]))

    def test_area_invalid_gis_m_area_marine12(self):
        self.assertEqual(qas.area_invalid_gis_m_area_marine12(
            wdpa_df, 
            True), 
            np.array([3,8,10]))

    def test_invalid_no_take_no_tk_area_rep_m_area(self):
        self.assertEqual(qas.invalid_no_take_no_tk_area_rep_m_area(
            wdpa_df, 
            True), 
            np.array([1,4]))

    def test_invalid_int_crit_desig_eng_other(self):
        self.assertEqual(qas.invalid_int_crit_desig_eng_other(
            wdpa_df, 
            True), 
            np.array([1,5,8]))

    def test_invalid_desig_eng_iucn_cat_other(self):
        self.assertEqual(qas.invalid_desig_eng_iucn_cat_other(
            wdpa_df, 
            True), 
            np.array([5,7,9]))

class TestInconsistent(unittest.TestCase):
    def test_inconsistent_name_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_name_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([3,4,5,7,8,9,10]))

    def test_inconsistent_orig_name_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_orig_name_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([1,2,3,4,7,8,9,10]))

    def test_inconsistent_desig_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_desig_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([3,4,5,8,9,10]))

    def test_inconsistent_desig_eng_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_desig_eng_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([3,4,5,8,9,10]))

    def test_inconsistent_desig_type_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_desig_type_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([1,2,3,9,10]))

    def test_inconsistent_iucn_cat_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_iucn_cat_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([4,5,6, 8,9,10]))

    def test_inconsistent_int_crit_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_int_crit_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([3,4,7,8]))

    def test_inconsistent_no_take_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_no_take_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([1,2,3]))

    def test_inconsistent_status_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_status_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([3,4,5]))

    def test_inconsistent_status_yr_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_status_yr_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([1,2]))

    def test_inconsistent_gov_type_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_gov_type_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([2,3]))

    def test_inconsistent_own_type_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_own_type_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([5,6,7]))

    def test_inconsistent_mang_auth_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_mang_auth_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([2,3,6,7]))

    def test_inconsistent_mang_plan_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_mang_plan_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([7,8,9,10]))

    def test_inconsistent_verif_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_verif_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([7,8]))

    def test_inconsistent_metadataid_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_metadataid_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([5,6,7,8]))

    def test_inconsistent_sub_loc_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_sub_loc_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([2,3,9,10]))

    def test_inconsistent_parent_iso3_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_parent_iso3_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([2,3,8,9]))

    def test_inconsistent_iso3_same_wdpaid(self):
        self.assertEqual(qas.inconsistent_iso3_same_wdpaid(
            wdpa_df, 
            True), 
            np.array([8,9,10]))

class TestInvalid(unittest.TestCase):
    def test_invalid_pa_def(self):
        self.assertEqual(qas.invalid_pa_def(
            wdpa_df, 
            True), 
            np.array([1,7,10]))

    def test_invalid_desig_eng_international(self):
        self.assertEqual(qas.invalid_desig_eng_international(
            wdpa_df, 
            True), 
            np.array([2,3,8]))

    def test_invalid_desig_type_international(self):
        self.assertEqual(qas.invalid_desig_type_international(
            wdpa_df, 
            True), 
            np.array([5,8]))

    def test_invalid_desig_eng_regional(self):
        self.assertEqual(qas.invalid_desig_eng_regional(
            wdpa_df, 
            True), 
            np.array([1,3,6]))

    def test_invalid_desig_type_regional(self):
        self.assertEqual(qas.invalid_desig_type_regional(
            wdpa_df, 
            True), 
            np.array([6,8]))

    def test_invalid_int_crit_desig_eng_ramsar_whs(self):
        self.assertEqual(qas.invalid_int_crit_desig_eng_ramsar_whs(
            wdpa_df, 
            True), 
            np.array([5,9,10]))

    def test_invalid_desig_type(self):
        self.assertEqual(qas.invalid_desig_type(
            wdpa_df, 
            True), 
            np.array([4,6,9]))

    def test_invalid_iucn_cat(self):
        self.assertEqual(qas.invalid_iucn_cat(
            wdpa_df, 
            True), 
            np.array([4,7,10]))

    def test_invalid_iucn_cat_unesco_whs(self):
        self.assertEqual(qas.invalid_iucn_cat_unesco_whs(
            wdpa_df, 
            True), 
            np.array([7,10]))

    def test_invalid_marine(self):
        self.assertEqual(qas.invalid_marine(
            wdpa_df, 
            True), 
            np.array([5,7,10]))

    def test_invalid_no_take_marine0(self):
        self.assertEqual(qas.invalid_no_take_marine0(
            wdpa_df, 
            True), 
            np.array([1,3,6]))

    def test_invalid_no_take_marine12(self):
        self.assertEqual(qas.invalid_no_take_marine12(
            wdpa_df, 
            True), 
            np.array([3,6,8]))

    def test_invalid_no_tk_area_marine(self):
        self.assertEqual(qas.invalid_no_tk_area_marine(
            wdpa_df, 
            True), 
            np.array([2,4,8]))

    def test_invalid_no_tk_area_no_take(self):
        self.assertEqual(qas.invalid_no_tk_area_no_take(
            wdpa_df, 
            True), 
            np.array([2,4,8,10]))

    def test_invalid_status(self):
        self.assertEqual(qas.invalid_status(
            wdpa_df, 
            True), 
            np.array([1,5,7,9]))

    def test_invalid_status_yr(self):
        self.assertEqual(qas.invalid_status_yr(
            wdpa_df, 
            True), 
            np.array([1,4,5]))

    def test_invalid_gov_type(self):
        self.assertEqual(qas.invalid_gov_type(
            wdpa_df, 
            True), 
            np.array([1,3,6]))

    def test_invalid_own_type(self):
        self.assertEqual(qas.invalid_own_type(
            wdpa_df, 
            True), 
            np.array([3,7]))

    def test_invalid_verif(self):
        self.assertEqual(qas.invalid_verif(
            wdpa_df, 
            True), 
            np.array([3,4,7]))

    def test_invalid_parent_iso3(self):
        self.assertEqual(qas.invalid_parent_iso3(
            wdpa_df, 
            True), 
            np.array([1,4,9]))

    def test_invalid_iso3(self):
        self.assertEqual(qas.invalid_iso3(
            wdpa_df, 
            True), 
            np.array([1,2,3]))

    def test_invalid_status_desig_type(self):
        self.assertEqual(qas.invalid_status_desig_type(
            wdpa_df, 
            True), 
            np.array([1,4,7,9]))

class TestAreaInvalid(unittest.TestCase):
    def test_area_invalid_no_tk_area_rep_m_area(self):
        self.assertEqual(qas.area_invalid_no_tk_area_rep_m_area(
            wdpa_df, 
            True), 
            np.array([3,5,7]))

    def test_area_invalid_no_tk_area_gis_m_area(self):
        self.assertEqual(qas.area_invalid_no_tk_area_gis_m_area(
            wdpa_df, 
            True), 
            np.array([1,2,5]))

    def test_area_invalid_gis_m_area_gis_area(self):
        self.assertEqual(qas.area_invalid_gis_m_area_gis_area(
            wdpa_df, 
            True), 
            np.array([2,5,8]))

    def test_area_invalid_rep_m_area_rep_area(self):
        self.assertEqual(qas.area_invalid_rep_m_area_rep_area(
            wdpa_df, 
            True), 
            np.array([2,7,9]))

class TestForbiddenCharacter(unittest.TestCase):
    def test_forbidden_character_name(self):
        self.assertEqual(qas.forbidden_character_name(
            wdpa_df, 
            True), 
            np.array([1,2,5,8,9,10]))

    def test_forbidden_character_orig_name(self):
        self.assertEqual(qas.forbidden_character_orig_name(
            wdpa_df, 
            True), 
            np.array([2,4,7,9]))

    def test_forbidden_character_desig(self):
        self.assertEqual(qas.forbidden_character_desig(
            wdpa_df, 
            True), 
            np.array([2,4,7,10]))

    def test_forbidden_character_desig_eng(self):
        self.assertEqual(qas.forbidden_character_desig_eng(
            wdpa_df, 
            True), 
            np.array([1,3,6]))

    def test_forbidden_character_mang_auth(self):
        self.assertEqual(qas.forbidden_character_mang_auth(
            wdpa_df, 
            True), 
            np.array([1,4,7]))

    def test_forbidden_character_mang_plan(self):
        self.assertEqual(qas.forbidden_character_mang_plan(
            wdpa_df, 
            True), 
            np.array([1,5,8,9]))

    def test_forbidden_character_sub_loc(self):
        self.assertEqual(qas.forbidden_character_sub_loc(
            wdpa_df, 
            True), 
            np.array([2,3,4,7]))

class TestMetadataid(unittest.TestCase):
    def test_invalid_metadataid_not_in_source_table_poly(self):
        self.assertEqual(qas.invalid_metadataid_not_in_source_table(
            wdpa_df = wdpa_df, 
            wdpa_source = wdpa_df, 
            return_pid=True), 
            np.array([1,2,3]))

    def test_invalid_metadataid_not_in_source_table_point(self):
        self.assertEqual(qas.invalid_metadataid_not_in_source_table(
            wdpa_df = wdpa_df, 
            wdpa_source = wdpa_df, 
            return_pid=True), 
            np.array([1,2,3]))

    def test_invalid_metadataid_not_in_wdpa(self):
        self.assertEqual(qas.invalid_metadataid_not_in_wdpa(
            wdpa_df = wdpa_df, 
            wdpa_point = wdpa_df, 
            wdpa_source = wdpa_df, 
            return_pid=True), 
            np.array([6,7,10,13,16,18,19,49,53]))


if __name__ == '__main__':
    unittest.main()