#### QA for WDPA 2019 ####
'''
Author: Stijn den Haan
Supervisor: Yichuan Shi
Bioinformatics internship • UNEP-WCMC • 10 June --- 9 August 2019

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

###########################################
##### 0. Load packages and WDPA fields ####
###########################################

## Load packages

import numpy as np
import pandas as pd
import arcpy
import datetime
import os

#### Load fields present in the WDPA tables ####

## Polygon data

input_fields_poly = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                     'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                     'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
                     'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                     'PARENT_ISO3', 'ISO3', ]

## Point data

input_fields_point = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                      'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                      'REP_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 'GOV_TYPE', 
                      'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                      'PARENT_ISO3', 'ISO3', ]

## Source Table

input_fields_source = ['METADATAID','DATA_TITLE','RESP_PARTY','VERIFIER','YEAR',
                       'UPDATE_YR', 'LANGUAGE','CHAR_SET','REF_SYSTEM', 'SCALE', 
                       'LINEAGE', 'CITATION','DISCLAIMER', ]

#####################################################
#### 1. Convert ArcGIS table to pandas DataFrame ####
#####################################################

# Use this for the Polygons, Points, and the Source Table

# Source: https://gist.github.com/d-wasserman/e9c98be1d0caebc2935afecf0ba239a0
def arcgis_table_to_df(in_fc, input_fields, query=''):
    '''
    Function will convert an arcgis table into a pandas DataFrame with an OBJECTID index, and the selected
    input fields using an arcpy.da.SearchCursor.
    For in_fc, specify the name of the geodatabase (.gdb) and feature class attribute table
    
    ## Arguments ##
    in_fc -- feature class attribute table - inside geodatabase - to import. 
             Specify: <nameOfGeodatabase>/<nameOfFeatureClassAttributeTable>
    input_fields -- list of all fields that must be imported from the dataset
    query -- optional where_clause of arcpy.da.SearchCursor. Leave default for normal usage.

    ## Example ##
    arcgis_table_to_df(in_fc='WDPA_Jun2019_Public.gdb/WDPA_Jun2019_errortest',
    input_fields=input_fields_poly,
    query='')
    '''

    OIDFieldName = arcpy.Describe(in_fc).OIDFieldName # obtain OBJECTID field.
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


#######################################
#### 2. Utility & hardcoded checks ####
#######################################

#############################################################################
#### 2.0. Utility to extract rows from the WDPA, based on WDPA_PID input ####
#############################################################################

def find_wdpa_rows(wdpa_df, wdpa_pid):
    '''
    Return a subset of dataframe based on wdpa_pid list

    Arguments:
    wdpa_df -- wdpa dataframe
    wdpa_pid -- a list of WDPA_PID
    '''
    
    return wdpa_df[wdpa_df['WDPA_PID'].isin(wdpa_pid)]
	
###################################
#### 2.1. Find NaN / NULL / NA ####
###################################

def invalid_nan(wdpa_df, return_field, return_pid=False):
    '''
    Return True if there is one or more NaNs present in the WDPA
    Return list of WDPA_PIDs in which a value contains NaN
    Specify return_field as either 'WDPA_PID' (to check WDPA) 
    or 'METADATAID' (to check Source Table)
    '''

    invalid_wdpa_pid = wdpa_df[wdpa_df.isnull().values][return_field].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

#######################################
#### 2.2. Find duplicate WDPA_PIDs ####
#######################################

def duplicate_wdpa_pid(wdpa_df, return_pid=False):
    '''
    Return True if WDPA_PID is duplicate in the DataFrame. 
    Return list of WDPA_PID, if duplicates are present 
    and return_pid is set True.
    '''

    if return_pid:
        ids = wdpa_df['WDPA_PID'] # make a variable of the field to find
        return ids[ids.duplicated()].unique() # return duplicate WDPA_PIDs

    return wdpa_df['WDPA_PID'].nunique() != wdpa_df.index.size # this returns True if there are WDPA_PID duplicates

###########################################################################
#### 2.3. Invalid: MARINE designation based on GIS_AREA and GIS_M_AREA ####
###########################################################################

def area_invalid_marine(wdpa_df, return_pid=False):
    '''
    Assign a marine_value based on GIS calculations, return True if marine_value is unequal to MARINE
    Return list of WDPA_PIDs where MARINE is invalid, if return_pid is set True
    '''
    
    # set min and max for 'coastal' designation (MARINE = 1)
    coast_min = 0.1
    coast_max = 0.9
    
    # create new column with proportion marine vs total GIS area 
    wdpa_df['marine_proportion'] = wdpa_df['GIS_M_AREA'] / wdpa_df['GIS_AREA']
    
    def assign_marine_value(wdpa_df):
        if wdpa_df['marine_proportion'] <= coast_min:
            return '0'
        elif coast_min < wdpa_df['marine_proportion'] < coast_max:
            return '1'
        elif wdpa_df['marine_proportion'] >= coast_max:
            return '2'
    
    # calculate the marine_value
    wdpa_df['marine_value'] = wdpa_df.apply(assign_marine_value, axis=1)
    
    # find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[wdpa_df['marine_value'] != wdpa_df['MARINE']]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

############################################
#### 2.4. Invalid: GIS_AREA >> REP_AREA ####
############################################

def area_invalid_too_large_gis(wdpa_df, return_pid=False):
    '''
    Return True if GIS_AREA is too large compared to REP_AREA - based on thresholds specified below.
    Return list of WDPA_PIDs where GIS_AREA is too large compared to REP_AREA, if return_pid=True
    '''
    
    # Set maximum allowed absolute difference between GIS_AREA and REP_AREA (in km2)
    MAX_ALLOWED_SIZE_DIFF_KM2 = 50
    
    # Two columns need to be created: one to calculate the mean and stdev without outliers
    # and another to find WDPA_PIDs with a too large GIS_AREA
    
    # Column 1: replace outliers with NaN, then obtain mean and stdev
    calc =      (wdpa_df['REP_AREA'] + wdpa_df['GIS_AREA']) / wdpa_df['REP_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    wdpa_df['GIS_size_check_stats'] = np.select(condition, # produce column without outliers
                                         choice, 
                                         default = calc)

    # Column 2: to find WDPA_PIDs with too large GIS_AREA
    wdpa_df['GIS_size_check'] = (wdpa_df['REP_AREA'] + wdpa_df['GIS_AREA']) / wdpa_df['REP_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_size_check using mean and stdev
    MAX_GIS = wdpa_df['GIS_size_check_stats'].mean() + (2*wdpa_df['GIS_size_check_stats'].std())
    MIN_GIS = wdpa_df['GIS_size_check_stats'].mean() - (2*wdpa_df['GIS_size_check_stats'].std())

    # Find the rows with an incorrect GIS_AREA
    invalid_wdpa_pid = wdpa_df[((wdpa_df['GIS_size_check'] > MAX_GIS) | 
                       (wdpa_df['GIS_size_check'] < MIN_GIS)) &
                       (abs(wdpa_df['GIS_AREA']-wdpa_df['REP_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return len(invalid_wdpa_pid) >= 1

############################################
#### 2.5. Invalid: REP_AREA >> GIS_AREA ####
############################################

def area_invalid_too_large_rep(wdpa_df, return_pid=False):
    '''
    Return True if REP_AREA is too large compared to GIS_AREA - based on thresholds specified below.
    Return list of WDPA_PIDs where REP_AREA is too large compared to GIS_AREA, if return_pid=True
    '''
    
    # Set maximum allowed absolute difference between GIS_AREA and REP_AREA (in km2)
    MAX_ALLOWED_SIZE_DIFF_KM2 = 50
    
    # Two columns need to be created: one to calculate the mean and stdev without outliers
    # and another to find WDPA_PIDs with a too large REP_AREA
    
    # Column 1: replace outliers with NaN, then obtain mean and stdev
    calc =      (wdpa_df['REP_AREA'] + wdpa_df['GIS_AREA']) / wdpa_df['GIS_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    wdpa_df['REP_size_check_stats'] = np.select(condition, # produce column without outliers
                                          choice, 
                                          default = calc)

    # Column 2: to find WDPA_PIDs with too large REP_AREA
    wdpa_df['REP_size_check'] = (wdpa_df['REP_AREA'] + wdpa_df['GIS_AREA']) / wdpa_df['GIS_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_size_check using mean and stdev
    MAX_REP = wdpa_df['REP_size_check_stats'].mean() + (2*wdpa_df['REP_size_check_stats'].std())
    MIN_REP = wdpa_df['REP_size_check_stats'].mean() - (2*wdpa_df['REP_size_check_stats'].std())

    # Find the rows with an incorrect REP_AREA
    invalid_wdpa_pid = wdpa_df[((wdpa_df['REP_size_check'] > MAX_REP) | 
                       (wdpa_df['REP_size_check'] < MIN_REP)) &
                       (abs(wdpa_df['GIS_AREA']-wdpa_df['REP_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return len(invalid_wdpa_pid) >= 1

################################################
#### 2.6. Invalid: GIS_M_AREA >> REP_M_AREA ####
################################################

def area_invalid_too_large_gis_m(wdpa_df, return_pid=False):
    '''
    Return True if GIS_M_AREA is too large compared to REP_M_AREA - based on thresholds specified below.
    Return list of WDPA_PIDs where GIS_M_AREA is too large compared to REP_M_AREA, if return_pid=True
    '''
    
    # Set maximum allowed absolute difference between GIS_M_AREA and REP_M_AREA (in km2)
    MAX_ALLOWED_SIZE_DIFF_KM2 = 50
    
    # Two columns need to be created: one to calculate the mean and stdev without outliers
    # and another to find WDPA_PIDs with a too large GIS_M_AREA
    
    # Column 1: replace outliers with NaN, then obtain mean and stdev
    calc =      (wdpa_df['REP_M_AREA'] + wdpa_df['GIS_M_AREA']) / wdpa_df['REP_M_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    wdpa_df['GIS_M_size_check_stats'] = np.select(condition, # produce column without outliers
                                         choice, 
                                         default = calc)

    # Column 2: to find WDPA_PIDs with too large GIS_AREA
    wdpa_df['GIS_M_size_check'] = (wdpa_df['REP_M_AREA'] + wdpa_df['GIS_M_AREA']) / wdpa_df['REP_M_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_M_size_check using mean and stdev
    MAX_GIS = wdpa_df['GIS_M_size_check_stats'].mean() + (2*wdpa_df['GIS_M_size_check_stats'].std())
    MIN_GIS = wdpa_df['GIS_M_size_check_stats'].mean() - (2*wdpa_df['GIS_M_size_check_stats'].std())

    # Find the rows with an incorrect GIS_AREA
    invalid_wdpa_pid = wdpa_df[((wdpa_df['GIS_M_size_check'] > MAX_GIS) | 
                       (wdpa_df['GIS_M_size_check'] < MIN_GIS)) &
                       (abs(wdpa_df['GIS_M_AREA']-wdpa_df['REP_M_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return len(invalid_wdpa_pid) >= 1

################################################
#### 2.7. Invalid: REP_M_AREA >> GIS_M_AREA ####
################################################

def area_invalid_too_large_rep_m(wdpa_df, return_pid=False):
    '''
    Return True if REP_M_AREA is too large compared to GIS_M_AREA - based on thresholds specified below.
    Return list of WDPA_PIDs where REP_M_AREA is too large compared to GIS_M_AREA, if return_pid=True
    '''
    
    # Set maximum allowed absolute difference between GIS_M_AREA and REP_M_AREA (in km2)
    MAX_ALLOWED_SIZE_DIFF_KM2 = 50
    
    # Two columns need to be created: one to calculate the mean and stdev without outliers
    # and another to find WDPA_PIDs with a too large REP_M_AREA
    
    # Column 1: replace outliers with NaN, then obtain mean and stdev
    calc =      (wdpa_df['REP_M_AREA'] + wdpa_df['GIS_M_AREA']) / wdpa_df['GIS_M_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    wdpa_df['REP_M_size_check_stats'] = np.select(condition, # produce column without outliers
                                          choice, 
                                          default = calc)

    # Column 2: to find WDPA_PIDs with too large REP_M_AREA
    wdpa_df['REP_M_size_check'] = (wdpa_df['REP_M_AREA'] + wdpa_df['GIS_M_AREA']) / wdpa_df['GIS_M_AREA']
    
    # Calculate the maximum and minimum allowed values for REP_M_size_check using mean and stdev
    MAX_REP = wdpa_df['REP_M_size_check_stats'].mean() + (2*wdpa_df['REP_M_size_check_stats'].std())
    MIN_REP = wdpa_df['REP_M_size_check_stats'].mean() - (2*wdpa_df['REP_M_size_check_stats'].std())

    # Find the rows with an incorrect REP_M_AREA
    invalid_wdpa_pid = wdpa_df[((wdpa_df['REP_M_size_check'] > MAX_REP) | 
                       (wdpa_df['REP_M_size_check'] < MIN_REP)) &
                       (abs(wdpa_df['GIS_M_AREA']-wdpa_df['REP_M_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return len(invalid_wdpa_pid) >= 1

#######################################################
#### 2.8. Invalid: GIS_AREA <= 0.0001 km² (100 m²) ####
#######################################################

def area_invalid_gis_area(wdpa_df, return_pid=False):
    '''
    Return True if GIS_AREA is smaller than 0.0001 km²
    Return list of WDPA_PIDs where GIS_AREA is smaller than 0.0001 km², if return_pid=True
    '''
    
    # Arguments
    size_threshold = 0.0001
    field_gis_area = ['GIS_AREA']
    
    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[wdpa_df[field_gis_area[0]] <= size_threshold]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

############################################################
#### 2.9. Invalid: REP_M_AREA <= 0 when MARINE = 1 or 2 ####
############################################################

def area_invalid_rep_m_area_marine12(wdpa_df, return_pid=False):
    '''
    Return True if REP_M_AREA is smaller than or equal to 0 while MARINE = 1 or 2
    Return list of WDPA_PIDs where REP_M_AREA is invalid, if return_pid=True
    '''
    
    # Arguments
    field = ['REP_M_AREA']
    field_allowed_values = [0]
    condition_field = ['MARINE']
    condition_crit = ['1','2']
    
    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[(wdpa_df[field[0]] <= field_allowed_values[0]) & 
                               wdpa_df[condition_field[0]].isin(condition_crit)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

##########################################################
## 2.10. Invalid: GIS_M_AREA <= 0 when MARINE = 1 or 2 ####
##########################################################

def area_invalid_gis_m_area_marine12(wdpa_df, return_pid=False):
    '''
    Return True if GIS_M_AREA is smaller than or equal to 0 while MARINE = 1 or 2
    Return list of WDPA_PIDs where GIS_M_AREA is invalid, if return_pid=True
    '''
    
    # Arguments
    field = ['GIS_M_AREA']
    field_allowed_values = [0]
    condition_field = ['MARINE']
    condition_crit = ['1','2']
    
    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[(wdpa_df[field[0]] <= field_allowed_values[0]) & 
                               wdpa_df[condition_field[0]].isin(condition_crit)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
        
    return len(invalid_wdpa_pid) >= 1

########################################################
## 2.11. Invalid: NO_TAKE, NO_TK_AREA and REP_M_AREA ####
########################################################

def invalid_no_take_no_tk_area_rep_m_area(wdpa_df, return_pid=False):
    '''
    Return True if NO_TAKE = 'All' while the REP_M_AREA is unequal to NO_TK_AREA
    Return list of WDPA_PIDs where NO_TAKE is invalid, if return_pid=True
    '''

    # Select rows with NO_TAKE = 'All'
    no_take_all = wdpa_df[wdpa_df['NO_TAKE']=='All']
    
    # Select rows where the REP_M_AREA is unequal to NO_TK_AREA
    invalid_wdpa_pid = no_take_all[no_take_all['REP_M_AREA'] != no_take_all['NO_TK_AREA']]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

############################################################################
## 2.12. Invalid: INT_CRIT & DESIG_ENG - non-Ramsar Site, non-WHS sites ####
############################################################################

def invalid_int_crit_desig_eng_other(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_ENG is something else than Ramsar Site (...)' or 'World Heritage Site (...)'
    while INT_CRIT is unequal to 'Not Applicable'. Other-than Ramsar / WHS should not contain anything
    else than 'Not Applicable'.
    Return list of WDPA_PIDs where INT_CRIT is invalid, if return_pid is set True
    '''
    
    # Arguments
    field = ['DESIG_ENG']
    field_allowed_values = ['Ramsar Site, Wetland of International Importance', 
                            'World Heritage Site (natural or mixed)']
    condition_field = ['INT_CRIT']
    condition_crit = ['Not Applicable']
    
    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(field_allowed_values) &
                               ~wdpa_df[condition_field[0]].isin(condition_crit)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

