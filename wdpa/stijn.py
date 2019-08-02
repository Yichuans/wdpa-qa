# import package
import os
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows    
from openpyxl.formatting import Rule
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.styles.differential import DifferentialStyle

def output_errors_to_excel(result, outpath, checks):
    '''
    The functions_list is a list that contains all the names of the 
    functions (tests) of the WDPA QA. If the function's name is present
    in the result dictionary produced by the main function, 
    the WDPA failed the test and contains errors.
    
    Function output_errors_to_excel evaluates whether each function's name 
    in functions_list, is present in the result dictionary. 
    If so, it will output the coresponding DataFrame to a sheet in an 
    Excel file. In the Excel Summary sheet, the function's name will be 
    added along with string 'Fail'. Else, the test's name will be added to 
    the Excel Summary sheet along with string 'Pass'.
        
    ## Arguments ##
    result --         dictionary created by the main function, containing 
                      functions' names and DataFrames for tests that failed. 
                      In this dictionary, a function's name is the 'key', and 
                      the DataFrame with errors is the 'value'.
    
    outpath --        the output directory where the Excel file is to be saved
    
    checks --         a dictionary containing all the descriptive names 
                      and function names of the WDPA QA checks
    
    datatype --       a string specifying what the input type was: e.g. point or poly
                      This will be added to the Excel file's name.

    ## Example ##
    output_errors_to_excel(result=result,
                           outpath='C:\\Users\\paintern\\Desktop\\Stijn\\3. Data\\Test data',
                           checks=poly_checks,
                           datatype='poly'])
    '''
    
    #### Action points - to add:
    #### - add datatype to filename
    #### - add hyperlinks to sheets per check
    #### - (low priority: refactor the conditional formatting)
        
    # Function to find the row of the function_name
    # Required to add a hyperlink of the tab to the 
    # corresponding function_name cell
    def find_row(function_name):
        for row in wb['Summary'].iter_rows(min_row=1, max_row=wb['Summary'].max_row, max_col=1):
            for cell in row: # iterate through the cells in rows 1 through the end
                if cell.value == function_name: # select the correct cell
                    return (wb['Summary'].cell(row=cell.row, column=1).row) # return cell's row number
    
    # set constants - to later add the current day to the filename
    filename = f'{datetime.datetime.now():%d%B%Y_WDPA_QA_checks.xlsx}'
    output = outpath + os.sep + filename
    
    # Create the Excel workbook and the Summary sheet
    wb = Workbook()
    wb['Sheet'].title = 'Summary' # change default sheet's title
    wb["Summary"].append(["CHECK","RESULT", "COUNT"]) # add header for Summary sheet

    # If the function's name - in the functions_list - is present in the 
    # result dictionary, add DataFrame to a new sheet
    function_names = [each['name'] for each in checks] # make a list of all checks' names

    for function_name in function_names:
        if function_name in result:
            ws = wb.create_sheet(function_name)
        # export DataFrame rows to Excel
            for row in dataframe_to_rows(result[function_name], index=False): 
                ws.append(row)
        # add 'Check' or 'Fail' to Summary sheet
            if not function_name.startswith('ivd'):
                wb['Summary'].append([function_name,'Check', len(result[function_name])])
                ws.sheet_properties.tabColor = '87CEFA' # blue tab
                link = f'#{function_name}!A1' # create link to cell A1 of function_name tab
                # add link to the function_name of the Summary sheet
                wb['Summary'].cell(row=find_row(function_name), column=1).hyperlink = link 
            else:
                wb['Summary'].append([function_name,'Fail', len(result[function_name])])
                ws.sheet_properties.tabColor = 'FF6347' # red tab
                link = f'#{function_name}!A1' # as above
                wb['Summary'].cell(row=find_row(function_name), column=1).hyperlink = link
        # add 'Pass' to Summary sheet as no rows with invalid WDPA_PIDs are present
        else:
            wb['Summary'].append([function_name,'Pass'])

    #### REFACTOR THIS ####
    
    # conditional formatting - red rows for tests that fail
    # red_fill = PatternFill(bgColor='FF6347') # specify what colour to load
    # style_to_apply = DifferentialStyle(fill=red_fill) # specify the style: fill only
    # r = Rule(type='expression', dxf=style_to_apply, stopIfTrue=True) # specify the format of the rule
    # r.formula = ['$B2="Fail"'] # value that determines conditional format
    # wb['Summary'].conditional_formatting.add(f'A2:C{wb['Summary'].max_row}', r) # add the formatting    
    
    # # conditional formatting - blue rows for tests that need to be checked
    # red_fill = PatternFill(bgColor='87CEFA') # specify what colour to load
    # style_to_apply = DifferentialStyle(fill=red_fill) # specify the style: fill only
    # r = Rule(type='expression', dxf=style_to_apply, stopIfTrue=True) # specify the format of the rule
    # r.formula = ['$B2="Check"'] # value that determines conditional format
    # wb['Summary'].conditional_formatting.add(f'A2:C{wb['Summary'].max_row}', r) # add the formatting    
    
    # # conditional formatting - green rows for tests that pass
    # green_fill = PatternFill(bgColor='00FF00') # specify what colour to load
    # style_to_apply = DifferentialStyle(fill=green_fill) # specify the style: fill only
    # r = Rule(type='expression', dxf=style_to_apply, stopIfTrue=True) # specify the format of the rule
    # r.formula = ['$B2="Pass"'] # value that determines conditional format
    # wb['Summary'].conditional_formatting.add(f'A2:C{wb['Summary'].max_row}', r) # add the formatting     
    
    # Extra formatting
    wb['Summary'].sheet_properties.tabColor = '1072BB' # blue tab   
    
    # Save the workbook
    wb.save(output)
    return