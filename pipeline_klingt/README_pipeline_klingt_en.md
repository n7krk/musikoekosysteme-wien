README - pipeline_klingt/
============================
last updated: 2026-09-01

purpose
----------
rebuild the corpus of klingt.org events filtered to Vienna, cross it
against dataset.csv, and produce the overlap / combined-corpus numbers
cited in the report (section 2.1: "X events appear in both archives...
Y unique events...").

the previous number (87 overlap / 1,286 combined) had no script
explaining how it was calculated. this folder replaces that black box
with a documented, repeatable process.

files needed beyond this folder
-----------------------------------
- data/klingt_events_raw.csv   (raw scrape from klingt_scraper.py, ~77,000 rows, includes events worldwide)
- data/venues.csv              (catalog of known Vienna venues)
- data/dataset.csv             (manual corpus)

execution order
-------------------
1. rebuild_klingt_pipeline_v2.py
   reads klingt_events_raw.csv + venues.csv
   exact dedup -> separates events with no venue ("???") -> applies venue
   aliases (spelling variants of the same place) -> exact match against
   venues.csv -> exports klingt_org_v2.csv

   IMPORTANT: always check the "alias check" block printed at the end.
   if any alias says MISSING, the right-hand name in ALIAS_VENUES does
   not match venues.csv exactly, fix it before trusting the result.

2. cruce_final_klingt_dataset.py
   reads klingt_org_v2.csv + dataset.csv
   matches on Date + Venue (the method already described in the text:
   "matched by date and venue")
   prints: overlap, unmatched, combined corpus

current result (2026-09-01)
-------------------------------
overlap: 84
klingt events unmatched to dataset: 1,365
combined corpus: 1,749

these numbers replace the 87/1,286/912 (there was more than one older
version circulating with no clear source) previously in the text.

LIMITATION THAT MUST BE STATED IN THE TEXT, not optional
--------------------------------------------------------------
out of 2,710 klingt events with a non-empty venue field, only 1,449
matched a known Vienna venue in venues.csv. the remaining 1,261 are a
mix of:
  a) events genuinely outside Vienna (likely the majority)
  b) real Vienna venues not yet catalogued in venues.csv (8 were added
     today: Vronihof, Reflexionswerkstatt 35, T-Raum, Breitenseer
     Lichtspiele, MuTh, Kunsttankstelle Ottakring, Volkstheater, Xian)

(a) and (b) were not distinguished for the remaining 1,261. this means
1,749/84/1,365 is a FLOOR, not a closed number. this must be stated as
such in the report's methodological note, not presented as a final
figure.

deprecated files, do not use
---------------------------------
- rebuild_klingt_pipeline.py (without _v2): first version, no aliases, no
  updated venues.csv. produced 891-1,060 rows depending on when it was
  run. kept for historical reference only, do not run it to source
  figures for the text.

pending (not resolved today, long tail)
-------------------------------------------
review the most frequent venues still in the "1,261 unmatched" list that
haven't been catalogued yet. today only the top ~35-60 by frequency were
reviewed. the long tail (venues with 1-3 events each) can add up to
several hundred events combined and was not addressed.