#########################################################################
#### 2.13. Invalid: DESIG_ENG & IUCN_CAT - non-UNESCO, non-WHS sites ####
#########################################################################

def invalid_desig_eng_iucn_cat_other(wdpa_df, return_pid=False):
    '''
    Return True if IUCN_CAT is unequal to the allowed values
    and DESIG_ENG is unequal to 'UNESCO-MAB (...)' or 'World Heritage Site (...)'
    Return list of WDPA_PIDs where IUCN_CAT is invalid, if return_pid is set True
    '''

    # Arguments
    field = ['IUCN_CAT']
    field_allowed_values = ['Ia',
                            'Ib',
                            'II',
                            'III',
                            'IV',
                            'V',
                            'VI',
                            'Not Reported',
                            'Not Assigned']
    condition_field = ['DESIG_ENG']
    condition_crit = ['UNESCO-MAB Biosphere Reserve', 
                      'World Heritage Site (natural or mixed)']
    
    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(field_allowed_values) &
                               ~wdpa_df[condition_field[0]].isin(condition_crit)]['WDPA_PID'].values

    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

#########################################################
#### 3. Find inconsistent fields for the same WDPAID ####
#########################################################

#### Parent function ####

def inconsistent_fields_same_wdpaid(wdpa_df, 
                                        check_fields, 
                                        return_pid=False):
    '''
    Factory of functions: this generic function is to be linked to
    the family of 'inconsistent' functions stated below. These latter 
    functions are to give information on which fields to check and pull 
    from the DataFrame. This function is the foundation of the others.
    
    Return True if inconsistent Fields are found for rows 
    sharing the same WDPAID

    Return list of WDPA_PID where inconsistencies occur, if 
    return_pid is set True

    ## Arguments ##
    check_fields -- list of the field(s) to check for inconsistency
    
    ## Example ##
    inconsistent_fields_same_wdpaid(
        wdpa_df=wdpa_df,
        check_fields=["DESIG_ENG"],
        return_pid=True):    
    '''

    if return_pid:
        # Group by WDPAID to find duplicate WDPAIDs and count the 
        # number of unique values for the field in question
        wdpaid_groups = wdpa_df.groupby(['WDPAID'])[check_fields[0]].nunique()

        # Select all WDPAID duplicates groups with >1 unique value for 
        # specified field ('check_attributtes') and use their index to
        # return the WDPA_PIDs
        return wdpa_df[wdpa_df['WDPAID'].isin(wdpaid_groups[wdpaid_groups >1].index)]['WDPA_PID'].values
                
    # Sum the number of times a WDPAID has more than 1 value for a field
    return (wdpa_df.groupby('WDPAID')[check_fields].nunique() > 1).sum() >= 1
	

