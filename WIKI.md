# RAMBO: a Quality Assurance Tool for the World Database on Protected Areas

This document is to guide you through the usage of RAMBO, a quality assurance tool developed for the World Database on Protected Areas.

---

Author: Stijn den Haan

Supervisor: Yichuan Shi

Bioinformatics internship • UNEP-WCMC • 10 June - 9 August 2019

---

## Index

[Background](https://github.com/Yichuans/wdpa-qa/wiki#background)

[Installation requirements](https://github.com/Yichuans/wdpa-qa/wiki#installation-requirements)

[How RAMBO works](https://github.com/Yichuans/wdpa-qa/wiki#how-rambo-works)

[Usage](https://github.com/Yichuans/wdpa-qa/wiki#usage)

[Troubleshooting common errors](https://github.com/Yichuans/wdpa-qa/wiki#troubleshooting-common-errors-when-running-rambo)

[Exploring RAMBO's output in Excel](https://github.com/Yichuans/wdpa-qa/wiki#exploring-rambos-output-in-excel)

[Description of QA checks](https://github.com/Yichuans/wdpa-qa/wiki#description-of-qa-checks)

---

## Background

RAMBO was created to make the quality assurance of the World Database on Protected Areas (WDPA) more systematic, efficient, thorough, and less labour-intensive. RAMBO finds the errors and creates an error report in Excel where the nature and number of errors can be explored. Subsequent changes to the WDPA data need to be made manually.

---

## Installation requirements

- ArcGIS Pro `2.4` or later 

Required, but included in ArcGIS Pro `2.4`: 

- Python `3.6.8` or later (included in ArcGIS Pro `2.4`)
- Python packages required (versions stated below or later):
	- pandas `0.24.2`
	- numpy `1.16.2`
	- openpyxl `2.6.1`

Note: installing Anaconda is not required. Refrain from using any other Conda installation than the one that is installed by ArcGIS Pro by default.

---

### *Optional (developers only): setting up your Python environment*

This is **not required** to run RAMBO, but it is **optional**. Doing this will allow you to update Python packages individually, e.g. to use new functionality of a package without having to wait for an ArcGIS Pro update. During ArcGIS Pro updates, Python packages are updated, but this happens infrequently.

**Step 1**: Clone ArcGIS Pro's default Python environment called `arcgispro-py3`

1. Open ESRI's `Python Command Prompt` - this comes with ArcGIS Pro's installation. In Windows, see folder `ArcGIS` in the Start menu.

2. In the terminal, the first line should look similar to this:

        (arcgispro-py3) C:\Users\[UserName]\AppData\Local\ESRI\conda\envs\

3. Enter the following in the command-prompt:

```    
    # Display Python environments present
    conda info --envs

    # Become root (obtain administrator permissions)
    conda activate root
        
    # If that yields an error, use:
    activate root
        
    # Clone the default ArcPy environment
    conda create --name [NameOfNewEnvironment] --clone arcgispro-py3
        
    # Activate the new environment
    conda activate [NameOfNewEnvironment]
        
    # If that yields an error, use:
    activate [NameOfNewEnvironment]
        
    # View all installed packages
    conda list
        
    # Install required packages, e.g. pandas
    conda install [nameOfPackage]
```

**Step 2**: Make the new Python environment ArcGIS Pro's default environment

In ArcGIS Pro, go to Settings --> Python. This will display the Python Package Manager. Access 'Manage Environments', select the environment you just created, press OK and restart ArcGIS Pro. The new Python environment will now be loaded by default when starting ArcGIS Pro.

You are now ready to use your own Python environment that contains ArcPy.

---

## How RAMBO works

RAMBO is stored in a compressed file named `rambo_vX.Y.7z`. It consists of one `.tbx` file and a folder named `wdpa`.

#### `.tbx` file

This file is the ArcGIS toolbox to be loaded into an ArcGIS project. In this file, two scripts are embedded: `poly.py` and `point.py` (in ArcGIS, these scripts are labelled `WDPA polygon` and `WDPA point`). These Python scripts call the QA checks for polygon and point data, respectively, stored in script `qa.py` (see below).

#### `wdpa` folder

This folder consists of multiple files and a folder. Of these, only `qa.py` and `export.py` are relevant to understand how RAMBO works.

`qa.py` is a Python script that contains all QA checks. These checks are built according to the following principles:

- Per type of check (e.g. looking for inconsistencies among WDPAID duplicates in a particular field), there is a single Factory Function. This is a Python function that performs the actual check.
- For each field to check per Factory Function, there is an Input Function. These Input Functions provide the variables  (fields and values) that need to be passed to the Factory Function to check for errors. Each of these Input Functions calls the corresponding Factory Function at the end of the function. In this way the Factory Function is re-used for multiple input variables.
- Some types of checks do not have a Factory Function - these are hardcoded checks that have only a single input.

`export.py` is a Python script that exports the results of RAMBO to an Excel Workbook.

---

## Usage

### Walkthrough: importing and using RAMBO in ArcGIS Pro

1. Download RAMBO (the WDPA QA tool), from this GitHub repository
2. Unzip the file in a folder of your choosing
3. Open a (non-empty / empty) project in ArcGIS Pro
4. On the ribbon, select Insert --> Toolbox --> Add Toolbox
5. Go to the folder where you unzipped RAMBO, select the `.tbx` file (with red icon), and press 'OK'
5. Open the Catalog pane --> Toolboxes --> The WDPA QA toolbox should now be visible.
6. Expand the toolbox, so that the embedded scripts become visible.
4. Right-click the script to run (e.g. for polygons or points), click Open, and specify the input table (feature class attribute table) to be checked, and the output directory.
5. Click Run, and click 'View Details' if you wish to see the progress
6. The Excel output will be present in the previously specified output directory.

### *Developers only:* Creating the ArcGIS toolbox

1. Open a blank project in ArcGIS Pro
2. On the ribbon, select Insert --> Toolbox --> New Toolbox
3. Specify the name of the toolbox
4. Once created, the toolbox will be present in the Catalog, under Toolboxes.
5. Right-click the created toolbox --> New --> Script
6. In tab 'General', specify the name and label, then point to a script containing the main functions (`poly.py` or `point.py`).
7. Ensure boxes 'Import script' and 'Store tool with relative path' are checked
8. In tab 'Parameters', add two parameters to specify the input type and the output folder
   - Label: WDPA polygon, Data Type: Feature Class, Type: Required, Direction: Input
   - Label: Output folder, Data Type: Folder, Type: Required, Direction: Input
9. Repeat steps 5-8 for another script if required (i.e. `poly.py` or `point.py`)
10. Finally, add the toolbox and the WDPA folder (containing the QA scripts) collectively in a single compressed file. Subsequently, wherever this folder is uncompressed, the toolbox will be in the same folder as the WDPA QA scripts. This makes RAMBO portable.

---

## Troubleshooting common errors when running RAMBO

#### 1. "Permission denied"

The Excel workbook with QA results is still open and RAMBO is trying to overwrite it. Close the workbook and give it a new name if it should not be overwritten, then try again.

#### 2. "RuntimeError: A column was specified that does not exist."

Your input was Points data while you tried to run the Polygon script. Specify the correct input and output, and try again.

#### 3. "RuntimeError: Not signed into Portal."

You do not have an internet connection. Connect to the internet, ensure that you are logged into the ArcGIS Pro portal, and try again.

---

## Exploring RAMBO's output in Excel

### General notes on the Excel workbook

- The filename of the Excel workbook is comprised of the day RAMBO was run, along with the type of input ('poly' or 'points'). The filename is written as per the following:

`[present_date]`_WDPA_QA_checks_`[datatype]`.xlsx

- **The RAMBO output file will be overwritten without warning**, if you have run a toolbox script (e.g. the WDPA QA for points data), and you run the same script again on the same day while leaving the output folder unchanged. If you wish to run the same script multiple times on one day, either change the output filename after running the script, or specify a different output folder.

### Summary sheet

This sheet contains an overview of the checks' results.

There are 3 labels:

-	**Fail**: violations of the WDPA rules or general logic 
    - E.g. PA_DEF = 5
    - E.g. REP_M_AREA > REP_AREA.
-	**Check**: verification required whether these are true errors (e.g. ‘tiny_gis_area’ shows areas with a size smaller than 100 m2).
    - E.g. for the same WDPAID, the associated WDPA_PIDs have different values for field NAME.
-	**Pass**: no errors found.

### Navigation

In the Summary sheet, the checks' names are hyperlinks: clicking one of them will bring you directly to the Excel sheet containing all errors found by that check.

Each sheet contains a hyperlink in cell A1, called 'To Summary'. Clicking this will bring you back to the Summary sheet. 

By default the first column and first row are frozen, so that the headers are always visible, and you can always click the 'To Summary' hyperlink to return to the Summary sheet.

### Sheets

Each check that returned errors has its own Excel sheet. The name of this sheet is the same as the name of the check as listed in the Summary sheet. Sheets' tabs are colour-coded, and tab colours correspond with the Summary result (red for 'Fail', blue for 'Check').

---

## Description of QA checks

Note: the checks have different names in the Excel file than in the quality assurance script (`qa.py`). The overview below shows both the name of the check as used in the Excel file, and the name of function in the script.

---

### duplicate_wdpa_pid
###### Script function name: `duplicate_wdpa_pid`

Duplicate WDPA_PIDs present. WDPA_PIDs must be unique throughout the entire WDPA.

---

### tiny_rep_area
###### Script function name: `area_invalid_rep_area`

The REP_AREA is smaller than 0.0001 km² (100 m²). This only requires a check, as the is the protected area could be extremely small.

---

### zero_rep_m_area_marine12
###### Script function name: `area_invalid_rep_m_area_marine12`

MARINE = 1 or 2, but REP_M_AREA is smaller than or equal to 0. This only requires a check, as REP_M_AREA could be 0 due to the way data providers share their information.

---

### ivd_rep_m_area_gt_rep_area
###### Script function name: `area_invalid_rep_m_area_rep_area`

REP_M_AREA is greater than REP_AREA. REP_M_AREA can only be equal to or smaller than REP_AREA.

---

### ivd_no_tk_area_gt_rep_m_area
###### Script function name: `area_invalid_no_tk_area_rep_m_area`

NO_TK_AREA is larger than REP_M_AREA. NO_TK_AREA can only be equal to or smaller than REP_M_AREA.

---

### ivd_no_tk_area_rep_m_area
###### Script function name: `invalid_no_take_no_tk_area_rep_m_area`

NO_TAKE value is 'All', but NO_TK_AREA is not the same value as REP_M_AREA.

---

### ivd_int_crit_desig_eng_other
###### Script function name: `invalid_int_crit_desig_eng_other`

DESIG_ENG is neither 'Ramsar Site, Wetland of International Importance', nor 'World Heritage Site (natural or mixed)', and the INT_CRIT is not the accepted value 'Not Applicable'.

Note: 'Not Applicable' is the only accepted value if DESIG_ENG is not 'Ramsar Site, Wetland of International Importance' or 'World Heritage Site (natural or mixed)'.

---

### ivd_desig_eng_iucn_cat_other
###### Script function name: `invalid_desig_eng_iucn_cat_other`

DESIG_ENG is neither 'UNESCO-MAB Biosphere Reserve' nor 'World Heritage Site (natural or mixed)', and the IUCN_CAT is not any of the following accepted values:

- Ia
- Ib
- II
- III
- IV
- V
- VI
- Not Reported
- Not Assigned

Note: 'Not Applicable' is only accepted if DESIG_ENG is 'UNESCO-MAB Biosphere Reserve' or 'World Heritage Site (natural or mixed)'.

---

### dif_name_same_id
###### Script function name: `inconsistent_name_same_wdpaid`

Inconsistencies in the NAME field for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in NAME per parcel (WDPA_PID).

---

### dif_orig_name_same_id
###### Script function name: `inconsistent_orig_name_same_wdpaid`

Inconsistencies in the ORIG_NAME field for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in ORIG_NAME per parcel (WDPA_PID).

---

### ivd_dif_desig_same_id
###### Script function name: `inconsistent_desig_same_wdpaid`

Inconsistencies in the DESIG field for WDPA_PIDs with the same WDPAID. It must be one protected area (and WDPAID) per designation. WDPA_PIDs with the same WDPAID (i.e. parcels) cannot have different designations.

---

### ivd_dif_desig_eng_same_id
###### Script function name: `inconsistent_desig_eng_same_wdpaid`

Inconsistencies in the DESIG_ENG field for WDPA_PIDs with the same WDPAID. It must be one protected area (and WDPAID) per designation. WDPA_PIDs with the same WDPAID cannot have different designations.

---

### dif_desig_type_same_id
###### Script function name: `inconsistent_desig_type_same_wdpaid`

Inconsistencies in DESIG_TYPE for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in DESIG_TYPE per parcel (WDPA_PID).

---

### dif_int_crit_same_id
###### Script function name: `inconsistent_int_crit_same_wdpaid`

Inconsistencies in INT_CRIT for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in INT_CRIT per parcel (WDPA_PID).

---

### dif_no_take_same_id
###### Script function name: `inconsistent_no_take_same_wdpaid`

Inconsistencies in NO_TAKE for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in NO_TAKE per parcel (WDPA_PID).

---

### dif_status_same_id
###### Script function name: `inconsistent_status_same_wdpaid`

Inconsistencies in STATUS for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in STATUS per parcel (WDPA_PID).

---

### dif_status_yr_same_id
###### Script function name: `inconsistent_status_yr_same_wdpaid`

Inconsistencies in STATUS_YR for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in STATUS_YR per parcel (WDPA_PID).

---

### dif_gov_type_same_id
###### Script function name: `inconsistent_gov_type_same_wdpaid`

Inconsistencies in GOV_TYPE for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in GOV_TYPE per parcel (WDPA_PID).

---

### dif_own_type_same_id
###### Script function name: `inconsistent_own_type_same_wdpaid`

Inconsistencies in OWN_TYPE for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in OWN_TYPE per parcel (WDPA_PID).

---

### dif_mang_auth_same_id
###### Script function name: `inconsistent_mang_auth_same_wdpaid`

Inconsistencies in MANG_AUTH for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in MANG_AUTH per parcel (WDPA_PID).

---

### dif_mang_plan_same_id
###### Script function name: `inconsistent_mang_plan_same_wdpaid`

Inconsistencies in MANG_PLAN for WDPA_PIDs with the same WDPAID. This only requires a check as the same protected area (WDPAID) is allowed to have a different value in MANG_PLAN per parcel (WDPA_PID).

---

### ivd_dif_verif_same_id
###### Script function name: `inconsistent_verif_same_wdpaid`

Inconsistencies in VERIF for WDPA_PIDs with the same WDPAID. The same protected area (WDPAID) cannot have a different value in VERIF per parcel (WDPA_PID).

---

### ivd_dif_metadataid_same_id
###### Script function name: `inconsistent_metadataid_same_wdpaid`

Inconsistencies in METADATAID for WDPA_PIDs with the same WDPAID. The same protected area (WDPAID) cannot have a different value in METADATAID per parcel (WDPA_PID).

---

### ivd_dif_sub_loc_same_id
###### Script function name: `inconsistent_sub_loc_same_wdpaid`

Inconsistencies in SUB_LOC for WDPA_PIDs with the same WDPAID. The same protected area (WDPAID) cannot have a different value in SUB_LOC per parcel (WDPA_PID).

---

### ivd_dif_parent_iso3_same_id
###### Script function name: `inconsistent_parent_iso3_same_wdpaid`

Inconsistencies in PARENT_ISO3 for WDPA_PIDs with the same WDPAID. The same protected area (WDPAID) cannot have a different value in PARENT_ISO3 per parcel (WDPA_PID).

---

### ivd_dif_iso3_same_id
###### Script function name: `inconsistent_iso3_same_wdpaid`

Inconsistencies in ISO3 for WDPA_PIDs with the same WDPAID. The same protected area (WDPAID) cannot have a different value in ISO3 per parcel (WDPA_PID).

---

### ivd_pa_def
###### Script function name: `invalid_pa_def`

PA_DEF is unequal to 1, which is the only accepted value.

---

### ivd_desig_eng_international
###### Script function name: `invalid_desig_eng_international`

DESIG_TYPE is 'International', but DESIG_ENG is not any of the following accepted values for International sites:

- Ramsar Site, Wetland of International Importance
- UNESCO-MAB Biosphere Reserve 
- World Heritage Site (natural or mixed)

---

### ivd_desig_type_international
###### Script function name: `invalid_desig_type_international`

DESIG_TYPE is not 'International', but DESIG_ENG is any of the following accepted values for International sites:

- Ramsar Site, Wetland of International Importance
- UNESCO-MAB Biosphere Reserve
- World Heritage Site (natural or mixed)

---

### ivd_desig_eng_regional
###### Script function name: `invalid_desig_eng_regional`

DESIG_TYPE is 'Regional', but DESIG_ENG is not any of the following accepted values for Regional sites:

- Baltic Sea Protected Area (HELCOM)
- Specially Protected Area (Cartagena Convention)
- Marine Protected Area (CCAMLR)
- Marine Protected Area (OSPAR)
- Site of Community Importance (Habitats Directive)
- Special Protection Area (Birds Directive)
- Specially Protected Areas of Mediterranean Importance (Barcelona Convention)

---

### ivd_desig_type_regional
###### Script function name: `invalid_desig_type_regional`

DESIG_TYPE is not 'Regional', but DESIG_ENG is any of the following accepted values for Regional sites:

- Baltic Sea Protected Area (HELCOM)
- Specially Protected Area (Cartagena Convention)
- Marine Protected Area (CCAMLR)
- Marine Protected Area (OSPAR)
- Site of Community Importance (Habitats Directive)
- Special Protection Area (Birds Directive)
- Specially Protected Areas of Mediterranean Importance (Barcelona Convention)

---

### ivd_int_crit
###### Script function name: `invalid_int_crit_desig_eng_ramsar_whs`

DESIG_ENG is 'Ramsar Site, Wetland of International Importance'  or 'World Heritage Site (natural or mixed)', but INT_CRIT is not one of the accepted values (>1000 possible values), which is any combination of the following: 

- (i)
- (ii)
- (iii)
- (iv)
- (v)
- (vi)
- (vii)
- (viii)
- (ix)
- (x)

Note: combinations of accepted values should not contain any symbols (e.g. commas) or spaces in between them. 

*Example*

Accepted format: (i)(ii)(vi)

Not accepted: (i) (ii) (vi)

Not accepted: (i),(ii),(vi)

Not accepted: (i);(ii);(vi)

Etc.

---

### ivd_desig_type
###### Script function name: `invalid_desig_type`

DESIG_TYPE is not any of the following accepted values: 

- National
- Regional
- International
- Not Applicable

---

### ivd_iucn_cat
###### Script function name: `invalid_iucn_cat`

IUCN_CAT is not any of the following accepted values:

- Ia
- Ib
- II
- III
- IV
- V
- VI
- Not Reported
- Not Applicable
- Not Assigned

---

### ivd_iucn_cat_unesco_whs
###### Script function name: `invalid_iucn_cat_unesco_whs`

DESIG_ENG is 'UNESCO-MAB Biosphere Reserve' or 'World Heritage Site (natural or mixed)', but IUCN_CAT is a different value than 'Not Applicable'.

---

### ivd_marine
###### Script function name: `invalid_marine`

MARINE is unequal to 0, 1, or 2

Note: datatype for field MARINE is *string*.

---

### check_no_take_marine0
###### Script function name: `invalid_no_take_marine0`

MARINE = 0, but NO_TAKE is a different value than 'Not Applicable'.

I.e. terrestrial protected areas (MARINE = 0) have a NO_TAKE other than 'Not Applicable'.

---

### ivd_no_take_marine12
###### Script function name: `invalid_no_take_marine12`

MARINE = 1 or 2, but NO_TAKE is not any of the following accepted values:

- All
- Part
- None
- Not Reported 

---

### check_no_tk_area_marine0
###### Script function name: `invalid_no_tk_area_marine`

MARINE = 0, but NO_TK_AREA is unequal to 0.

I.e. terrestrial protected areas (MARINE = 0) have a NO_TK_AREA other than 0.

---

### ivd_no_tk_area_no_take
###### Script function name: `invalid_no_tk_area_no_take`

NO_TK_AREA is unequal to 0 while NO_TAKE is 'Not Applicable'.

---

### ivd_status
###### Script function name: `invalid_status`

STATUS is not any of the following accepted values:

- Proposed
- Inscribed
- Adopted
- Designated
- Established

---

### ivd_status_yr
###### Script function name: `invalid_status_yr` 

STATUS_YR is invalid. It can only be between 1750 and present year, or the value of 0 (if the year is not reported).

---

### ivd_gov_type
###### Script function name: `invalid_gov_type`

GOV_TYPE is not any of the following accepted values:

- Federal or national ministry or agency
- Sub-national ministry or agency
- Government-delegated management
- Transboundary governance
- Collaborative governance
- Joint governance
- Individual landowners
- Non-profit organisations
- For-profit organisations
- Indigenous peoples
- Local communities
- Not Reported

---

### ivd_own_type
###### Script function name: `invalid_own_type`

OWN_TYPE is not any of the following accepted values:

- State
- Communal
- Individual landowners
- For-profit organisations
- Non-profit organisations
- Joint ownership
- Multiple ownership
- Contested
- Not Reported

---

### ivd_verif
###### Script function name: `invalid_verif`

VERIF is not any of the following accepted values: 

- State Verified
- Expert Verified
- Not Reported

---

### check_parent_iso3
###### Script function name: `invalid_parent_iso3`

PARENT_ISO3 is not any of the accepted ISO3 values, or 'ABNJ'.

The accepted values are obtained from a .csv file located on a GitHub repository (latest update: 19 March 2019):

https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv

Link to the repository:

https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

Note: this list is updated periodically. Please check with the WDPA and/or data manager to make sure you are using the most up to date list.

---

### check_iso3
###### Script function name: `invalid_parent_iso3`

ISO3 is not any of the accepted ISO3 values, or 'ABNJ'. For accepted ISO3 values, see 'check_parent_iso3' above.

---

### ivd_status_desig_type
###### Script function name: `invalid_status_desig_type`

DESIG_TYPE is 'Not Applicable', but STATUS is not 'Established'.

---

### ivd_character_name
###### Script function name: `forbidden_character_name`

Forbidden characters present in NAME.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### ivd_character_orig_name
###### Script function name: `forbidden_character_orig_name`

Forbidden characters present in ORIG_NAME.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### ivd_character_desig
###### Script function name: `forbidden_character_desig`

Forbidden characters present in DESIG.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### ivd_character_desig_eng
###### Script function name: `forbidden_character_desig_eng`

Forbidden characters present in DESIG_ENG.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### ivd_character_mang_auth
###### Script function name: `forbidden_character_mang_auth`

Forbidden characters present in MANG_AUTH.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### ivd_character_mang_plan
###### Script function name: `forbidden_character_mang_plan`

Forbidden characters present in MANG_PLAN.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

### ivd_character_sub_loc
###### Script function name: `forbidden_character_sub_loc`

Forbidden characters present in SUB_LOC.

Forbidden characters:

- `<`
- `>`
- `?`
- `*`
- `\r` (new-line character)
- `\n` (new-line character)

Note: if a WPDA_PID has been flagged but you cannot see anything wrong, it is most likely a new-line character error. Double click on the cell in ArcGIS Pro to see (they do not consistently appear in Excel). The new-line characters appear as one or multiple empty white lines below or above the cell's value when you explore this in ArcGIS Pro, or they break up a value in two lines.

---

### nan_present_name
Scipt function name: `nan_present_name`

NaN / NA present in NAME. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_orig_name
###### Script function name: `nan_present_orig_name`

NaN / NA present in ORIG_NAME. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_desig
###### Script function name: `nan_present_desig`

NaN / NA present in DESIG. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_desig_eng
###### Script function name: `nan_present_desig_eng`

NaN / NA present in DESIG_ENG. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_mang_auth
###### Script function name: `nan_present_mang_auth`

NaN / NA present in MANG_AUTH. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_mang_plan
###### Script function name: `nan_present_mang_plan`

NaN / NA present in MANG_PLAN. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### nan_present_sub_loc
###### Script function name: `nan_present_sub_loc`

NaN / NA present in SUB_LOC. These values are 'Not a Number' and could be the result of a range of errors or a calculation such as division by 0.

---

### gis_area_gt_rep_area
###### Script function name: `area_invalid_too_large_gis`

GIS_AREA is too large compared to REP_AREA. This may not be an error and can just be attributed to a lack of reporting from the data provider.

WDPA_PIDs will be picked up if they comply with two rules:

1. The absolute difference between the two areas is greater than 50 km².
2. The proportion of GIS_AREA compared to REP_AREA falls outside of a distribution calculated.

This distribution is produced by calculating the following for each WDPA_PID in the WDPA: 

    (REP_AREA + GIS_AREA) / REP_AREA

Then, the mean and standard deviation of this distribution is calculated. However, if the product of this calculation is larger than 100 (e.g. if REP_AREA is 0) or smaller than 0 (e.g. if REP_AREA is negative), then these WDPA_PIDs are left out to calculate the mean and standard deviation. 

Subsequently, the maximum accepted value is calculated as per the following: 

    mean + 2 * standard deviation

If the product of (REP_AREA + GIS_AREA) / REP_AREA is larger than this maximum, the WDPA_PID will be output as an error.

---

### rep_area_gt_gis_area
###### Script function name: `area_invalid_too_large_rep`

REP_AREA is too large compared to GIS_AREA. This may not be an error and can just be attributed to a lack of reporting from the data provider.

WDPA_PIDs will be picked up if they comply with two rules:

1. The absolute difference between the two areas is greater than 50 km².
2. The proportion of REP_AREA compared to GIS_AREA falls outside of a distribution calculated.

This distribution is produced by calculating the following for each WDPA_PID in the WDPA: 

    (REP_AREA + GIS_AREA) / GIS_AREA

Then, the mean and standard deviation of this distribution is calculated. However, if the product of this calculation is larger than 100 (e.g. if GIS_AREA is 0) or smaller than 0 (e.g. if GIS_AREA is negative), then these WDPA_PIDs are left out to calculate the mean and standard deviation. 

Subsequently, the maximum accepted value is calculated as per the following: 

    mean + 2 * standard deviation

If the product of (REP_AREA + GIS_AREA) / GIS_AREA is larger than this maximum, the WDPA_PID will be output as an error. 

---

### gis_m_area_gt_rep_m_area
###### Script function name: `area_invalid_too_large_gis_m`

GIS_M_AREA is too large compared to REP_M_AREA. This may not be an error and can just be attributed to a lack of reporting from the data provider.

WDPA_PIDs will be picked up if they comply with two rules:

1. The absolute difference between the two areas is greater than 50 km².
2. The proportion of GIS_M_AREA compared to REP_M_AREA falls outside of a distribution calculated.

This distribution is produced by calculating the following for each WDPA_PID in the WDPA: 

    (REP_M_AREA + GIS_M_AREA) / REP_M_AREA

Then, the mean and standard deviation of this distribution is calculated. However, if the product of this calculation is larger than 100 (e.g. if REP_M_AREA is 0) or smaller than 0 (e.g. if REP_M_AREA is negative), then these WDPA_PIDs are left out to calculate the mean and standard deviation.

Subsequently, the maximum accepted value is calculated as per the following: 

    mean + 2 * standard deviation

If the product of (REP_M_AREA + GIS_M_AREA) / REP_M_AREA is larger than this maximum, the WDPA_PID will be output as an error.

---

### rep_m_area_gt_gis_m_area
###### Script function name: `area_invalid_too_large_rep_m`

REP_M_AREA is too large compared to GIS_M_AREA. This may not be an error and can just be attributed to a lack of reporting from the data provider.

WDPA_PIDs will be picked up if they comply with two rules:

1. The absolute difference between the two areas is greater than 50 km².
2. The proportion of REP_M_AREA compared to GIS_M_AREA falls outside of a distribution calculated.

This distribution is produced by calculating the following for each WDPA_PID in the WDPA: 

    (REP_M_AREA + GIS_M_AREA) / GIS_M_AREA

Then, the mean and standard deviation of this distribution is calculated. However, if the product of this calculation is larger than 100 (e.g. if GIS_M_AREA is 0) or smaller than 0 (e.g. if GIS_M_AREA is negative), then these WDPA_PIDs are left out to calculate the mean and standard deviation. 

Subsequently, the maximum accepted value is calculated as per the following: 

    mean + 2 * standard deviation

If the product of (REP_M_AREA + GIS_M_AREA) / GIS_M_AREA is larger than this maximum, the WDPA_PID will be output as an error. 

---

### tiny_gis_area
###### Script function name: `area_invalid_gis_area`

The GIS_AREA is smaller than 0.0001 km² (100 m²). This only requires a check, as the is the protected area could be extremely small.

---

### no_tk_area_gt_gis_m_area
###### Script function name: `area_invalid_no_tk_area_gis_m_area`

NO_TK_AREA is larger than GIS_M_AREA. The NO_TK_AREA can only be equal to or smaller than the GIS_M_AREA.

---

### ivd_gis_m_area_gt_gis_area
###### Script function name: `area_invalid_gis_m_area_gis_area`

GIS_M_AREA is larger than GIS_AREA. The GIS_M_AREA can only be equal to or smaller than the GIS_AREA.

---

### zero_gis_m_area_marine12
###### Script function name: `area_invalid_gis_m_area_marine12`

GIS_M_AREA is smaller than or equal to 0 while MARINE = 1 or 2.

---

### ivd_marine_designation
###### Script function name: `area_invalid_marine`

The MARINE value is incorrect based on GIS calculations.

This check produces two new columns. One column, named marine_GIS_proportion, is the product of the following calculation:

    GIS_M_AREA / GIS_AREA

The second column, named marine_GIS_value, contains a value (0, 1, or 2) based on the official WDPA manual (v1.6) thresholds to designate the MARINE value, as stated below.

- marine_GIS_value = 0 if: 

`GIS_M_AREA / GIS_AREA` is smaller than or equal to 0.1

- marine_GIS_value = 1 if:

`GIS_M_AREA / GIS_AREA` is larger than 0.1 but smaller than 0.9

- marine_GIS_value = 2 if:

`GIS_M_AREA / GIS_AREA` is larger than or equal to 0.9

If the marine_GIS_value is unequal to the MARINE value, then this is an error.

---

END OF WIKI.