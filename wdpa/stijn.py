# import package
import os
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows    
from openpyxl.formatting import Rule
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.styles.differential import DifferentialStyle

def output_errors_to_excel(main_output, functions_list):
    '''
    ## Action point: refactor the conditional formatting
    
    The functions_list is a list that contains all the names of the 
    functions (tests) of the WDPA QA. If the function's name is present
    in the main_output dictionary produced by the main function, 
    the WDPA failed the test and contains errors.
    
    Function output_errors_to_excel evaluates whether each function's name 
    in functions_list, is present in the main_output dictionary. 
    If so, it will output the coresponding DataFrame to a sheet in an 
    Excel file. In the Excel Summary sheet, the function's name will be 
    added along with string 'Fail'. Else, the test's name will be added to 
    the Excel Summary sheet along with string 'Pass'.
        
    ## Arguments ##
    main_output --    dictionary created by the main function, containing 
                      functions' names and DataFrames for tests that failed. 
                      In this dictionary, a function's name is the 'key', and 
                      the DataFrame with errors is the 'value'.
    
    functions_list -- a list of strings containing all the functions' (tests') 
                      names of the WDPA QA

    ## Example ##
    output_errors_to_excel(main_output='output_31July2019',
                            functions_list=['invalid_desig_type',
                            'inconsistent_name_same_wdpaid'])
    '''
    
    # set constants - to later add the current day to the filename
    DATE = f"{datetime.datetime.now():%d%B%Y}"
    FILENAME ='WDPA_errors'
    SUFFIX = '.xlsx'
    
    # Create the Excel workbook and the Summary sheet
    wb = Workbook()
    wb.remove(wb['Sheet']) # remove default sheet
    wb.create_sheet("Summary",0)
    wb["Summary"].append(["CHECK","RESULT"]) # enter header for Summary sheet

    # If the function's name - in the functions_list - is present in the 
    # main_output dictionary, add DataFrame to a new sheet
    for function_name in functions_list:
        if function_name in main_output:
            ws = wb.create_sheet(function_name)
        # export DataFrame rows to Excel
            for row in dataframe_to_rows(main_output[function_name], index=False): 
                ws.append(row)
        # add 'Fail' to Summary sheet
            wb["Summary"].append([function_name,"Fail"]) 

        # function_name is not present in the main_output
        else:
            wb["Summary"].append([function_name,"Pass"])

    # conditional formatting - red rows for tests that fail
    red_fill = PatternFill(bgColor="FF6347") # specify what colour to load
    style_to_apply = DifferentialStyle(fill=red_fill) # specify the style: fill only
    r = Rule(type="expression", dxf=style_to_apply, stopIfTrue=True) # specify the format of the rule
    r.formula = ['$B2="Fail"'] # value that determines conditional format
    wb["Summary"].conditional_formatting.add("A2:B200", r) # add the formatting    
    
    # conditional formatting - green rows for tests that pass
    green_fill = PatternFill(bgColor="00FF00") # specify what colour to load
    style_to_apply = DifferentialStyle(fill=green_fill) # specify the style: fill only
    r = Rule(type="expression", dxf=style_to_apply, stopIfTrue=True) # specify the format of the rule
    r.formula = ['$B2="Pass"'] # value that determines conditional format
    wb["Summary"].conditional_formatting.add("A2:B200", r) # add the formatting     
    
    # Extra formatting
    wb["Summary"].sheet_properties.tabColor = "1072BB" # blue tab   
    
    # Save the workbook
    wb.save(DATE+FILENAME+SUFFIX)
    return