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
    field_allowed_values = ['1'] # WDPA data type is string
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
    field_allowed_values = ['Ramsar Site', 
                            'Wetland of International Importance', 
                            'UNESCO-MAB Biosphere Reserve', 
                            'World Heritage Site (natural or mixed)']
    condition_field = ['DESIG_TYPE']
    condition_crit = ['International']
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

##########################################
#### 4.3 Invalid DESIG_ENG - regional ####
##########################################

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

################################################################################
#### 4.4 Invalid INT_CRIT & DESIG_ENG  - Ramsar Site & World Heritage Sites ####
################################################################################

def invalid_int_crit_desig_eng_ramsar_whs(wdpa_df, return_pid=False):
     '''
    Return True if INT_CRIT is unequal to the allowed values (>1000 possible values) 
    and DESIG_ENG equals 'Ramsar Site (...)' or 'World Heritage Site (...)'
    Return list of WDPA_PIDs where INT_CRIT is invalid, if return_pid is set True
    '''
    
    # Function to create the possible INT_CRIT combinations
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

################################
#### 4.5 Invalid DESIG_TYPE ####
################################

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

##############################
#### 4.6 Invalid IUCN_CAT ####
##############################

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

####################################################################
#### 4.7 Invalid IUCN_CAT - UNESCO-MAB and World Heritage Sites ####
####################################################################

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

############################
#### 4.8 Invalid MARINE ####
############################

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

##########################################
#### 4.9 Invalid NO_TAKE & MARINE = 0 ####
##########################################

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

###############################################
#### 4.10 Invalid NO_TAKE & MARINE = [1,2] ####
###############################################

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

##########################################
#### 4.11 Invalid NO_TK_AREA & MARINE ####
##########################################

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
#### 4.12. Invalid NO_TK_AREA & NO_TAKE ####
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
#### 4.13. Invalid STATUS ####
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

################################
#### 4.14 Invalid STATUS_YR ####
################################

def invalid_status_yr(wdpa_df, return_pid=False):
    '''
    Return True if STATUS_YR is unequal to 0 or any year between 1819 and the current year
    Return list of WDPA_PIDs where STATUS_YR is invalid, if return_pid is set True
    '''
    
    field = ['STATUS_YR']
    year = datetime.date.today().year # obtain current year
    yearArray = [0] + np.arange(1819, year + 1, 1).tolist() # make a list of all years, from 0 to current year
    field_allowed_values = [str(x) for x in testArray] # change all integers to strings
    condition_field = []
    condition_crit = []
    
    return invalid_value_in_field(wdpa_df, field, field_allowed_values, condition_field, condition_crit, return_pid)

################################
#### 4.15. Invalid GOV_TYPE ####
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
#### 4.16. Invalid OWN_TYPE ####
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
#### 4.17. Invalid VERIF ####
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
#### 4.18. Invalid PARENT_ISO3 ####
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
#### 4.19. Invalid ISO3 ####
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
#### 4.20. Invalid STATUS & DESIG_TYPE ####
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