#### Child functions ####

#################################
#### 3.1. Inconsistent NAME #####
#################################

def inconsistent_name_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'NAME'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''

    check_fields = ['NAME']
    
    # The command below loads the parent function
    # and adds the check_fields and return_pid arguments in it
    # to evaluate the wdpa_df for these arguments
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)
	
#####################################
#### 3.2. Inconsistent ORIG_NAME ####
#####################################

def inconsistent_orig_name_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'ORIG_NAME'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''

    check_fields = ['ORIG_NAME']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

#################################	
#### 3.3. Inconsistent DESIG ####
#################################

def inconsistent_desig_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'DESIG'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    
    check_fields = ['DESIG']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)
	
#####################################
#### 3.4. Inconsistent DESIG_ENG ####
#####################################

def inconsistent_desig_eng_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'DESIG_ENG'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    
    check_fields = ['DESIG_ENG']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

######################################
#### 3.5. Inconsistent DESIG_TYPE ####
######################################

def inconsistent_desig_type_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'DESIG_TYPE'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    
    check_fields = ['DESIG_TYPE']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

####################################
#### 3.6. Inconsistent IUCN_CAT ####
####################################

def inconsistent_iucn_cat_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'IUCN_CAT'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''

    check_fields = ['IUCN_CAT']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

