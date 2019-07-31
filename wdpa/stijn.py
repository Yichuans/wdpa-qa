# import package
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows    
from openpyxl.formatting import Rule
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.styles.differential import DifferentialStyle
import datetime
import os

def output_errors_to_excel(main_output, function_name):
    '''
    ## Action point: refactor the conditional formatting
    
    If the function_name is present in the main_output dictionary 
    produced by the main function, it means that the WDPA failed the test and
    contains errors. In the dictionary, the function_name is the 
    key, and the DataFrame with errors is the value.
    
    The present function, output_errors_to_excel, will lookup whether the function_name
    is present in the main_output dictionary. If so, it will output
    the DataFrames to a corresponding sheet in an Excel file and in the Excel Summary sheet
    the function_name will be added along with text 'Fail'. If function_name is not present,
    the function_name will be added to the Excel Summary sheet along with text 'Pass'.
    
    Dependent on whether there is an Excel file present, an Excel file 
    will either be created (if not present) or appended (if present) if run on the same day.
    
    ## Arguments ##
    main_output --   dictionary created by the main function, containing 
                     function names and dataframes for tests that failed
    
    function_name -- a string with the name of the function, 
                     to be checked whether it is present in main_output
    
    
    ## Example ##
    output_errors_to_excel(main_output='output_31July2019',
                            function_name='invalid_desig_eng_regional')
    '''


    # set constants - to later add the current day to the filename
    DATE = f"{datetime.datetime.now():%d%B%Y}"
    FILENAME = 'WDPA_errors'
    SUFFIX = '.xlsx'
    
    # Import WDPA rows, that contain errors, into Excel    
    # Excel sheet present
    if os.path.isfile(DATE+FILENAME+SUFFIX): 
        wb = load_workbook(DATE+FILENAME+SUFFIX)
        if function_name in main_output:
            ws = wb.create_sheet(function_name)
            ws.sheet_properties.tabColor = "FF6347" # red tab
            for row in dataframe_to_rows(main_output[function_name], index=False): # import DataFrame rows
                ws.append(row)
            wb["Summary"].append([function_name,"Fail"]) # add test result to Summary sheet

        # function_name is not present in the main_output
        else:
            wb["Summary"].append([function_name,"Pass"])

    # Excel sheet absent
    else: 
        wb = Workbook()
        if function_name in main_output:
            ws = wb.create_sheet(function_name)
            wb.remove(wb['Sheet'])
            ws.sheet_properties.tabColor = "FA8072" # red tab
            for row in dataframe_to_rows(main_output[function_name], index=False):
                ws.append(row)
            wb.create_sheet("Summary",0)
            wb["Summary"].sheet_properties.tabColor = "1072BB" # blue tab
            wb["Summary"].append(["CHECK","RESULT"])
            wb["Summary"].append([function_name,"Fail"])

        # function_name is not present in the main_output
        else:
            wb.create_sheet("Summary",0)
            wb.remove(wb['Sheet'])
            wb["Summary"].sheet_properties.tabColor = "1072BB" # blue tab
            wb["Summary"].append(["CHECK","RESULT"])
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
    
    # Save the workbook
    wb.save(DATE+FILENAME+SUFFIX)
    return