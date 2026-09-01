"""
rebuild_klingt_pipeline_v2.py
final version, using the updated venues.csv (87 rows, includes the 8 new
venues added today) and an alias dictionary for spelling variants of the
same venue.

run this in the new notebook, inside the repo folder, with these files
present: klingt_events_raw.csv, venues.csv (today's version, 87 rows)
"""

import pandas as pd

# alias: variant as it appears in klingt -> EXACT name in venues.csv
ALIAS_VENUES = {
    'kulturcafe max': 'kulturcafé max',      # confirm exact name in venues.csv
    'cafe max': 'kulturcafé max',
    'ruprechtskirche': 'st. ruprecht',
    'st. ruprecht (neue musik in)': 'st. ruprecht',
    'theater am werk / petersplatz': 'theater am werk / petersplatz',
    'chateau rouge': 'château rouge',
    'porgy&bess': 'porgy & bess jazz& music club',
    'strenge kammer / porgy & bess': 'porgy & bess jazz& music club',
    'klangtheater': 'klangtheater mdw',
    'koje': 'koje – kollektive organisation für jetztzeit-experimente',
    'modul': 'setzkasten wien',
    'im spitzer': 'odeon theater',
}
# NOTE: the right-hand values are a best estimate of how these names are
# written in your current venues.csv. before running, confirm against
# your own file (venues['Venue'].str.lower()) that these EXACT names
# exist, otherwise the alias will not match.

raw = pd.read_csv('klingt_events_raw.csv', sep=';', encoding='utf-8')
print('raw:', len(raw))

clean = raw.drop_duplicates(subset=['datum', 'event_name', 'venue']).copy()
print('clean (exact dedup):', len(clean))

venue_norm = clean['venue'].astype(str).str.strip()
sin_venue = clean[venue_norm.isin(['???', '', 'nan']) | clean['venue'].isna()]
con_venue = clean[~clean.index.isin(sin_venue.index)].copy()
print('no venue (???, empty):', len(sin_venue))

con_venue['_venue_norm'] = con_venue['venue'].astype(str).str.strip().str.lower()
# apply aliases BEFORE matching
con_venue['_venue_norm'] = con_venue['_venue_norm'].replace(ALIAS_VENUES)

venues_actual = pd.read_csv('venues.csv', sep='\t')
venues_conocidos = set(venues_actual['Venue'].astype(str).str.strip().str.lower())

matched = con_venue[con_venue['_venue_norm'].isin(venues_conocidos)]
sin_match = con_venue[~con_venue['_venue_norm'].isin(venues_conocidos)]

print('venue recognized (including aliases):', len(matched))
print('still unmatched:', len(sin_match))

# check that the aliases actually matched (if any gives 0, the right-hand
# name in ALIAS_VENUES is not exact, needs correcting)
print()
print('alias check (should be >0 for each one that has events):')
for variante, canonico in ALIAS_VENUES.items():
    n = (con_venue['venue'].astype(str).str.strip().str.lower() == variante).sum()
    matcheo = canonico in venues_conocidos
    print(f"  {variante!r} ({n} events) -> {canonico!r}: {'OK, exists in venues.csv' if matcheo else 'MISSING, check exact name'}")

klingt_org_v2 = matched[['datum', 'event_name', 'venue']].rename(
    columns={'datum': 'Datum', 'event_name': 'Event_Name', 'venue': 'Venue'}
)
klingt_org_v2.to_csv('klingt_org_v2.csv', sep='\t', index=False)
print()
print('saved: klingt_org_v2.csv,', len(klingt_org_v2), 'rows')
print('(next step, Date+Venue match against dataset.csv, comes after this)')