####################################
#### 3.7. Inconsistent INT_CRIT ####
####################################

def inconsistent_int_crit_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'INT_CRIT'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''

    check_fields = ['INT_CRIT']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

###################################
#### 3.8. Inconsistent NO_TAKE ####
###################################

def inconsistent_no_take_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'NO_TAKE'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['NO_TAKE']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

##################################
#### 3.9. Inconsistent STATUS ####
##################################

def inconsistent_status_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'STATUS'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['STATUS']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

######################################
#### 3.10. Inconsistent STATUS_YR ####
######################################

def inconsistent_status_yr_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'STATUS_YR'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['STATUS_YR']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

#####################################
#### 3.11. Inconsistent GOV_TYPE ####
#####################################

def inconsistent_gov_type_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'GOV_TYPE'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['GOV_TYPE']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

#####################################
#### 3.12. Inconsistent OWN_TYPE ####
#####################################

def inconsistent_own_type_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'OWN_TYPE'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['OWN_TYPE']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

######################################
#### 3.13. Inconsistent MANG_AUTH ####
######################################

def inconsistent_mang_auth_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'MANG_AUTH'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    
    check_fields = ['MANG_AUTH']
    
    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

######################################
#### 3.14. Inconsistent MANG_PLAN ####
######################################

def inconsistent_mang_plan_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'MANG_PLAN'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['MANG_PLAN']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

##################################
#### 3.15. Inconsistent VERIF ####
##################################

def inconsistent_verif_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'VERIF'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['VERIF']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

#######################################
#### 3.16. Inconsistent METADATAID ####
#######################################

def inconsistent_metadataid_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'METADATAID'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['METADATAID']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

###################################
#### 3.17 Inconsistent SUB_LOC ####
###################################

def inconsistent_sub_loc_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'SUB_LOC'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['SUB_LOC']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

#######################################
### 3.18. Inconsistent PARENT_ISO3 ####
#######################################

def inconsistent_parent_iso3_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'PARENT_ISO3'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['PARENT_ISO3']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)

################################
#### 3.19 Inconsistent ISO3 ####
################################


def inconsistent_iso3_same_wdpaid(wdpa_df, return_pid=False):
    '''
    This function is to capture inconsistencies in the field 'ISO3'
    for records with the same WDPAID
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing field inconsistencies
    '''
    check_fields = ['ISO3']

    return inconsistent_fields_same_wdpaid(wdpa_df, check_fields, return_pid)
	
##########################################
#### 4. Find invalid values in fields ####
##########################################

#### Parent function ####

def invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid=False):
    '''
    This function checks the WDPA for invalid values and returns a list of WDPA_PIDs 
    that have invalid values for the specified field(s).
    
    This function is to be linked to the family of 'invalid field'-checking functions. 
    These latter functions give specific information on the fields to be checked, and how.
        
    Return True if invalid values are found in specified fields
    Return list of WDPA_PIDs with invalid fields, if return_pid is set True

    ## Arguments ##
    
    field                -- the field to be checked for invalid values, in a list
    field_allowed_values -- a list of expected values in each field, case sensitive
    condition_field      -- a constraint of another field for evaluating 
                            invalid values, in list; leave "" if no condition specified
    condition_crit       -- a list of values for which the condition_field 
                            needs to be evaluated; leave "" if no condition specified

    ## Example ##
    invalid_value_in_field(
        wdpa_df,
        field=["DESIG_ENG"],
        field_allowed_values=["Ramsar Site, Wetland of International Importance", 
                              "UNESCO-MAB Biosphere Reserve", 
                              "World Heritage Site (natural or mixed)],
        condition_field=["DESIG_TYPE"],
        condition_crit=["International"],
        return_pid=True):
    '''

    if field and field_allowed_values and condition_field and condition_crit:
        invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(field_allowed_values) & 
                           wdpa_df[condition_field[0]].isin(condition_crit)]['WDPA_PID'].values

    # If no condition_field and condition_crit are specified
    else:
        if field and field_allowed_values:
            invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(field_allowed_values)]['WDPA_PID'].values
        else: 
            raise Exception('ERROR: field(s) and/or condition(s) to test are not specified')
            
    if return_pid:
        # return list with invalid WDPA_PIDs
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1
	
#### Child functions ####

#############################
#### 4.1. Invalid PA_DEF ####
#############################

def invalid_pa_def(wdpa_df, return_pid=False):
    '''
    Return True if PA_DEF not 1
    Return list of WDPA_PIDs where PA_DEF is not 1, if return_pid is set True
    '''

    field = ['PA_DEF']
    field_allowed_values = ['1'] # WDPA datatype is string
    condition_field = []
    condition_crit = []

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

################################################
#### 4.2. Invalid DESIG_ENG - international ####
################################################

def invalid_desig_eng_international(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_ENG is invalid while DESIG_TYPE is 'International'
    Return list of WDPA_PIDs where DESIG_ENG is invalid, if return_pid is set True
    '''
    
    field = ['DESIG_ENG']
    field_allowed_values = ['Ramsar Site, Wetland of International Importance', 
                            'UNESCO-MAB Biosphere Reserve', 
                            'World Heritage Site (natural or mixed)']
    condition_field = ['DESIG_TYPE']
    condition_crit = ['International']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

#################################################
#### 4.3. Invalid DESIG_TYPE - international ####
#################################################

def invalid_desig_type_international(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_TYPE is unequal to 'International', while DESIG_ENG is an allowed 'International' value
    Return list of WDPA_PIDs where DESIG_TYPE is invalid, if return_pid is set True
    '''
    
    field = ['DESIG_TYPE']
    field_allowed_values = ['International']
    condition_field = ['DESIG_ENG']
    condition_crit = ['Ramsar Site, Wetland of International Importance', 
                      'UNESCO-MAB Biosphere Reserve', 
                      'World Heritage Site (natural or mixed)']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)


###########################################
#### 4.4. Invalid DESIG_ENG - regional ####
###########################################

def invalid_desig_eng_regional(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_ENG is invalid while DESIG_TYPE is 'Regional'
    Return list of WDPA_PIDs where DESIG_ENG is invalid, if return_pid is set True
    '''
    
    field = ['DESIG_ENG']
    field_allowed_values = ['Baltic Sea Protected Area (HELCOM)', 
                            'Specially Protected Area (Cartagena Convention)', 
                            'Marine Protected Area (CCAMLR)', 
                            'Marine Protected Area (OSPAR)', 
                            'Site of Community Importance (Habitats Directive)', 
                            'Special Protection Area (Birds Directive)', 
                            'Specially Protected Areas of Mediterranean Importance (Barcelona Convention)']
    condition_field = ['DESIG_TYPE']
    condition_crit = ['Regional']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

###########################################
#### 4.5. Invalid DESIG_TYPE - regional ###
###########################################

def invalid_desig_type_regional(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_TYPE is unequal to 'Regional' while DESIG_ENG is an allowed 'Regional' value
    Return list of WDPA_PIDs where DESIG_TYPE is invalid, if return_pid is set True
    '''
    
    field = ['DESIG_TYPE']
    field_allowed_values = ['Regional']
    condition_field = ['DESIG_ENG']
    condition_crit = ['Baltic Sea Protected Area (HELCOM)', 
                      'Specially Protected Area (Cartagena Convention)', 
                      'Marine Protected Area (CCAMLR)', 
                      'Marine Protected Area (OSPAR)', 
                      'Site of Community Importance (Habitats Directive)', 
                      'Special Protection Area (Birds Directive)', 
                      'Specially Protected Areas of Mediterranean Importance (Barcelona Convention)']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)


#################################################################################
#### 4.6. Invalid INT_CRIT & DESIG_ENG  - Ramsar Site & World Heritage Sites ####
#################################################################################

def invalid_int_crit_desig_eng_ramsar_whs(wdpa_df, return_pid=False):
    '''
    Return True if INT_CRIT is unequal to the allowed values (>1000 possible values) 
    and DESIG_ENG equals 'Ramsar Site (...)' or 'World Heritage Site (...)'
    Return list of WDPA_PIDs where INT_CRIT is invalid, if return_pid is set True
    '''
    
    # Function to create the possible INT_CRIT combination
    def generate_combinations():
        import itertools
        collection = []
        INT_CRIT_ELEMENTS = ['(i)','(ii)','(iii)','(iv)',
                             '(v)','(vi)','(vii)','(viii)',
                             '(ix)','(x)']
        for length_combi in range(1, len(INT_CRIT_ELEMENTS)+1): # for 1 - 10 elements
            for combi in itertools.combinations(INT_CRIT_ELEMENTS, length_combi): # generate combinations
                collection.append(''.join(combi)) # append to list, remove the '' in each combination
        return collection
   
    # Arguments
    field = ['INT_CRIT']
    field_allowed_values_extra = ['Not Reported']
    field_allowed_values =  generate_combinations() + field_allowed_values_extra
    condition_field = ['DESIG_ENG']
    condition_crit = ['Ramsar Site, Wetland of International Importance', 
                      'World Heritage Site (natural or mixed)']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

#################################
#### 4.7. Invalid DESIG_TYPE ####
#################################

