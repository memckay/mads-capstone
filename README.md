# MADS Capstone: Healthcare Heroes

University of Michigan, Master of Applied Data Science capstone research project.

## Overview

Does regional physician-group quality, measured by Medicare's Merit-based Incentive Payment System
(MIPS), relate to county-level Medicare outcomes such as hospital readmissions once county
characteristics are accounted for? This project builds a county panel from public CMS data and tests
the question with unsupervised and supervised models.

**Finding.** The supervised analysis finds at most a small, borderline association that does not
survive adjustment for a county's own prior outcomes; details and caveats are in `04_supervised_learning`.

## Notebooks (run in order)

1. `01_loading_data`: load and explore the raw CMS files
2. `02_zip_county_crosswalk`: map physician groups to counties and build the analytic table
3. `03_unsupervised_learning`: PCA and clustering on county MIPS profiles
4. `04_supervised_learning`: does MIPS predict county outcomes beyond demographics?
5. `05_supervised_learning_extensions`: population weighting and PCA robustness checks

## Setup

Requires Python 3.11 or newer (developed on 3.13).

```
python -m pip install -r requirements.txt
```

Run the notebooks in numbered order; each depends on outputs from earlier ones (for example, `04`
uses the table built in `02` and the clusters from `03`, and `05` uses the frame exported by `04`).
The pipeline runs in a few minutes once the data is in `data/raw/`.

## Data

All source data is public and is not committed to the repository. The exact file versions are recorded
in `data/manifest.yaml`, each with a fingerprint that confirms you have the identical file; download
them into `data/raw/` before running the notebooks.

| Dataset | Role | Source |
|---|---|---|
| Group MIPS performance | predictor | [CMS Provider Data Catalog `0ba7-2cb0`](https://data.cms.gov/provider-data/dataset/0ba7-2cb0) |
| Doctors & Clinicians national file | group to ZIP and specialty | [CMS Provider Data Catalog `mj5m-pzi6`](https://data.cms.gov/provider-data/dataset/mj5m-pzi6) |
| Medicare Geographic Variation | county outcomes and controls | [CMS Summary Statistics](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-geographic-comparisons/medicare-geographic-variation-by-national-state-county) |
| ZIP-to-county crosswalk | geography | [HUD USPS ZIP Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html) |

Notebook 04 also downloads US county boundaries (county FIPS GeoJSON) automatically for the maps. The
CMS and HUD data are public U.S. government works; source licenses are respected for use and
redistribution.

## Repository layout

```
data/         raw (gitignored) and processed inputs, plus the pinned manifest
notebooks/    the analysis pipeline, run in numbered order
reports/      figures and outputs
requirements.txt
```

## Authors

Transaint Gau, Maria Paz, Zachary Sletten, and Justin Tseng. University of Michigan, SIADS 699.

## License and use

Coursework for the University of Michigan Master of Applied Data Science (SIADS 699); the code is
shared for academic review. The source data is public and remains under its original terms: the CMS
and HUD files are U.S. government works in the public domain.
