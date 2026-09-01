# final step: Date+Venue match between klingt_org_v2.csv (rebuilt today,
# with updated venues.csv and applied aliases) and dataset.csv
# methodology as documented in the text: "matched by date and venue"

import pandas as pd

klingt_v2 = pd.read_csv('klingt_org_v2.csv', sep='\t')
ds = pd.read_csv('dataset.csv', sep='\t')  # the project's actual dataset.csv

print('klingt_org_v2 rows:', len(klingt_v2))
print('dataset rows:', len(ds))

klingt_v2['_date_norm'] = pd.to_datetime(klingt_v2['Datum'], errors='coerce').dt.date
ds['_date_norm'] = pd.to_datetime(ds['Datum'], errors='coerce').dt.date

klingt_v2['_venue_norm'] = klingt_v2['Venue'].astype(str).str.strip().str.lower()
ds['_venue_norm'] = ds['Venue'].astype(str).str.strip().str.lower()

klingt_v2['_key'] = klingt_v2['_date_norm'].astype(str) + '|' + klingt_v2['_venue_norm']
ds['_key'] = ds['_date_norm'].astype(str) + '|' + ds['_venue_norm']

overlap_mask = klingt_v2['_key'].isin(ds['_key'])
n_overlap = overlap_mask.sum()
n_unmatched = (~overlap_mask).sum()

print()
print('=== FINAL RESULT (replaces the 87/77/90 in the text) ===')
print('overlap (Date+Venue match in both sources):', n_overlap)
print('klingt_org_v2 unmatched to dataset:', n_unmatched)
combined = len(ds) + n_unmatched
print('combined corpus (dataset + unmatched klingt):', combined)
print()
print('to compare against the current text (informe_31ago_4.docx):')
print('  current: 77 overlap, 1,286 combined, 912 unmatched')
print(f'  new:     {n_overlap} overlap, {combined} combined, {n_unmatched} unmatched')