def invalid_desig_type(wdpa_df, return_pid=False):
    '''
    Return True if DESIG_TYPE is not "National", "Regional", "International" or "Not Applicable"
    Return list of WDPA_PIDs where DESIG_TYPE is invalid, if return_pid is set True
    '''

    field = ['DESIG_TYPE']
    field_allowed_values = ['National', 
                            'Regional', 
                            'International', 
                            'Not Applicable']
    condition_field = []
    condition_crit = []

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

###############################
#### 4.8. Invalid IUCN_CAT ####
###############################

def invalid_iucn_cat(wdpa_df, return_pid=False):
    '''
    Return True if IUCN_CAT is not equal to allowed values
    Return list of WDPA_PIDs where IUCN_CAT is invalid, if return_pid is set True
    '''
    
    field = ['IUCN_CAT']
    field_allowed_values = ['Ia', 'Ib', 'II', 'III', 
                            'IV', 'V', 'VI', 
                            'Not Reported', 
                            'Not Applicable', 
                            'Not Assigned']
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

#####################################################################
#### 4.9. Invalid IUCN_CAT - UNESCO-MAB and World Heritage Sites ####
#####################################################################

def invalid_iucn_cat_unesco_whs(wdpa_df, return_pid=False):
    '''
    Return True if IUCN_CAT is unqueal to 'Not Applicable' 
    and DESIG_ENG is 'UNESCO-MAB (...)' or 'World Heritage Site (...)'
    Return list of WDPA_PIDs where IUCN_CAT is invalid, if return_pid is set True
    '''
    
    field = ['IUCN_CAT']
    field_allowed_values = ['Not Applicable']
    condition_field = ['DESIG_ENG']
    condition_crit = ['UNESCO-MAB Biosphere Reserve', 
                      'World Heritage Site (natural or mixed)']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

##############################
#### 4.10. Invalid MARINE ####
##############################

def invalid_marine(wdpa_df, return_pid=False):
    '''
    Return True if MARINE is not in [0,1,2]
    Return list of WDPA_PIDs where MARINE is invalid, if return_pid is set True
    '''

    field = ['MARINE']
    field_allowed_values = ['0','1','2']
    condition_field = []
    condition_crit = []

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

############################################
#### 4.11. Invalid NO_TAKE & MARINE = 0 ####
############################################

def invalid_no_take_marine0(wdpa_df, return_pid=False):
    '''
    Return True if NO_TAKE is not equal to 'Not Applicable' and MARINE = 0
    Test whether terrestrial PAs (MARINE = 0) have a NO_TAKE other than 'Not Applicable'
    Return list of WDPA_PIDs where NO_TAKE is invalid, if return_pid is set True
    '''

    field = ['NO_TAKE']
    field_allowed_values = ['Not Applicable']
    condition_field = ['MARINE']
    condition_crit = ['0']

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

################################################
#### 4.12. Invalid NO_TAKE & MARINE = [1,2] ####
################################################

def invalid_no_take_marine12(wdpa_df, return_pid=False):
    '''
    Return True if NO_TAKE is not in ['All', 'Part', 'None', 'Not Reported'] while MARINE = [1, 2]
    I.e. check whether coastal and marine sites (MARINE = [1, 2]) have an invalid NO_TAKE value.
    Return list of WDPA_PIDs where NO_TAKE is invalid, if return_pid is set True
    '''

    field = ['NO_TAKE']
    field_allowed_values = ['All', 'Part', 'None', 'Not Reported']
    condition_field = ['MARINE']
    condition_crit = ['1', '2']

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

###########################################
#### 4.13. Invalid NO_TK_AREA & MARINE ####
###########################################

def invalid_no_tk_area_marine(wdpa_df, return_pid=False):
    '''
    Return True if NO_TK_AREA is not in [0] while MARINE = [0]
    I.e. check whether NO_TK_AREA is unequal to 0 for terrestrial PAs.
    Return list of WDPA_PIDs where NO_TAKE is invalid, if return_pid is set True
    '''

    field = ['NO_TK_AREA']
    field_allowed_values = [0]
    condition_field = ['MARINE']
    condition_crit = ['0']

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

############################################
#### 4.14. Invalid NO_TK_AREA & NO_TAKE ####
############################################

def invalid_no_tk_area_no_take(wdpa_df, return_pid=False):
    '''
    Return True if NO_TK_AREA is not in [0] while NO_TAKE = 'Not Applicable'
    Return list of WDPA_PIDs where NO_TK_AREA is invalid, if return_pid is set True
    '''

    field = ['NO_TK_AREA']
    field_allowed_values = [0]
    condition_field = ['NO_TAKE']
    condition_crit = ['Not Applicable']

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

##############################
#### 4.15. Invalid STATUS ####
##############################

def invalid_status(wdpa_df, return_pid=False):
    '''
    Return True if STATUS is not in ["Proposed", "Inscribed", "Adopted", "Designated", "Established"]
    Return list of WDPA_PIDs where STATUS is invalid, if return_pid is set True
    '''

    field = ['STATUS']
    field_allowed_values = ['Proposed', 'Inscribed', 'Adopted', 'Designated', 'Established']
    condition_field = []
    condition_crit = []

    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

#################################
#### 4.16. Invalid STATUS_YR ####
#################################

def invalid_status_yr(wdpa_df, return_pid=False):
    '''
    Return True if STATUS_YR is unequal to 0 or any year between 1819 and the current year
    Return list of WDPA_PIDs where STATUS_YR is invalid, if return_pid is set True
    '''
    
    field = ['STATUS_YR']
    year = datetime.date.today().year # obtain current year
    yearArray = [0] + np.arange(1819, year + 1, 1).tolist() # make a list of all years, from 0 to current year
    field_allowed_values = [str(x) for x in yearArray] # change all integers to strings
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

################################
#### 4.17. Invalid GOV_TYPE ####
################################

def invalid_gov_type(wdpa_df, return_pid=False):
    '''
    Return True if GOV_TYPE is invalid
    Return list of WDPA_PIDs where GOV_TYPE is invalid, if return_pid is set True
    '''
    
    field = ['GOV_TYPE']
    field_allowed_values = ['Federal or national ministry or agency', 
                            'Sub-national ministry or agency', 
                            'Government-delegated management', 
                            'Transboundary governance', 
                            'Collaborative governance', 
                            'Joint governance', 
                            'Individual landowners', 
                            'Non-profit organisations', 
                            'For-profit organisations', 
                            'Indigenous peoples', 
                            'Local communities', 
                            'Not Reported']
    
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

