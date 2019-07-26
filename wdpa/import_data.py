#### QA for WDPA 2019 ####
'''
# Stijn den Haan
# Supervisor: Yichuan Shi
# Bioinformatics internship • UNEP-WCMC • 10 June --- 9 August 2019

### Action points

# 1. Invalid `ISO3` check could be improved by separating ISO3 values by ';' when comparing to list of allowed values

### Definitions 

**Offending fields** are fields (columns) that contain values that do not adhere to the rules set in the WDPA manual.
- Offending fields are subdivided in **three types**:
    - *Duplicate*: records holding exactly the same values for all fields. Notably, the WDPA_PID field should not hold duplicates.
    - *Inconsistent*: multiple records (rows) about the same protected area contains conflicting field information
        - Example: records with the same `WDPAID` have different values present in field `NAME`, e.g. 'De Veluwe' vs 'De VeLUwe'.
    - *Invalid*: a record has an incorrect value for a particular field where only a particular set of values is allowed.
        - Example: `DESIG_TYPE` = 'Individual' while only 'National', 'International', and 'Regional' are allowed values for this field.
    
In this document, we use:
- **field** to refer to a column of the database;
    - Example: `ISO3`
- **value** to refer to each individual entry present in a field - i.e. the intersection of the field and row.
    - Example: 12345 present in field `WDPAID` on row 12
'''

##### Load packages

import numpy as np
import pandas as pd
import arcpy
import datetime
import os

##### Load fields present in the WDPA tables

###### Polygon data

input_fields_poly = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                     'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                     'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
                     'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                     'PARENT_ISO3', 'ISO3', ]

###### Point data

input_fields_point = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                      'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                      'REP_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 'GOV_TYPE', 
                      'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                      'PARENT_ISO3', 'ISO3', ]

###### Source Table

input_fields_source = ['METADATAID','DATA_TITLE','RESP_PARTY','VERIFIER','YEAR',
                       'UPDATE_YR', 'LANGUAGE','CHAR_SET','REF_SYSTEM', 'SCALE', 
                       'LINEAGE', 'CITATION','DISCLAIMER', ]

#####################################################
#### 1. Convert ArcGIS table to pandas DataFrame ####
#####################################################

# Use this for the Polygons, Points, and the Source Table

# Source: https://gist.github.com/d-wasserman/e9c98be1d0caebc2935afecf0ba239a0
def arcgis_table_to_df(in_fc, workspace_gdb input_fields, query=''):
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

## Use function and assign WDPA tables to variables ##
# wdpa_df = arcgis_table_to_df(wdpa, input_fields_poly)

## Same variable name for the point data? 
# wdpa_df = arcgis_table_to_df(wdpa, input_fields_point)

## Different name for WDPA Source Table
# wdpa_source = arcgis_table_to_df(wdpa, input_fields_source)

#########################################
##### 1.1 Obtain allowed ISO3 values ####
#########################################

column_with_iso3 = ['alpha-3']
url = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv'

# Store the ISO3 values into a Pandas DataFrame for later use
iso3_df = pd.read_csv(url, usecols = column_with_iso3)

###########################################################
#### 1.2. Verify that the imported data is as expected ####
###########################################################

def invalid_data_import(wdpa_df, wdpa_df_point, wdpa_source, input_fields_poly, input_fields_point, input_fields_source):
    '''
    Return True if any of the WDPA tables imported does not contain all expected fields, or is in the wrong order.
    This test is order-sensitive: if the fields are present but in the wrong order, 
    ''' 

    return (list(wdpa_df) != input_fields_poly) | (list(wdpa_df_point) != input_fields_point) | (list(wdpa_source) != input_fields_source)