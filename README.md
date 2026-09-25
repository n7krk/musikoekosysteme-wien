# Musical Ecosystems in Vienna: Preliminary study 2026

This repository documents the dataset, analysis steps, and visualizations behind a preliminary study (Vorstudie) on the distribution of public cultural funding and event activity in Vienna's experimental, improvised, electronic music ecosystem, covering 2022 to 2026. The preliminary study was carried out under a Wissenschaftsstipendium (science stipend) awarded by Stadt Wien Kultur (MA 7). The study took place between April and June 2026.

The full report with the interpretation of the findings is included in this repository as a PDF.

## Structure

```
musikoekosysteme_wien/
├── daten/          source CSVs and district boundaries (see below)
├── geo/            BEZIRKSGRENZEOGD.json, Vienna district boundaries
├── outputs/
│   ├── karten/      Karte 1-6, as PNG and HTML
│   ├── abbildungen/ Abbildung 1-8, as PNG 
│   └── tabellen/    Tabelle 1-4, as CSV
├── musikoekosysteme-wien_scripts.ipynb   notebook verifying the report's central figures
├── Bericht_final.pdf
├── README.md
└── README_EN.md (this file)
```

Folder and file names inside `daten/`, `outputs/`, and the notebook itself are kept in German to match the terminology used throughout the report (Bericht) and its footnotes; this file exists to make the repository navigable for an English-speaking reader without renaming anything the report itself refers to.

## Data (`daten/`)

| File | Content |
|---|---|
| `vereine.csv` | Funding decisions (MA 7, BMKöS, BMWKMS) by association (Verein), year and funding line |
| `foerderungen_bezirkskultur.csv` | District-level cultural funding (Bezirkskultur), administered independently by each of Vienna's 23 districts |
| `dataset_key.csv` | Manually researched event dataset (384 entries), with an association key linking to `vereine.csv` |
| `klingt_org_v2.csv` | Event corpus scraped from klingt.org (1,449 entries, 2022-2026) |
| `kombinierter_korpus.csv` | Deduplicated combination of `dataset_key.csv` and `klingt_org_v2.csv` (1,734 unique events) |
| `venues.csv` | Venues with address, district and classification |
| `vereine_empfehlungen.csv` | Music advisory board (Musikbeirat) recommendations 2025-2026, for cross-checking against confirmed decisions in `vereine.csv` |

The source data was researched manually and semi-manually over several months: cross-checked against the Transparenzportal (Austria's freedom-of-information funding database), the City of Vienna's annual funding reports (Magistratsabteilung 5), the City of Vienna's Arts, Culture and Science Report, and the federal Arts and Culture Reports. Rebuilding this source data from scratch is out of scope for this repository; this README assumes it already exists in `daten/`.

## Methodology, briefly

Full methodological documentation is in the report, sections 2.1 to 2.8 and 5.5. Key points:

- **Attribution by legal domicile (Sitzbezirk), not by activity location**: funding is attributed to the district where the receiving association is legally registered, since public sources don't allow venue-level attribution. This gap between registered domicile and actual activity area is itself a central finding of the study (section 5.3), not a limitation to be corrected away.
- **Disciplinary classification** (which funding lines count as music-related) follows a three-tier rule (Regel A, B, C), documented in section 2.2.1.
- **Deduplication**: where multiple sources document the same decision, priority is given in this order: annual funding report, then the Transparenzportal, then the general Arts, Culture and Science Report (KKWB).

## Maps and charts

All visualizations were built with Plotly (Python), a deviation from the QGIS workflow originally planned, chosen to keep data processing and map rendering in a single reproducible pipeline.

**Maps** (`outputs/karten/`), all based on `BEZIRKSGRENZEOGD.json`:
- Karte 1: musical activity by district (event venue)
- Karte 2: MA 7 funding by district of legal domicile
- Karte 3: discrepancy between activity rank and funding rank by district (rank-based rather than a direct ratio, since the ratio becomes unstable in districts with very few recorded events and overstates outliers)
- Karte 4: district-level cultural funding (Bezirkskultur) by district
- Karte 5: total funding from all sources by district, log color scale (given the wide spread of values)
- Karte 6: density of venues by district

**Figures** (`outputs/abbildungen/`):
- Abbildung 1: funding by source and year
- Abbildung 2: historical MA 7 series
- Abbildung 3: corpus distribution by program category
- Abbildung 4: yearly growth of the event corpus (the 2026 dip reflects the incomplete collection period for that year, not an actual drop in activity)
- Abbildung 5: events per month, time series
- Abbildung 6: top 25 associations, funding compared to number of documented events
- Abbildung 7: district x association heatmap
- Abbildung 8: distribution of event types by district

## Verification notebook (`musikoekosysteme-wien_scripts.ipynb`)

Checks the report's key figures directly against `daten/`: the 2023 total, the funding series by source and year, the district distribution, the concentration in the three largest districts, and the count of unique programs with their continuity. Also includes a list of known cases where the raw data needs human judgment rather than automated processing (see the notebook's last section).

Run the "Setup" section first in every new session; the notebook assumes it runs from this repository's root directory.

## Installation

```
pip install -r requirements.txt
```

## Citation

The dataset is additionally archived with a DOI on Zenodo: https://doi.org/10.5281/zenodo.22962935
