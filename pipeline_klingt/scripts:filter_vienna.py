"""
filter_vienna.py
cruza klingt_events_clean.csv con venues.csv
guarda solo los eventos que ocurren en venues vieneses conocidos
"""

import csv

venues_file = "venues.csv"
events_file = "klingt_events_clean.csv"
output_file = "klingt_events_vienna.csv"

known_venues = set()
with open(venues_file, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    for i, row in enumerate(reader):
        if i == 0:
            continue
        if not row or not row[0].strip():
            continue
        venue = row[0].strip().lower()
        if venue and venue != "venue":
            known_venues.add(venue)

print(f"venues conocidos: {len(known_venues)}")

matched = []
unmatched_venues = set()

with open(events_file, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        venue_raw = row["venue"].strip().lower()
        found = False
        for known in known_venues:
            if known in venue_raw or venue_raw in known:
                found = True
                break
        if found:
            matched.append(row)
        else:
            unmatched_venues.add(row["venue"].strip())

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["datum", "event_name", "venue"], delimiter=";")
    writer.writeheader()
    writer.writerows(matched)

print(f"eventos en venues conocidos: {len(matched)}")
print(f"guardado en: {output_file}")
print(f"\nvenues NO reconocidos (primeros 30):")
for v in sorted(unmatched_venues)[:30]:
    print(f"  - {v}")
