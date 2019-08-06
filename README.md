# Description

This is a Python module that automates the Quality Assurance of the World Database on Protected Areas. It is integrated in an ArcGIS toolbox and can be run in ArcGIS Pro.

### CHECK THIS
Input: WDPA feature class attribute table, e.g. polygons

Output: Excel Workbook with identified errors. 

**For in-depth usage and the description of checks included, please check the Wiki page on this GitHub repository.**

---

# Proposing improvements to this script: Push

Please refrain from committing directly to the `master` branch. Instead, create a different branch containing edits and submit a pull request. 

```
git checkout -b {your branch} {base branch}
```

---

# Installation requirements - ADD PYTHON ENVIRONMENT CREATION IF NECESSARY

- ArcGIS Pro `2.4` or later 
- Python `3.6.8` or later (included in ArcGIS Pro `2.4`)

Note: installing Anaconda is not required. Refrain from using any other Conda installation than the one that comes with ArcGIS Pro installation.

---

# Installation

1. Clone ArcGIS Pro's default Python environment called `arcgispro-py3`, and access ArcGIS Pro's Conda using the command-prompt
2. Explain how to get there (see walkthrough)
3. 


3. If packages specified under 'Installation requirements' are older than those installed, update these using the command-prompt. 




- Python packages:
	- Pandas `0.25`
	- NumPy `1.16.4`
	- OpenPyXL `2.6.1`

Installed Python packages can be viewed and updated through ArcGIS Pro. Go to 'Settings', access 'Python' tab, which will lead you to the Python Package Manager. Here, packages can be installed or updated. Note that in order to update your own 

# Quick start - NEEDS MORE DETAIL

1. Download the WDPA QA toolbox 
2. Extract the file
3. Import toolbox into ArcGIS Pro
4. Point the toolbox to the correct script (`poly.py`, `point.py`)
5. Provide WDPA table input
6. Specify output folder
7. Run
8. Explore the results in Excel

---

# Credits

Author: Stijn den Haan

Supervisor: Yichuan Shi

Bioinformatics internship • UNEP-WCMC • 10 June - 9 August 2019

---

# Wish list: improving the QA

- Add `METADATAID` check: compare the `METADATAID`s present in the WDPA Polygon and Point tables, to the Source Table.
- Add a check for empty cells
- Improve invalid `ISO3` check: currently, Protected Areas which have more than one `ISO3` value are flagged. Instead, split up those entries that contain multiple `ISO3` values, separated by `;`, and compare those individually to the list of allowed `ISO3` values. 