################################
#### 4.18. Invalid OWN_TYPE ####
################################

def invalid_own_type(wdpa_df, return_pid=False):
    '''
    Return True if OWN_TYPE is invalid
    Return list of WDPA_PIDs where OWN_TYPE is invalid, if return_pid is set True
    '''
    
    field = ['OWN_TYPE']
    field_allowed_values = ['State', 
                            'Communal', 
                            'Individual landowners', 
                            'For-profit organisations', 
                            'Non-profit organisations', 
                            'Joint ownership', 
                            'Multiple ownership', 
                            'Contested', 
                            'Not Reported']
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

#############################
#### 4.19. Invalid VERIF ####
#############################

def invalid_verif(wdpa_df, return_pid=False):
    '''
    Return True if VERIF is invalid
    Return list of WDPA_PIDs where VERIF is invalid, if return_pid is set True
    '''
    
    field = ['VERIF']
    field_allowed_values = ['State Verified', 
                            'Expert Verified', 
                            'Not Reported']
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)
	
###################################
#### 4.20. Invalid PARENT_ISO3 ####
###################################
# AP: could be improved by separating the ISO3s by `;` and then check.

def invalid_parent_iso3(wdpa_df, return_pid=False):
    '''
    Return True if PARENT_ISO3 is not equal to any of the allowed ISO3 values
    Return list of WDPA_PIDs for which the PARENT_ISO3 is invalid
    '''
    
    field = ['PARENT_ISO3']
    field_allowed_values = iso3_df['alpha-3'].values
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

############################
#### 4.21. Invalid ISO3 ####
############################
# AP: could be improved by separating the ISO3s by `;` and then check.

def invalid_iso3(wdpa_df, return_pid=False):
    '''
    Return True if ISO3 is not equal to any of the allowed ISO3 values
    Return list of WDPA_PIDs for which the ISO3 is invalid
    '''
    
    field = ['ISO3']
    field_allowed_values = iso3_df['alpha-3'].values
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

###########################################
#### 4.22. Invalid STATUS & DESIG_TYPE ####
###########################################

def invalid_status_desig_type(wdpa_df, return_pid=False):
    '''
    Return True if STATUS is unequal to 'Established', while DESIG_TYPE = 'Not Applicable'
    Return list of WDPA_PIDs for which the STATUS is invalid
    '''

    field = ['STATUS']
    field_allowed_values = ['Established']
    condition_field = ['DESIG_TYPE']
    condition_crit = ['Not Applicable']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

###############################################################
#### 5. Area invalid size: GIS or Reported area is invalid ####
###############################################################

#### Parent function ####

def area_invalid_size(wdpa_df, field_small_area, field_large_area, return_pid=False):
    '''
    Factory of functions: this generic function is to be linked to
    the family of 'area' functions stated below. These latter 
    functions are to give information on which fields to check and pull 
    from the DataFrame. This function is the foundation of the others.
    
    Return True if the size of the small_area is invalid compared to large_area

    Return list of WDPA_PIDs where small_area is invalid compared to large_area,
    if return_pid is set True

    ## Arguments ##
    field_small_area  -- list of the field to check for size - supposedly smaller
    field_large_area  -- list of the field to check for size - supposedly larger
    
    ## Example ##
    area_invalid_size(
        wdpa_df,
        field_small_area=["GIS_M_AREA"],
        field_large_area=["GIS_AREA"],
        return_pid=True):
    '''
    
    size_threshold = 1.0001 # due to the rounding of numbers, there are many false positives without a threshold.

    if field_small_area and field_large_area:
        invalid_wdpa_pid = wdpa_df[wdpa_df[field_small_area[0]] > 
                                 (size_threshold*wdpa_df[field_large_area[0]])]['WDPA_PID'].values

    else:
        raise Exception('ERROR: field(s) to test is (are) not specified')
            
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

######################################################
#### 5.1. Area invalid: NO_TK_AREA and REP_M_AREA ####
######################################################

def area_invalid_no_tk_area_rep_m_area(wdpa_df, return_pid=False):
    '''
    Return True if NO_TK_AREA is larger than REP_M_AREA
    Return list of WDPA_PIDs where NO_TK_AREA is larger than REP_M_AREA if return_pid=True
    '''
    
    field_small_area = ['NO_TK_AREA']
    field_large_area = ['REP_M_AREA']
    
    return area_invalid_size(wdpa_df, field_small_area, field_large_area, return_pid)

######################################################
#### 5.2. Area invalid: NO_TK_AREA and GIS_M_AREA ####
######################################################

def area_invalid_no_tk_area_gis_m_area(wdpa_df, return_pid=False):
    '''
    Return True if NO_TK_AREA is larger than GIS_M_AREA
    Return list of WDPA_PIDs where NO_TK_AREA is larger than GIS_M_AREA if return_pid=True
    '''
    
    field_small_area = ['NO_TK_AREA']
    field_large_area = ['GIS_M_AREA']
    
    return area_invalid_size(wdpa_df, field_small_area, field_large_area, return_pid)

####################################################
#### 5.3. Area invalid: GIS_M_AREA and GIS_AREA ####
####################################################

def area_invalid_gis_m_area_gis_area(wdpa_df, return_pid=False):
    '''
    Return True if GIS_M_AREA is larger than GIS_AREA
    Return list of WDPA_PIDs where GIS_M_AREA is larger than GIS_AREA, if return_pid=True
    '''
    
    field_small_area = ['GIS_M_AREA']
    field_large_area = ['GIS_AREA']

    return area_invalid_size(wdpa_df, field_small_area, field_large_area, return_pid)

####################################################
#### 5.4. Area invalid: REP_M_AREA and REP_AREA ####
####################################################

