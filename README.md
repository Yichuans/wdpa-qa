# RAMBO: a Quality Assurance Tool for the World Database on Protected Areas

## Description

RAMBO is a quality assurance tool developed for the World Database on Protected Areas, and can be run in ArcGIS Pro. The quality assurance (QA) scripts have been written in Python.

*Input*: Feature class attribute table that conforms to the official WDPA format. Currently, polygon and point feature class attribute tables are the only allowed inputs.

*Output*: Excel Workbook with identified errors.

**For in-depth usage and a description of Quality Assurance checks included, please check the Wiki page on this GitHub repository.**

---

## Proposing improvements to this script: Push

Please refrain from committing directly to the `master` branch. Instead, create a different branch containing edits and submit a pull request. 

```
git checkout -b {your branch} {base branch}
```

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

## Quick start

1. Download the latest WDPA QA toolbox version from this GitHub repository (folder 'QA_toolbox')
2. Extract the file on your computer
3. Add the QA toolbox in an ArcGIS Pro project
4. Double-click (expand) the toolbox and open the script to run (for Point or Polygon feature class attribute tables)
5. Specify the WDPA input feature class attribute table
6. Specify the output folder
7. Click 'Run'
8. Explore the results in Excel
9. In case you encounter errors upon running the tool, please see the Wiki page of this GitHub repository to troubleshoot

---

## Improving RAMBO: wish list

- Halt script if your input is Polygon data while you run the Points script. At present it runs, but GIS checks are not present in the Points script, and therefore no GIS errors are output. Idea: incorporate a check in the `arcgis_table_to_df` function: if the length (total number) of fields present in the `in_fc` is unequal to the length of final_fields, throw an error.
- Add `METADATAID` check: compare the `METADATAID`s present in the WDPA Polygon and Point tables, to the Source Table.
- Add a check for empty cells
- Improve invalid `ISO3` check: currently, Protected Areas which have more than one `ISO3` value are flagged. Instead, split up those entries that contain multiple `ISO3` values, separated by `;`, and compare those individually to the list of allowed `ISO3` values.
- Make the name of the input feature class a part of the Excel output's filename.
- If useful: add function that is the `GIS_M_AREA` equivalent of `ivd_no_tk_area_rep_m_area`: flag `WDPA_PIDs` whose `NO_TAKE` value is `All`, but `NO_TK_AREA` is not the same value as `GIS_M_AREA`.
- Add a single check for `Null` values for all fields

---

## Credits

Author: Stijn den Haan

Supervisor: Yichuan Shi

Bioinformatics internship • UNEP-WCMC • 10 June - 9 August 2019

---
