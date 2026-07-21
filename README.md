# MADS Capstone: Healthcare Heroes

University of Michigan, Master of Applied Data Science capstone research project.

## Overview

Does regional physician-group quality, measured by Medicare's Merit-based Incentive Payment System
(MIPS), relate to county-level Medicare outcomes such as hospital readmissions once county
characteristics are accounted for? This project builds a county panel from public CMS data and tests
the question with unsupervised and supervised models.

**Finding.** The supervised analysis finds at most a small, borderline association that does not
survive adjustment for a county's own prior outcomes: it reads as one stable county trait tracking
another, and as a lower bound given exposure misattribution. Details and caveats are in
[`04_supervised_learning`](notebooks/04_supervised_learning.ipynb); key figures are in
[`reports/figures/`](reports/figures).

## Notebooks

1. [`01_loading_data`](notebooks/01_loading_data.ipynb): load and explore the raw CMS files
2. [`02_zip_county_crosswalk`](notebooks/02_zip_county_crosswalk.ipynb): map physician groups to counties; documents how the analytic table is built (later notebooks load the pinned artifact, not a fresh build)
3. [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb): PCA and clustering on county MIPS profiles
4. [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb): does MIPS predict county outcomes beyond demographics?
5. [`05_supervised_learning_extensions`](notebooks/05_supervised_learning_extensions.ipynb): population weighting and PCA robustness checks

## Setup

Requires Python 3.11 or newer (developed on 3.13 and 3.14; the `requirements.txt` versions were pinned on 3.13).

```
python -m pip install -r requirements.txt
```

Run the notebooks in numbered order. Notebook 03 writes the cluster labels that notebook 04 reads.

Inputs live in two folders:
- **Raw source files** go in `data/raw/` (see the Data section below).
- **Team-built artifacts** go in `data/processed/`: `analytic_measure.csv.gz` (the county-by-measure
  table read by notebooks 03 and 04) and `county_clusters.csv`. Notebook 02 documents how
  `analytic_measure.csv.gz` is built, but the pipeline does not regenerate it; notebooks 03 and 04
  load this pinned copy. Get both from the team's shared Drive (ask a maintainer) and verify each
  `sha256` against [`data/manifest.yaml`](data/manifest.yaml).

The pipeline runs in a few minutes once the data is in place.

## Data

Source data is not committed. [`data/manifest.yaml`](data/manifest.yaml) lists each dataset's exact
version and a fingerprint to verify it; download the files into `data/raw/` before running the
notebooks. CMS and HUD rotate their download URLs, so if a link stops working, match the file by its
`sha256` in the manifest. The HUD crosswalk has no stable direct URL: download the ZIP-COUNTY file
manually from the landing page and confirm its `sha256`.

| Dataset | Role | Source |
|---|---|---|
| Group MIPS performance | predictor | [CMS Provider Data Catalog `0ba7-2cb0`](https://data.cms.gov/provider-data/dataset/0ba7-2cb0) |
| Doctors & Clinicians national file | group to ZIP and specialty | [CMS Provider Data Catalog `mj5m-pzi6`](https://data.cms.gov/provider-data/dataset/mj5m-pzi6) |
| Medicare Geographic Variation | county outcomes and controls | [CMS Summary Statistics](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-geographic-comparisons/medicare-geographic-variation-by-national-state-county) |
| ZIP-to-county crosswalk | geography | [HUD USPS ZIP Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html) |

Notebook 04 also downloads US county boundaries (county FIPS GeoJSON) automatically for the maps.

## Repository layout

```
data/         pinned manifest and small MIPS reference tables (bulk raw, interim, and processed data is gitignored)
notebooks/    the analysis pipeline
reports/      figures
requirements.txt
```

## Authors

Transaint Gau, Maria Paz, Zachary Sletten, and Justin Tseng. University of Michigan, SIADS 699.

## License and use

Coursework for the University of Michigan Master of Applied Data Science (SIADS 699); the code is
shared for academic review. The source data is U.S. government data (CMS and HUD), not committed here;
each source's own terms apply.