def area_invalid_rep_m_area_rep_area(wdpa_df, return_pid=False):
    '''
    Return True if REP_M_AREA is larger than REP_AREA
    Return list of WDPA_PIDs where REP_M_AREA is larger than REP_AREA, if return_pid=True
    '''
    
    field_small_area = ['REP_M_AREA']
    field_large_area = ['REP_AREA']
    
    return area_invalid_size(wdpa_df, field_small_area, field_large_area, return_pid)
	
#################################
#### 6. Forbidden characters ####
#################################

#### Parent function ####

def forbidden_character(wdpa_df, check_fields, return_pid=False):
    '''
    Factory of functions: this generic function is to be linked to
    the family of 'forbidden character' functions stated below. These latter 
    functions are to give information on which fields to check and pull 
    from the DataFrame. This function is the foundation of the others.
    
    Return True if forbidden characters are found in the DataFrame

    Return list of WDPA_PID where forbidden characters occur, if 
    return_pid is set True

    ## Arguments ##
    check_fields -- list of the field(s) to check for forbidden characters
    
    ## Example ##
    forbidden_character(
        wdpa_df,
        check_fields=["DESIG_ENG"],
        return_pid=True):    
    '''

    # Import regular expression package and the forbidden characters
    import re
    matches = ['<','>',"?","*","#","\n","\r"]
    field_unallowed_values = [re.escape(m) for m in matches] # ensure correct formatting of forbidden characters

    # Obtain the WDPA_PIDs with forbidden characters
    invalid_wdpa_pid = wdpa_df[wdpa_df[check_fields[0]].str.contains('|'.join(field_unallowed_values))]['WDPA_PID'].values

    if return_pid:
        return invalid_wdpa_pid
        
    return len(invalid_wdpa_pid) >= 1

#### Child functions ####

#########################################
#### 6.1. Forbidden character - NAME ####
#########################################

def forbidden_character_name(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'NAME'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'NAME'
    '''

    check_fields = ['NAME']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##############################################
#### 6.2. Forbidden character - ORIG_NAME ####
##############################################

def forbidden_character_orig_name(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'ORIG_NAME'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'ORIG_NAME'
    '''

    check_fields = ['ORIG_NAME']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##########################################
#### 6.3. Forbidden character - DESIG ####
##########################################

def forbidden_character_desig(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'DESIG'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'DESIG'
    '''

    check_fields = ['DESIG']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##############################################
#### 6.4. Forbidden character - DESIG_ENG ####
##############################################

def forbidden_character_desig_eng(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'DESIG_ENG'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'DESIG_ENG'
    '''

    check_fields = ['DESIG_ENG']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##############################################
#### 6.5. Forbidden character - MANG_AUTH ####
##############################################

def forbidden_character_mang_auth(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'MANG_AUTH'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'MANG_AUTH'
    '''

    check_fields = ['MANG_AUTH']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##############################################
#### 6.6. Forbidden character - MANG_PLAN ####
##############################################

def forbidden_character_mang_plan(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'MANG_PLAN'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'MANG_PLAN'
    '''

    check_fields = ['MANG_PLAN']

    return forbidden_character(wdpa_df, check_fields, return_pid)

############################################
#### 6.7. Forbidden character - SUB_LOC ####
############################################

def forbidden_character_sub_loc(wdpa_df, return_pid=False):
    '''
    This function is to capture forbidden characters in the field 'SUB_LOC'
    
    Input: WDPA in pandas DataFrame 
    Output: list with WDPA_PIDs containing forbidden characters in field 'SUB_LOC'
    '''

    check_fields = ['SUB_LOC']

    return forbidden_character(wdpa_df, check_fields, return_pid)

##############################################
#### 7. METADATAID: WDPA and Source Table ####
##############################################

#######################################################################
#### 7.1. Invalid: METADATAID present in WDPA, not in Source Table ####
#######################################################################

def invalid_metadataid_not_in_source_table(wdpa_df, wdpa_source, return_pid=False):
    '''
    Return True if METADATAID is present in the WDPA but not in the Source Table
    Return list of WDPA_PIDs for which the METADATAID is not present in the Source Table
    '''
        
    field = ['METADATAID']

    ########## OPTIONAL ##########
    #### Remove METADATAID = 840 (Russian sites that are restricted and not in Source Table)    
    #condition_crit = [840]
    # Remove METADATAID = 840 from the WDPA
    #wdpa_df_no840 = wdpa_df[wdpa_df[field[0]] != condition_crit[0]]
    #invalid_wdpa_pid = wdpa_df_no840[~wdpa_df_no840[field[0]].isin(
    #                                  wdpa_source[field[0]].values)]['WDPA_PID'].values
    ##############################

    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(
                                wdpa_source[field[0]].values)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return invalid_wdpa_pid >= 1

#######################################################################
#### 7.2. Invalid: METADATAID present in Source Table, not in WDPA ####
#### Note: output is METADATAIDs.                                  ####
#######################################################################

def invalid_metadataid_not_in_wdpa(wdpa_df, wdpa_point, wdpa_source, return_pid=False):
    '''
    Return True if METADATAID is present in the Source Table but not in the Source Table
    Return list of METADATAIDs for which the METADATAID is not present in the Source Table
    '''
    
    field = ['METADATAID']

    # Concatenate all METADATAIDs of the WDPA point and poly tables
    field_allowed_values = np.concatenate((wdpa_df[field[0]].values,wdpa_point[field[0]].values),axis=0)

    ########## OPTIONAL ##########
    # Remove METADATA = 840 (Russian sites that are restricted and not in Source Table)
    #metadataid_wdpa = np.concatenate((wdpa_df[field[0]].values,wdpa_point[field[0]].values),axis=0)
    #field_allowed_values = np.delete(metadataid_wdpa, np.where(metadataid_wdpa == 840), axis=0)
    #######################
    
    # Find METADATAIDs in the Source Table that are not present in the WDPA
    invalid_metadataid = wdpa_source[~wdpa_source[field[0]].isin(field_allowed_values)]['METADATAID'].values
    
    if return_pid:
        return invalid_metadataid
    
    return len(invalid_metadataid) >= 1