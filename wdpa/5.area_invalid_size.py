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
	
