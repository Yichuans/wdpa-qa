import sys, arcpy
import numpy as np
from wdpa.qa import arcgis_table_to_df, find_wdpa_rows, poly_checks, INPUT_FIELDS_META
from wdpa.export import output_errors_to_excel

# input
input_poly = sys.argv[1]
input_pt = sys.argv[2]
input_meta = sys.argv[3]
output_path = sys.argv[4]

# input_poly = r'E:\Yichuan\WDPA\WDPA_Dec2016_Public\WDPA_Dec2016_Public.gdb\WDPA_poly_Dec2016'
# input_pt = r'E:\Yichuan\WDPA\WDPA_Dec2016_Public\WDPA_Dec2016_Public.gdb\WDPA_point_Dec2016'
# input_meta = r'E:\Yichuan\WDPA\WDPA_Dec2016_Public\WDPA_Dec2016_Public.gdb\WDPA_source_Dec2016'
# output_path = r'E:\Yichuan\WDPA\WDPA_Dec2016_Public'

# poly and points
INPUT_FIELDS = ['WDPAID', 'WDPA_PID', 'METADATAID', 'NAME', 'ISO3', 'DESIG']

# make dfs
df_poly = arcgis_table_to_df(input_poly, INPUT_FIELDS)
df_pt = arcgis_table_to_df(input_pt, INPUT_FIELDS)
df_meta = arcgis_table_to_df(input_meta, INPUT_FIELDS_META)

result = dict()
# check duplicate WDPAID and WDPA_PID across point and polygon
result['overlap_wdpaid'] = df_poly[df_poly['WDPAID'].isin(
    np.intersect1d(df_poly['WDPAID'].values, df_pt['WDPAID'].values))]

result['overlap_wdpa_pid'] = df_poly[df_poly['WDPA_PID'].isin(
    np.intersect1d(df_poly['WDPA_PID'].values, df_pt['WDPA_PID'].values))]

# check matching metadata ID in source table
indata_meta = np.union1d(df_poly['METADATAID'].values, df_pt['METADATAID'].values)
inref_meta = df_meta['METADATAID'].values

result['metaid_only_in_data'] = df_poly[df_poly['METADATAID'].isin(
    np.setdiff1d(indata_meta, inref_meta))]

result['metaid_only_in_metadata'] =  df_meta[df_meta['METADATAID'].isin(
    np.setdiff1d(inref_meta, indata_meta))]

output_errors_to_excel(result, output_path, [{'name': key} for key in result.keys()], 'meta')

