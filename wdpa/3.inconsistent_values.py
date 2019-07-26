#########################################################
#### 3. Find inconsistent fields for the same WDPAID ####
#########################################################

#### Parent function ####

def inconsistent_fields_same_wdpaid(wdpa_df, 
                                        check_field, 
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
        wdpa_df,
        check_field=["DESIG_ENG"],
        return_pid=True):    
    '''

    if return_pid:
        # Group by WDPAID to find duplicate WDPAIDs and count the 
        # number of unique values for the field in question
        wdpaid_groups = wdpa_df.groupby(['WDPAID'])[check_fields].nunique()

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
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)
	
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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)
	
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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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
    
    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)

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

    return inconsistent_fields_same_wdpaid(wdpa_df, return_pid, check_fields)
	
