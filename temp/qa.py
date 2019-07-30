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


# == Utility ==
# find rows of the WDPA based on the WDPA_PID
def find_wdpa_rows(wdpa_df, wdpa_pid):
    '''
    Return a subset of dataframe based on wdpa_pid list

    Arguments:
    wdpa_df -- wdpa dataframe
    wdpa_pid -- a list of WDPA_PID
    '''
    return wdpa_df[wdpa_df['WDPA_PID'].isin(wdpa_pid)]


# == Check ==
# check validality should be implemented as efficiently as possible, to avoid having to pull out all 'offending' rows when return_pid is set to true

def duplicate_wdpa_pid(wdpa_df, return_pid=False):
    '''
    Return True if WDPA_PID is duplicate in the dataframe. 
    
    Return list of WDPAID_PID, if duplicates are present and return_pid is set True, 
    '''

    if return_pid:
        pid_list = list()

        # AP return PID
        
        return pid_list

    return wdpa_df['WDPA_PID'].nunique() != wdpa_df.index.size

# == inconsistent values for the same WDPAID ==

def inconsistent_attributes_same_wdpaid(wdpa_df, check_attribute, return_pid=False):
    '''
    Return True if inconsistent attributes are found for rows sharing the same WDPAID

    Return list of WDPA_PID where inconsistency occurs, if return_pid is set True

    Arguments:
    check_attributes -- list of attributes to check inconsistency
    '''

    # this function can be repurposed
    return 

def inconsistent_desig_same_wdpaid(wdpa_df, return_pid=False):
    '''

    '''

    check_attributes = 'DESIG'
    return inconsistent_attributes_same_wdpaid(wdpa_df, return_pid, check_attributes)

def inconsistent_desig_eng_same_wdpaid(wdpa_df, return_pid=False):
    return

def inconsistent_name_same_wdpaid(wdpa_df, return_pid=False):
    return

def inconsistent_mang_auth_wdpaid(wdpa_df, return_pid=False):
    return

def inconsistent_plan_wdpaid(wdpa_df, return_pid=False):
    return


# == invalid values identified in the field ==

def invalid_value_in_field(wdpa_df, field, field_allowed_values, condition, return_pid=False):
    '''
    Return True if invalid values are found in field rows sharing the same WDPAID

    Return list of WDPA_PID where inconsistency occurs, if return_pid is set True

    Arguments:
    field -- in which invalid values are checked
    field_allowed_values -- expected values, case sensitive
    condition -- a constraint of another field for evaluating invalid value , leave "" if no condition specified

    Example:
    invalid_value_in_field(wdpa_df, 'DESIG_ENG',
    field_allowed_values=["Ramsar Site, Wetland of International Importance", "UNESCO-MAB Biosphere Reserve", "World Heritage Site (natural or mixed],
    condition=("DESIG_TYPE", "International"), 
    return_pid=True)
    '''
    # This generic function can be repurposed to specific functions

    return

def invalid_iucn_cat(wdpa_df, return_pid=False):
    
    field = 'IUCN_CAT'
    field_allowed_values = ["Ia", "Ib", "II", "III", "IV", "V", "VI", "Not Reported", "Not Applicable", "Not Assigned"]
    condition = ''

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition, return_pid)

def invalid_pa_def(wdpa_df, return_pid=False):
    '''
    Return True if PA_DEF not 1

    Return list of WDPA_PID where PA_DEF is not 1, if return_pid is set True

    '''
    field = 'PA_DEF'
    field_allowed_values = [1]
    condition = ''

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition, return_pid)

def invalid_desig_type(wdpa_df, return_pid=False):
    return

def invalid_desig_eng_regional(wdpa_df, return_pid=False):
    return

def invalid_desig_eng_international(wdpa_df, return_pid=False):
    return

def invalid_desig_eng_int_crit(wdpa_df, return_pid=False):
    return

def invalid_marine(wdpa_df, return_pid=False):
    return

def invalid_status(wdpa_df, return_pid=False):
    return

def invalid_status_yr(wdpa_df, return_pid=False):
    return

def invalid_gov_type(wdpa_df, return_pid=False):
    return

def invalid_own_type(wdpa_df, return_pid=False):
    return

def invalid_verif(wdpa_df, return_pid=False):
    return

def invalid_metadataid(wdpa_df, return_pid=False):
    return

def invalid_gis_area(wdpa_df, return_pid=False):
    '''
    Return list of WDPA_PID where value small GIS_AREA are present 
    '''
    return 

def invalid_int_crit(wdpa_df, return_pid=False):
    '''
    Return list of WDPA_PID where invalid characters (space, comma), are present 
    '''   
    return

# == Marine ==
# hard code the rules for marine fields
def invalid_marine_areas(wdpa_df, return_pid=False):
    # all areal inconsistency to be pickup here and specified
    return

def invalid_no_take(wdpa_df, return_pid=False):
    # no take and no take are
    return