# MADS Capstone: Healthcare Heroes

Does regional physician-group quality, measured by Medicare's Merit-based Incentive Payment System
(MIPS), relate to county-level Medicare outcomes such as hospital readmissions once county
characteristics are accounted for? University of Michigan, SIADS 699.

---

## Findings

**Supervised.** County-level MIPS aggregates are too thin to carry a regional quality signal. Two
thirds of county-measure cells rest on two or fewer reporting practices, and reporting pattern alone
recovers most of the tree model's lift. The association that survives is small (~+0.017 R² after
demographics) and is absorbed by the county's own prior-year outcomes, which is what a mostly-noise
exposure predicts. Of the 16 measures clearing a 70% coverage floor, 3 hold up after correction, all
preventive care. This is a claim about the county aggregate, not about MIPS at the practice level.
See [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb) and
[`reports/figures/`](reports/figures).

![Cross-validated R2 for four models, each fitted with county controls only and again with controls plus MIPS. Gradient boosting gains the most at +0.020, Elastic Net +0.017, random forest +0.013, and linear OLS is negative at -0.009. Every model leaves most county readmission variance unexplained.](reports/figures/sl_delta_r2.png)

**Unsupervised.** County MIPS profiles are high-dimensional (~41 components for 90% variance) and do
not form sharp clusters (best silhouette ~0.10 at k=2). PC1 is mostly preventive care; cluster
differences show up in utilization and cost more than in acute outcomes.
See [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb).

---

## Notebooks

Run in numbered order. 02 writes the county-by-measure table and 03 writes the cluster labels, both of
which 04 reads.

1. [`01_loading_data`](notebooks/01_loading_data.ipynb): load and profile the raw CMS files
2. [`02_zip_county_crosswalk`](notebooks/02_zip_county_crosswalk.ipynb): map physician groups to counties, write `analytic_measure.csv.gz`
3. [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb): PCA and clustering on county MIPS profiles
4. [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb): does MIPS predict county outcomes beyond demographics?
5. [`05_supervised_learning_extensions`](notebooks/05_supervised_learning_extensions.ipynb): robustness checks on population weighting, PCA features, and spatial standard errors

---

## Setup

Python 3.11+. The committed outputs were produced on 3.12.11 with the exact versions pinned in
`requirements.txt`.

```
python -m pip install -r requirements.txt
cd notebooks && jupyter lab
```

**Run with `notebooks/` as the working directory**; every path in them is relative, like `../data/raw`.

Put the raw source files in `data/raw/` (see [Data](#data)). The pipeline builds everything else, so
`data/processed/` starts empty. Pre-built copies of `analytic_measure.csv.gz` and `county_clusters.csv`
are on the team's shared Drive if you want to skip to the modeling notebooks; verify them against
[`data/manifest.yaml`](data/manifest.yaml), using `content_sha256` for the gzip file since its file
hash differs by platform.

A full run takes roughly 10 to 20 minutes, mostly notebook 02 (reads an 840 MB provider file) and
notebook 04 (four model families under grouped cross-validation).

---

## Data

Source data is not committed. [`data/manifest.yaml`](data/manifest.yaml) pins each dataset's version
and `sha256`. CMS and HUD rotate download URLs, so match files by hash if a link breaks. The HUD
crosswalk has no stable direct URL; download it from the landing page.

| Dataset | Role | Source |
|---|---|---|
| Group MIPS performance | predictor | [CMS `0ba7-2cb0`](https://data.cms.gov/provider-data/dataset/0ba7-2cb0) |
| Doctors & Clinicians national file | group to ZIP and specialty | [CMS `mj5m-pzi6`](https://data.cms.gov/provider-data/dataset/mj5m-pzi6) |
| Medicare Geographic Variation | county outcomes and controls | [CMS Summary Statistics](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-geographic-comparisons/medicare-geographic-variation-by-national-state-county) |
| ZIP-to-county crosswalk | geography | [HUD USPS ZIP Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html) |

County map boundaries download on first run and cache in `data/raw/`. State boundaries ship with the
repo as [`data/raw/us-states.geojson`](data/raw/us-states.geojson).

---

## Repository layout

```
data/         pinned manifest and small static reference geometry (bulk data is gitignored)
notebooks/    the analysis pipeline
reports/      figures and the report source
```

---

## Authors

Transaint Gau, Maria Paz, Zachary Sletten, and Justin Tseng.

---

## Third-party assets and attributions

| Asset | Source | License |
|---|---|---|
| County boundaries (`geojson-counties-fips.json`) | [plotly/datasets](https://github.com/plotly/datasets) | MIT; boundaries US Census derived, public domain |
| State boundaries (`data/raw/us-states.geojson`) | Leaflet choropleth example | boundaries US Census derived, public domain |

---

## License

Code released under the [MIT License](LICENSE); coursework for SIADS 699, shared for academic review.
The source data is U.S. government data (CMS and HUD), not committed here, and each source's own terms
apply.
