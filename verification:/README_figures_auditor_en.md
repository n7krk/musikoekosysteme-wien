README - auditor_cifras.py
=============================
last updated: 2026-09-01

purpose
----------
end-to-end check: recalculates from the source csv files the figures
that are cited in prose in the report, and flags whether the text is out
of sync with the data. this is not a data-cleaning tool, it is a quality
control step, meant to be run right before delivering a version of the
report, not during day-to-day data work.

it does not trust the report. it computes everything from scratch and
compares.

files needed in the same folder
------------------------------------
- vereine.csv
- v_bezirkskultur.csv (149 rows, 419,034.59 EUR total, the version
  already unified, including Floating Sound Gallery Vienna and SUENA)
- dataset.csv
- klingt_org_v2.csv (the one rebuilt in pipeline_klingt/, NOT the old
  klingt_org.csv)
- vereine_empfehlungen.csv

how to run it
----------------
in Jupyter, cell by cell or all at once. each block prints the
calculated value vs. the value cited in the report. any line marked
"*** DISCREPANCY ***" is a figure in the text that no longer matches the
current data, and needs review before publishing.

what this version checks (2026-09-01)
------------------------------------------
1. total rows in vereine.csv (661) and countable rows without Ausnahme (597)
2. historical MA7 series 2022-2026
3. BMKöS 2022-2026
4. BMWKmS 2025-2026
5. unified Bezirkskultur, total and by year (149 rows, 419,034.59 EUR)
6. Wien Modern 2023 (amount and % of that year's MA7, 40.97%)
7. peak year (2023) and combined total by year
8. klingt.org / dataset.csv corpus (overlap 84, unmatched 1,365, combined
   1,749) -- see the warning inside the script itself, this figure is a
   floor, not a closed number

what this version does NOT check yet (trimmed from the previous version)
--------------------------------------------------------------------------
the previous version of this script also audited Tabelle 4 (programs
such as Der Blöde Dritte Mittwoch, PARKEN, etc.) and the Empfehlungen vs.
Beschlüsse table. these were removed from this version because:
  - Tabelle 4 has a known, unfixed bug (the old function only summed
    MA7, ignoring BMKöS/BMWKmS -- see the "FIX del bug MA7-only" comment
    in vorstudie_scripts.py)
  - Empfehlungen vs. Beschlüsse was not re-verified this session

if you need to audit those two sections, recalculate them first with
vorstudie_scripts.py (functions tabelle4_programm_foerderung_jahr and
tabelle5_musikbeirat_empfehlungen) before adding them back here with
trustworthy figures.

relationship to pipeline_klingt/
-------------------------------------
block 8 of this script depends on klingt_org_v2.csv, which is generated
in the separate pipeline_klingt/ folder. run that folder first if
klingt_org_v2.csv does not exist yet or is out of date.
