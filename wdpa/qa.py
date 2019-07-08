# QA for WDPA 2019
import numpy as np
import pandas as pd
import arcpy

wdpa_fields = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
          'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
          'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
          'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 'PARENT_ISO3', 'ISO3', ]

def arcgis_table_to_df(in_fc, input_fields, query=""):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""

    OIDFieldName = arcpy.Describe(in_fc).OIDFieldName
    final_fields = [OIDFieldName] + input_fields
    data = [row for row in arcpy.da.SearchCursor(in_fc,final_fields,where_clause=query)]
    fc_dataframe = pd.DataFrame(data,columns=final_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName,drop=True)

    return fc_dataframe

