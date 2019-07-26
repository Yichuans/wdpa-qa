##############################################
#### 7. METADATAID: WDPA and Source Table ####
##############################################

#######################################################################
#### 7.1. Invalid: METADATAID present in WDPA, not in Source Table ####
#######################################################################

def invalid_metadataid_not_in_source_table(wdpa_df, return_pid=False):
    '''
    Return True if METADATAID is present in the WDPA but not in the Source Table
    Return list of WDPA_PIDs for which the METADATAID is not present in the Source Table
    '''
        
    field = ['METADATAID']

    #######################
    # OPTIONAL: remove METADATAID = 840 (Russian sites that are restricted and not in Source Table)    
    #condition_crit = [840]
    # Remove METADATAID = 840 from the WDPA
    #wdpa_df_no840 = wdpa_df[wdpa_df[field[0]] != condition_crit[0]]
    #invalid_wdpa_pid = wdpa_df_no840[~wdpa_df_no840[field[0]].isin(wdpa_source[field[0]].values)]['WDPA_PID'].values
    #######################

    # Find invalid WDPA_PIDs
    invalid_wdpa_pid = wdpa_df[~wdpa_df[field[0]].isin(wdpa_source[field[0]].values)]['WDPA_PID'].values
    
    if return_pid:
        return invalid_wdpa_pid

    return invalid_wdpa_pid >= 1

#######################################################################
#### 7.2. Invalid: METADATAID present in Source Table, not in WDPA ####
#### Note: output is METADATAIDs.                                  ####
#######################################################################

def invalid_metadataid_not_in_wdpa(wdpa_df, return_pid=False):
    '''
    Return True if METADATAID is present in the Source Table but not in the Source Table
    Return list of METADATAIDs for which the METADATAID is not present in the Source Table
    '''
    
    # Concatenate all METADATAIDs of the WDPA point and poly tables
    field_allowed_values = np.concatenate((wdpa_df[field[0]].values,wdpa_point[field[0]].values),axis=0)

    #######################
    # OPTIONAL: remove METADATA = 840 (Russian sites that are restricted and not in Source Table)
    #metadataid_wdpa = np.concatenate((wdpa_df[field[0]].values,wdpa_point[field[0]].values),axis=0)
    #field_allowed_values = np.delete(metadataid_wdpa, np.where(metadataid_wdpa == 840), axis=0)
    #######################

    field = ['METADATAID']
    
    # Find METADATAIDs in the Source Table that are not present in the WDPA
    invalid_metadataid = wdpa_source[~wdpa_source[field[0]].isin(field_allowed_values)]['METADATAID'].values
    
    if return_pid:
        return invalid_metadataid
    
    return len(invalid_metadataid) >= 1