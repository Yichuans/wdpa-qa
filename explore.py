# QA for WDPA 2019
import numpy as np
import pandas as pd
import arcpy

wdpa = r'E:\Yichuan\WDPA\WDPA_May2016_Public.gdb\WDPA_poly_May2016'

fields = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
          'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
          'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
          'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 'PARENT_ISO3', 'ISO3', ]

# https://gist.github.com/d-wasserman/e9c98be1d0caebc2935afecf0ba239a0
def arcgis_table_to_df(in_fc, input_fields, query=""):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""

    OIDFieldName = arcpy.Describe(in_fc).OIDFieldName
    final_fields = [OIDFieldName] + input_fields
    data = [row for row in arcpy.da.SearchCursor(in_fc,final_fields,where_clause=query)]
    fc_dataframe = pd.DataFrame(data,columns=final_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName,drop=True)
    
    return fc_dataframe

# wdpa_df = arcgis_table_to_df(wdpa, fields)


# utility function: find rows of the WDPA based on the WDPA_PID
def find_wdpa_rows(wdpa_df, wdpa_pid):
    return wdpa_df[wdpa_df['WDPA_PID'].isin(wdpa_pid)]


# 1,2 check: if WDPA_PID unique
def check_unique_wdpa_pid(wdpa_df):
    return wdpa_df['WDPA_PID'].nunique() == wdpa_df.index.size

# 3 check: PA_DEF should all be 1
def check_pd_def_1(wdpa_df):
    pa_def = wdpa_df['PA_DEF'].unique()
    if pa_def.size == 1 and pa_def[0] == '1':
        return True
    else:
        return False

# 4 validation: for each WDPAID, cannot have more than 1 DESIG, find wdpa_pid
def wdpaid_desig(wdpa_df):
    wdpaid_desig_unique_count = wdpa_df.groupby('WDPAID').DESIG.nunique()

    wdpa_pid = wdpa_df[wdpa_df['WDPAID'].isin(wdpaid_desig_unique_count[wdpaid_desig_unique_count>1].index)]['WDPA_PID']
    return wdpa_pid

# 5 validation
def desig_type_desig(wdpa_df):
    # AP:
    return wdpa_pid