import sys
from wdpa.qas import arcgis_table_to_df, find_wdpa_rows, poly_checks, INPUT_FIELDS_POLY
from wdpa.stijn import output_errors_to_excel

# load input
input_poly = r"E:\Yichuan\WDPA\WDPA_May2016_Public.gdb\WDPA_poly_May2016"
output_path = r"E:\Yichuan"

# input_poly = sys.argv[1]
# output_path = sys.argv[2]

# poly
poly_df = arcgis_table_to_df(input_poly, INPUT_FIELDS_POLY)
sample = poly_df.sample(20000)

result = dict()

for poly_check in poly_checks:
    print(poly_check['name'])
    # checks are not currently optimised, thus return all pids regardless
    wdpa_pid = poly_check['func'](sample, True)

    if wdpa_pid.size > 0:
        result[poly_check['name']] = find_wdpa_rows(sample, wdpa_pid)

output_errors_to_excel(result, output_path, poly_checks)


