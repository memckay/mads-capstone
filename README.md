# County-Level MIPS Quality Scores: Coverage Limits and Association with Medicare Outcomes

Does county-aggregated physician-group quality, measured by Medicare's Merit-based Incentive Payment
System (MIPS), relate to county-level Medicare outcomes once county characteristics are accounted for?
The primary outcome is the county 30-day all-cause hospital readmission rate for 2023; standardized
Medicare cost per beneficiary is carried as a secondary outcome. MIPS is published for a single
performance year, so our analysis is cross-sectional rather than a forward looking panel.

---

## Findings

County-level MIPS aggregates appear too thin to carry a reliable regional quality signal. Two-thirds
of county-measure cells are based on two or fewer reporting practices, and a county's reporting
pattern alone recovers most of what the models gain from the scores themselves.

![Cross-validated R² for four models, each fitted with county controls only and again with controls plus MIPS. Gradient boosting gains the most at +0.020, Elastic Net +0.017, random forest +0.013, and linear OLS is negative at -0.009. Every model leaves most county readmission variance unexplained.](reports/figures/sl_delta_r2.png)

Four models were fitted with and without the MIPS measures. The gains are small throughout, and we
quote the Elastic Net at **+0.017 R²** because its gain is the most consistent, positive in all five
held-out folds, rather than the largest. Gradient boosting gains more (+0.020) but in only two of five
folds, and linear regression gets worse.

Adding the county's own prior-year readmission rate largely erases the MIPS contribution, suggesting
that the signal overlaps more with persistent county outcome patterns than with contemporaneous MIPS
performance. Of the 16 measures reported widely enough to test, 3 survive multiple-testing
correction, all preventive care: diabetes HbA1c poor control, cervical cancer screening, and breast
cancer screening. For each of these, better county-level performance is associated with fewer
readmissions, though the associations remain small.

Clustering the same county profiles without any outcome data reaches the same place from the other
direction. The profiles are high-dimensional, requiring roughly 41 components to reach 90% of the
variance, and they form no sharp groups, with the best silhouette around 0.10 at k = 2. A continuum
rather than distinct archetypes is consistent with a weak or noisy county-level signal.

These findings apply to county-level MIPS aggregates, not to MIPS performance at the individual
practice level where the program operates. They should not be read as evidence that MIPS lacks value
for practices; the question here is whether the signal survives aggregation to counties. The results
are associations, not causal estimates.

Details in [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb) and
[`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb); figures in
[`reports/figures/`](reports/figures).

---

## Notebooks

Run in numbered order. Notebook 02 writes the county-by-measure table and notebook 03 writes the
cluster labels, both of which notebook 04 reads.

1. [`01_loading_data`](notebooks/01_loading_data.ipynb): load and profile the raw CMS files
2. [`02_zip_county_crosswalk`](notebooks/02_zip_county_crosswalk.ipynb): map physician groups to counties and write `analytic_measure.csv.gz`
3. [`03_unsupervised_learning`](notebooks/03_unsupervised_learning.ipynb): PCA and clustering on county MIPS profiles
4. [`04_supervised_learning`](notebooks/04_supervised_learning.ipynb): test whether MIPS adds predictive value beyond county controls under state-grouped cross-validation
5. [`05_supervised_learning_extensions`](notebooks/05_supervised_learning_extensions.ipynb): robustness checks on population weighting, PCA features, and spatial standard errors

---

## Setup

Python 3.11+. The committed outputs were produced on 3.12.11 with the exact versions pinned in
`requirements.txt`.

```bash
python -m pip install -r requirements.txt
cd notebooks && jupyter lab
```

**Run with `notebooks/` as the working directory**; every path in the notebooks is relative, like
`../data/raw`.

Put the raw source files in `data/raw/` (see [Data](#data)). The pipeline builds everything else, so
`data/processed/` starts empty. Prebuilt copies of `analytic_measure.csv.gz` and
`county_clusters.csv` are on the team's shared Drive if you want to skip to the modeling notebooks.
Verify them against [`data/manifest.yaml`](data/manifest.yaml), using `content_sha256` for the gzip
file since its file hash differs by platform.

A full run takes roughly 10 to 20 minutes, mostly notebook 02, which reads an 840 MB provider file,
and notebook 04, which runs four model families under grouped cross-validation.

---

## Data

Source data is not committed. [`data/manifest.yaml`](data/manifest.yaml) pins each dataset's version
and `sha256`, and notebook 01 checks every raw file against it before loading anything, so a stale or
newer snapshot stops the run instead of quietly changing the results. CMS and HUD refresh these files
in place, so match by hash if a link breaks. The HUD crosswalk has no stable direct URL; download it
from the landing page.

| Dataset | Role | Source |
|---|---|---|
| Group MIPS performance | predictor | [CMS `0ba7-2cb0`](https://data.cms.gov/provider-data/dataset/0ba7-2cb0) |
| Doctors & Clinicians national file | group to ZIP and specialty | [CMS `mj5m-pzi6`](https://data.cms.gov/provider-data/dataset/mj5m-pzi6) |
| Medicare Geographic Variation | county outcomes and controls | [CMS Summary Statistics](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-geographic-comparisons/medicare-geographic-variation-by-national-state-county) |
| ZIP-to-county crosswalk | geography | [HUD USPS ZIP Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html) |

County and state map boundaries are included in `data/raw/` and pinned in the manifest, so the map
cells can run without a first-run download.

---

## Repository layout

```text
data/        pinned manifest and small static reference geometry; bulk data is gitignored
notebooks/   analysis pipeline
reports/     figures and report source
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
The source data is U.S. government data from CMS and HUD, not committed here, and each source's own
terms apply.