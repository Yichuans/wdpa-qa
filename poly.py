import sys
from wdpa.qas import *

# load input
# input_poly = sys.argv[1]
input_poly = r"E:\Yichuan\WDPA\WDPA_May2016_Public.gdb\WDPA_poly_May2016"
# output_path = sys.argv[2]

# test
poly_df = arcgis_table_to_df(input_poly, INPUT_FIELDS_POLY)

sample = poly_df.sample(20000)

# prepare loading different checks
core_checks = [
# ('invalid_nan', invalid_nan),
# ('assign_marine_value', assign_marine_value),
('duplicate_wdpa_pid', duplicate_wdpa_pid),
('area_invalid_rep_m_area_marine12', area_invalid_rep_m_area_marine12),
('area_invalid_rep_m_area_rep_area', area_invalid_rep_m_area_rep_area),
('area_invalid_no_tk_area_rep_m_area', area_invalid_no_tk_area_rep_m_area),
('invalid_no_take_no_tk_area_rep_m_area', invalid_no_take_no_tk_area_rep_m_area),
('invalid_int_crit_desig_eng_other', invalid_int_crit_desig_eng_other),
('invalid_desig_eng_iucn_cat_other', invalid_desig_eng_iucn_cat_other),
('inconsistent_name_same_wdpaid', inconsistent_name_same_wdpaid),
('inconsistent_orig_name_same_wdpaid', inconsistent_orig_name_same_wdpaid),
('inconsistent_desig_same_wdpaid', inconsistent_desig_same_wdpaid),
('inconsistent_desig_eng_same_wdpaid', inconsistent_desig_eng_same_wdpaid),
('inconsistent_desig_type_same_wdpaid', inconsistent_desig_type_same_wdpaid),
('inconsistent_iucn_cat_same_wdpaid', inconsistent_iucn_cat_same_wdpaid),
('inconsistent_int_crit_same_wdpaid', inconsistent_int_crit_same_wdpaid),
('inconsistent_no_take_same_wdpaid', inconsistent_no_take_same_wdpaid),
('inconsistent_status_same_wdpaid', inconsistent_status_same_wdpaid),
('inconsistent_status_yr_same_wdpaid', inconsistent_status_yr_same_wdpaid),
('inconsistent_gov_type_same_wdpaid', inconsistent_gov_type_same_wdpaid),
('inconsistent_own_type_same_wdpaid', inconsistent_own_type_same_wdpaid),
('inconsistent_mang_auth_same_wdpaid', inconsistent_mang_auth_same_wdpaid),
('inconsistent_mang_plan_same_wdpaid', inconsistent_mang_plan_same_wdpaid),
('inconsistent_verif_same_wdpaid', inconsistent_verif_same_wdpaid),
('inconsistent_metadataid_same_wdpaid', inconsistent_metadataid_same_wdpaid),
('inconsistent_sub_loc_same_wdpaid', inconsistent_sub_loc_same_wdpaid),
('inconsistent_parent_iso3_same_wdpaid', inconsistent_parent_iso3_same_wdpaid),
('inconsistent_iso3_same_wdpaid', inconsistent_iso3_same_wdpaid),
('invalid_pa_def', invalid_pa_def),
('invalid_desig_eng_international', invalid_desig_eng_international),
('invalid_desig_type_international', invalid_desig_type_international),
('invalid_desig_eng_regional', invalid_desig_eng_regional),
('invalid_desig_type_regional', invalid_desig_type_regional),
('invalid_int_crit_desig_eng_ramsar_whs', invalid_int_crit_desig_eng_ramsar_whs),
('invalid_desig_type', invalid_desig_type),
('invalid_iucn_cat', invalid_iucn_cat),
('invalid_iucn_cat_unesco_whs', invalid_iucn_cat_unesco_whs),
('invalid_marine', invalid_marine),
('invalid_no_take_marine0', invalid_no_take_marine0),
('invalid_no_take_marine12', invalid_no_take_marine12),
('invalid_no_tk_area_marine', invalid_no_tk_area_marine),
('invalid_no_tk_area_no_take', invalid_no_tk_area_no_take),
('invalid_status', invalid_status),
('invalid_status_yr', invalid_status_yr),
('invalid_gov_type', invalid_gov_type),
('invalid_own_type', invalid_own_type),
('invalid_verif', invalid_verif),
('invalid_parent_iso3', invalid_parent_iso3),
('invalid_iso3', invalid_iso3),
('invalid_status_desig_type', invalid_status_desig_type),]

area_checks = [
('area_invalid_too_large_gis', area_invalid_too_large_gis),
('area_invalid_too_large_rep', area_invalid_too_large_rep),
('area_invalid_too_large_gis_m', area_invalid_too_large_gis_m),
('area_invalid_too_large_rep_m', area_invalid_too_large_rep_m),
('area_invalid_gis_area', area_invalid_gis_area),
('area_invalid_no_tk_area_gis_m_area', area_invalid_no_tk_area_gis_m_area),
('area_invalid_gis_m_area_gis_area', area_invalid_gis_m_area_gis_area),
('area_invalid_marine', area_invalid_marine),
('area_invalid_gis_m_area_marine12', area_invalid_gis_m_area_marine12)]

# checks to run
# pt = core_checks
poly = core_checks + area_checks

# ('forbidden_character', forbidden_character),
# ('forbidden_character_name', forbidden_character_name),
# ('forbidden_character_orig_name', forbidden_character_orig_name),
# ('forbidden_character_desig', forbidden_character_desig),
# ('forbidden_character_desig_eng', forbidden_character_desig_eng),
# ('forbidden_character_mang_auth', forbidden_character_mang_auth),
# ('forbidden_character_mang_plan', forbidden_character_mang_plan),
# ('forbidden_character_sub_loc', forbidden_character_sub_loc)

result = dict()

for name, f in poly:
    # checks are not optimised, thus return all pids regardless
    wdpa_pid = f(sample, True)
    if wdpa_pid.size > 0:
        result[name] = find_wdpa_rows(sample, wdpa_pid)



