# Analysis scripts — Musikalische Ökosysteme in Wien

These scripts are the second stage of the pipeline, after data collection
and cleaning (deduplicate.py, filter_vienna.py, klingt_scraper.py).
All of them assume that vereine.csv and v_bezirkskultur.csv are in the
same folder.

## Order of use

1. **01_bezirkskultur_bezirk_zuordnung.py**
   Cross-references v_bezirkskultur.csv against vereine.csv to assign a
   Bezirk to each Verein, without modifying any file on disk. The match
   is done by name, using the Bezirk history already documented in
   vereine.csv. Vereine with a contradictory Bezirk history (or no name
   match) are left unassigned and listed explicitly at the end.

2. **02_summe_nach_quelle_und_jahr.py**
   Uses script 01. Sums MA7 + BMKöS + BMWKmS + Bezirkskultur per year.
   Provides the figure for the paragraph in 1. Kontext ("das historische
   Maximum...").

3. **03_tabelle2_ma7_nach_bezirk.py**
   Generates Tabelle 2 (MA7 by legal domicile Bezirk, 2022–2026). MA7
   only, does not include BMKöS or Bezirkskultur. Separates the 20
   numbered Bezirke (used for Karte 2/3) from Klagenfurt / nicht
   dokumentiert (outside the map grid).

4. **04_allgemeine_verifikation.py**
   Calculates all series by institutional source from scratch, and flags
   rows with identical Verein/Jahr/Betrag/Foerderung_ref/Typ as possible
   duplicates to review manually (it does not automatically assume these
   are errors — they may be two distinct projects with the same amount).

## Important note

None of these scripts contain hand-written "expected" figures. They are
the source of truth: they are run, and their output is compared against
what the Bericht states at that moment — not the other way around. If
new rows are added to vereine.csv, everything simply gets run again.

## Dependencies

pandas (all scripts), geopandas + plotly + kaleido (for mapas_finales.py,
not included in this folder).
