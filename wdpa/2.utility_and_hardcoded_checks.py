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

# REFACTOR THIS USING invalid_nan(wdpa_df, field, return_pid=False)
# Specify `field` as "METADATAID" or "WDPA_PID"

# Add pd.DataFrame.isna() to check for NAs

## 2.1.a. Find NaN / NULL in WDPA polygon and point data

def invalid_nan(wdpa_df, return_pid=False):
    '''
    Return True if there is one or more NaNs present in the WDPA
    Return list of WDPA_PIDs in which a value contains NaN
    '''

    invalid_wdpa_pid = wdpa_df[wdpa_df.isnull().values]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid
    
    return len(invalid_wdpa_pid) >= 1

## 2.1.b. Find NaN / NULL in WDPA Source Table
## Note: output is METADATAIDs.

def invalid_nan_source(wdpa_source, return_pid=False):
    '''
    Return True if there is one or more NaNs present in the WDPA
    Return list of WDPA_PIDs in which a value contains NaN
    '''

    invalid_metadataid = wdpa_source[wdpa_source.isnull().values]['METADATAID'].values
    
    if return_pid:
        return invalid_metadataid
    
    return len(invalid_metadataid) >= 1


	
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
        if wdpa_df['marine_proportion'] < coast_min:
            return '0'
        elif coast_min < wdpa_df['marine_proportion'] < coast_max:
            return '1'
        elif wdpa_df['marine_proportion'] > coast_max:
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
    calc =      (d['REP_AREA'] + d['GIS_AREA']) / d['REP_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    d['GIS_size_check_stats'] = np.select(condition, # produce column without outliers
                                         choice, 
                                         default = calc)

    # Column 2: to find WDPA_PIDs with too large GIS_AREA
    d['GIS_size_check'] = (d['REP_AREA'] + d['GIS_AREA']) / d['REP_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_size_check using mean and stdev
    MAX_GIS = d['GIS_size_check_stats'].mean() + (2*d['GIS_size_check_stats'].std())
    MIN_GIS = d['GIS_size_check_stats'].mean() - (2*d['GIS_size_check_stats'].std())

    # Find the rows with an incorrect GIS_AREA
    invalid_wdpa_pid = d[((d['GIS_size_check'] > MAX_GIS) | 
                       (d['GIS_size_check'] < MIN_GIS)) &
                       (abs(d['GIS_AREA']-d['REP_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
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
    calc =      (d['REP_AREA'] + d['GIS_AREA']) / d['GIS_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    d['REP_size_check_stats'] = np.select(condition, # produce column without outliers
                                          choice, 
                                          default = calc)

    # Column 2: to find WDPA_PIDs with too large REP_AREA
    d['REP_size_check'] = (d['REP_AREA'] + d['GIS_AREA']) / d['GIS_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_size_check using mean and stdev
    MAX_REP = d['REP_size_check_stats'].mean() + (2*d['REP_size_check_stats'].std())
    MIN_REP = d['REP_size_check_stats'].mean() - (2*d['REP_size_check_stats'].std())

    # Find the rows with an incorrect REP_AREA
    invalid_wdpa_pid = d[((d['REP_size_check'] > MAX_REP) | 
                       (d['REP_size_check'] < MIN_REP)) &
                       (abs(d['GIS_AREA']-d['REP_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
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
    calc =      (d['REP_M_AREA'] + d['GIS_M_AREA']) / d['REP_M_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    d['GIS_M_size_check_stats'] = np.select(condition, # produce column without outliers
                                         choice, 
                                         default = calc)

    # Column 2: to find WDPA_PIDs with too large GIS_AREA
    d['GIS_M_size_check'] = (d['REP_M_AREA'] + d['GIS_M_AREA']) / d['REP_M_AREA']
    
    # Calculate the maximum and minimum allowed values for GIS_M_size_check using mean and stdev
    MAX_GIS = d['GIS_M_size_check_stats'].mean() + (2*d['GIS_M_size_check_stats'].std())
    MIN_GIS = d['GIS_M_size_check_stats'].mean() - (2*d['GIS_M_size_check_stats'].std())

    # Find the rows with an incorrect GIS_AREA
    invalid_wdpa_pid = d[((d['GIS_M_size_check'] > MAX_GIS) | 
                       (d['GIS_M_size_check'] < MIN_GIS)) &
                       (abs(d['GIS_M_AREA']-d['REP_M_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
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
    calc =      (d['REP_M_AREA'] + d['GIS_M_AREA']) / d['GIS_M_AREA']
    condition = [calc > 100,
                 calc < 0]
    choice =    [np.nan,np.nan]
    
    d['REP_M_size_check_stats'] = np.select(condition, # produce column without outliers
                                          choice, 
                                          default = calc)

    # Column 2: to find WDPA_PIDs with too large REP_M_AREA
    d['REP_M_size_check'] = (d['REP_M_AREA'] + d['GIS_M_AREA']) / d['GIS_M_AREA']
    
    # Calculate the maximum and minimum allowed values for REP_M_size_check using mean and stdev
    MAX_REP = d['REP_M_size_check_stats'].mean() + (2*d['REP_M_size_check_stats'].std())
    MIN_REP = d['REP_M_size_check_stats'].mean() - (2*d['REP_M_size_check_stats'].std())

    # Find the rows with an incorrect REP_M_AREA
    invalid_wdpa_pid = d[((d['REP_M_size_check'] > MAX_REP) | 
                       (d['REP_M_size_check'] < MIN_REP)) &
                       (abs(d['GIS_M_AREA']-d['REP_M_AREA']) > MAX_ALLOWED_SIZE_DIFF_KM2)]['WDPA_PID'].values
    
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