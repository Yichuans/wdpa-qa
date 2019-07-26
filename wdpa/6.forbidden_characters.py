#################################
#### 6. Forbidden characters ####
#################################

#### Parent function ####

def forbidden_character(wdpa_df, check_field, return_pid=False):
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
        check_field=["DESIG_ENG"],
        return_pid=True):    
    '''

    # Import regular expression package and the forbidden characters
    import re
    matches = ['<','>',"?","*","#","\n","\r"]
    field_unallowed_values = [re.escape(m) for m in matches] # ensure correct formatting of forbidden characters

    # Obtain the WDPA_PIDs with forbidden characters
    invalid_wdpa_pid = wdpa_df[wdpa_df[check_field[0]].str.contains('|'.join(field_unallowed_values))]['WDPA_PID'].values

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)

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

    return forbidden_character(wdpa_df, return_pid, check_fields)