# Test attributes
# Stijn den Haan
# 29 July 2019

import unittest as unittest
from wdpa import qas
import arcpy
import pandas as pd
import numpy as np
import os

# Set working directory
os.chdir(r"C:\Users\paintern\Desktop\Stijn\3. Data\Test data + bug")

# Load fields of the WDPA - polygon table
input_fields_poly = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                     'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                     'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
                     'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                     'PARENT_ISO3', 'ISO3', ]

# Load data

def arcgis_table_to_df(in_fc, workspace_gdb, input_fields, query=''):
    '''
    Function will convert an arcgis table into a pandas DataFrame with an OBJECTID index, and the selected
    input fields using an arcpy.da.SearchCursor.
    '''

    arcpy.env.workspace = workspace_gdb # set workspace (e.g. 'WDPA_Jun2019_Public.gdb')
    OIDFieldName = arcpy.Describe(in_fc).OIDFieldName # obtain OBJECTID field
    final_fields = [OIDFieldName] + input_fields # Make a list of all fields that need to be extracted
    data = [row for row in arcpy.da.SearchCursor(in_fc,final_fields,where_clause=query)] # for all fields, obtain all rows
    fc_dataframe = pd.DataFrame(data,columns=final_fields) # Put data into pandas DataFrame
    fc_dataframe = fc_dataframe.set_index(OIDFieldName,drop=True) # set OBJECTID as index, but no longer use it as column
    
    return fc_dataframe

wdpa_df = arcgis_table_to_df(in_fc = "test", 
                             workspace_gdb = "WDPA_Jun2019_Public.gdb", 
                             input_fields = input_fields_poly, 
                             query='')


############################
#### 1. Load dummy data ####
############################

# The dummy data that is loaded to test the code, 
# was created using Excel.

## AP: create class to test data import and utility functions below?
#def test_arcgis_table_to_df
#def test_invalid_data_import
#def test_find_wdpa_rows


class TestInvalid(unittest.TestCase):
    def test_invalid_pa_def(self):
        self.assertEqual(qas.invalid_pa_def(wdpa_df, 
            True), 
            ['9421'])

if __name__ == '__main__':
    unittest.main()