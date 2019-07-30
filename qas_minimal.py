#### QA for WDPA 2019 ####
'''
Author: Stijn den Haan
Supervisor: Yichuan Shi
Bioinformatics internship • UNEP-WCMC • 10 June --- 9 August 2019

Minimal viable unit of testing 
## Trying out all the different functions to produce tables ##
'''

###########################################
##### 0. Load packages and WDPA fields ####
###########################################

## Load packages

from wdpa import qas
import numpy as np
import pandas as pd
import arcpy
import datetime
import os

#### Load fields present in the WDPA tables ####

## Polygon data
os.chdir(r"C:\Users\paintern\Desktop\Stijn\3. Data\Test data + bug")

input_fields_poly = ['WDPAID', 'WDPA_PID', 'PA_DEF', 'NAME', 'ORIG_NAME', 'DESIG', 
                     'DESIG_ENG', 'DESIG_TYPE', 'IUCN_CAT', 'INT_CRIT', 'MARINE', 'REP_M_AREA', 
                     'GIS_M_AREA', 'REP_AREA', 'GIS_AREA', 'NO_TAKE', 'NO_TK_AREA', 'STATUS', 'STATUS_YR', 
                     'GOV_TYPE', 'OWN_TYPE', 'MANG_AUTH', 'MANG_PLAN', 'VERIF', 'METADATAID', 'SUB_LOC', 
                     'PARENT_ISO3', 'ISO3', ]

wdpa_df = qas.arcgis_table_to_df(in_fc = "test", 
                             workspace_gdb = "WDPA_Jun2019_Public.gdb", 
                             input_fields = input_fields_poly, 
                             query='')

print(qas.invalid_pa_def(wdpa_df, True))