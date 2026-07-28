# MADS Capstone: Healthcare Heroes

University of Michigan, Master of Applied Data Science capstone research project.

## Overview

Does regional physician-group quality, measured by Medicare's Merit-based Incentive Payment System
(MIPS), relate to county-level Medicare outcomes such as hospital readmissions once county
characteristics are accounted for? This project builds a county panel from public CMS data and tests
the question with unsupervised and supervised models.

**Unsupervised.** County MIPS profiles are high-dimensional (~41 components for 90% variance) and
do not form sharp clusters (best silhouette ~0.10 at k=2). PC1 is mostly preventive care; cluster
differences show up more in utilization and cost than in acute outcomes like readmissions. Details
in [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb).

**Supervised.** At most a small, borderline association with readmissions after demographics
(~+0.017 R²) that is essentially absorbed by the county's own prior-year outcomes: one stable
county trait tracking another, and a lower bound given exposure misattribution. Details in
[`04_supervised_learning`](notebooks/04_supervised_learning.ipynb); figures in
[`reports/figures/`](reports/figures).

## Notebooks

1. [`01_loading_data`](notebooks/01_loading_data.ipynb): load and explore the raw CMS files
2. [`02_zip_county_crosswalk`](notebooks/02_zip_county_crosswalk.ipynb): map physician groups to counties; documents how the analytic table is built (later notebooks load the pinned artifact, not a fresh build)
3. [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb): PCA and clustering on county MIPS profiles
4. [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb): does MIPS predict county outcomes beyond demographics?
5. [`05_supervised_learning_extensions`](notebooks/05_supervised_learning_extensions.ipynb): population weighting and PCA robustness checks

## Setup

Requires Python 3.11 or newer. The committed notebook outputs were produced on Python 3.12.11 with the
exact versions in `requirements.txt`; the full pipeline was last run end to end on 2026-07-28.

```
python -m pip install -r requirements.txt
```

Run the notebooks in numbered order, **with `notebooks/` as the working directory** (every path in them
is relative, like `../data/raw`). Notebook 02 writes the county-by-measure table and notebook 03 writes
the cluster labels, both of which notebook 04 reads, so the order matters.

Inputs live in two folders:
- **Raw source files** go in `data/raw/` (see the Data section below).
- **Team-built artifacts** go in `data/processed/`: `analytic_measure.csv.gz` (the county-by-measure
  table read by notebooks 03 and 04) and `county_clusters.csv`. Both are produced by the pipeline:
  notebook 02 writes `analytic_measure.csv.gz` and notebook 03 writes `county_clusters.csv`, so
  running the notebooks in order builds them from the raw files. A pre-built copy of each is also on
  the team's shared Drive (ask a maintainer) if you want to skip straight to the modeling notebooks.
  Verify either against [`data/manifest.yaml`](data/manifest.yaml); for `analytic_measure.csv.gz`
  check `content_sha256`, not the file hash, since gzip framing and line endings differ by platform.

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

Notebook 04 draws two map layers. County boundaries (county FIPS GeoJSON) download automatically on
first run and cache in `data/raw/`. State boundaries ship with the repo as
[`data/raw/us-states.geojson`](data/raw/us-states.geojson), since the file is small, static, and the
map cannot be drawn without it; it is listed under `reference_assets` in the manifest.

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
