# RAMBO: a Quality Assurance Tool for the World Database on Protected Areas

## Description

RAMBO is a quality assurance tool developed for the World Database on Protected Areas, and can be run in ArcGIS Pro. The quality assurance (QA) scripts have been written in Python.

*Input*: Feature class attribute table that conforms to the official WDPA format. Currently, polygon and point feature class attribute tables are the only allowed inputs.

*Output*: Excel Workbook with identified errors.

**For in-depth usage and a description of Quality Assurance checks included, please check the [Wiki page](https://github.com/Yichuans/wdpa-qa/wiki) on this GitHub repository.**

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

## Quick start

1. Download RAMBO (the WDPA QA tool), from this GitHub repository.
2. Unzip the file in a folder of your choosing.
3. Open a (non-empty / empty) project in ArcGIS Pro.
4. On the ribbon, select Insert --> Toolbox --> Add Toolbox.
5. Go to the folder where you unzipped RAMBO, select the `.tbx` file (with red icon), and press 'OK'.
6. Open the Catalog pane --> Toolboxes --> The WDPA QA toolbox should now be visible.
7. Expand the toolbox, so that the embedded scripts become visible.
8. Right-click the script to run (e.g. for polygons or points), click Open, and specify the input table (feature class attribute table) to be checked, and the output directory.
9. Click Run, and click 'View Details' if you wish to see the progress.
10. The Excel output will be present in the previously specified output directory.
11. If you encounter errors, please refer to the Troubleshooting section in the Wiki.

## Notes

Please refrain from committing directly to the `master` branch. Instead, create a different branch containing edits and submit a pull request. 

```bash
git checkout -b {your branch} {base branch}
```

Run tests with

```bash
python -m unittest
```

## next steps

- (Done) Add `METADATAID` check: compare the `METADATAID`s present in the WDPA Polygon and Point tables, to the Source Table.
- (Done) Add a check for empty cells
- (Done) Improve invalid `ISO3` check: currently, Protected Areas which have more than one `ISO3` value are flagged. Instead, split up those entries that contain multiple `ISO3` values, separated by `;`, and compare those individually to the list of allowed `ISO3` values.
- (Duplicate?) Add a single check for `Null` values for all fields
- (Done) Check whether there are any duplicate `WDPA_PID`s between Points and Polygon feature class attribute tables.

## ideas
- Make the name of the input feature class a part of the Excel output's filename.
- If useful: add function that is the `GIS_M_AREA` equivalent of `ivd_no_tk_area_rep_m_area`: flag `WDPA_PIDs` whose `NO_TAKE` value is `All`, but `NO_TK_AREA` is not the same value as `GIS_M_AREA`.
- Add forbidden characters checks for the fields of the Source table.

## Credits

Author: Stijn den Haan

Supervisor: Yichuan Shi

Bioinformatics internship • UNEP-WCMC • 10 June - 9 August 2019

---
