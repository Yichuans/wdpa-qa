import sys
from wdpa.qas import *
from wdpa.stijn import output_errors_to_excel

# load input
# input_poly = sys.argv[1]
input_poly = r"E:\Yichuan\WDPA\WDPA_May2016_Public.gdb\WDPA_poly_May2016"
# output_path = sys.argv[2]

# poly
poly_df = arcgis_table_to_df(input_poly, INPUT_FIELDS_POLY)

sample = poly_df.sample(20000)

# prepare loading different checks


# ('forbidden_character', forbidden_character),
# ('forbidden_character_name', forbidden_character_name),
# ('forbidden_character_orig_name', forbidden_character_orig_name),
# ('forbidden_character_desig', forbidden_character_desig),
# ('forbidden_character_desig_eng', forbidden_character_desig_eng),
# ('forbidden_character_mang_auth', forbidden_character_mang_auth),
# ('forbidden_character_mang_plan', forbidden_character_mang_plan),
# ('forbidden_character_sub_loc', forbidden_character_sub_loc)

result = dict()

for poly_check in POLY_CHECKS:
    print(poly_check['name'])
    # checks are not optimised, thus return all pids regardless
    wdpa_pid = poly_check['func'](sample, True)

    if wdpa_pid.size > 0:
        result[poly_check['name']] = find_wdpa_rows(sample, wdpa_pid)

output_errors_to_excel(result, POLY_CHECKS)


