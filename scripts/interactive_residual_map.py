"""Build an interactive county choropleth of model residuals.

Reads the residuals exported by notebooks/04_supervised_learning.ipynb and the
county geometry, then writes a self-contained HTML map where hovering a county
shows its name, state, and residual. Regenerate with:

    pip install plotly polars
    python scripts/interactive_residual_map.py

Output: reports/residual_map.html  (locally excluded; regenerate on demand).
"""
import json
from pathlib import Path

import plotly.express as px
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "reports" / "residual_map.html"

BLUE, MAIZE = "#00274C", "#FFCB05"

STATE_FIPS_ABBR = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO",
    "09": "CT", "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI",
    "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
    "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
    "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
    "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
    "54": "WV", "55": "WI", "56": "WY", "72": "PR",
}

# County geometry (fetched by the notebook into data/raw, gitignored)
counties = json.loads((DATA / "raw" / "geojson-counties-fips.json").read_text())
fips_name = {
    f["id"]: f"{f['properties']['NAME']} County, {STATE_FIPS_ABBR.get(f['properties']['STATE'], f['properties']['STATE'])}"
    for f in counties["features"]
}

# Residuals exported by the supervised notebook (county_fips kept as text)
resid = (
    pl.read_csv(DATA / "interim" / "residuals_2023.csv", infer_schema_length=0)
    .with_columns(
        pl.col("resid").cast(pl.Float64),
        pl.col("county_fips").map_elements(lambda c: fips_name.get(c, c), return_dtype=pl.String).alias("county"),
    )
)

lim = float(resid["resid"].abs().quantile(0.95))

fig = px.choropleth(
    resid.to_pandas(),
    geojson=counties,
    locations="county_fips",
    featureidkey="id",
    color="resid",
    color_continuous_scale=[[0.0, BLUE], [0.5, "#f7f7f7"], [1.0, MAIZE]],
    range_color=[-lim, lim],
    scope="usa",
    labels={"resid": "residual"},
    hover_name="county",
    hover_data={"county_fips": True, "resid": ":.4f"},
)
fig.update_traces(marker_line_width=0.15, marker_line_color="white")
fig.update_layout(
    title=dict(
        text="County readmission residuals (actual minus predicted)<br>"
             "<sup>blue = model over-predicts, maize = under-predicts; hover for county detail</sup>",
        x=0.5, xanchor="center", font=dict(color=BLUE, size=18),
    ),
    coloraxis_colorbar=dict(title="residual"),
    margin=dict(l=0, r=0, t=70, b=0),
)
fig.update_geos(visible=False, fitbounds="locations")

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(f"wrote {OUT}  ({OUT.stat().st_size // 1024} KB, {resid.height:,} counties)")
