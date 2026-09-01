"""
deduplicate.py
elimina duplicados del dataset de klingt.org
un evento es duplicado si tiene el mismo datum + event_name + venue
"""

import csv

input_file = "klingt_events_raw.csv"
output_file = "klingt_events_clean.csv"

seen = set()
unique = []
duplicates = 0

with open(input_file, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        key = (row["datum"], row["event_name"], row["venue"])
        if key not in seen:
            seen.add(key)
            unique.append(row)
        else:
            duplicates += 1

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["datum", "event_name", "venue"], delimiter=";")
    writer.writeheader()
    writer.writerows(unique)

print(f"total original: {len(unique) + duplicates}")
print(f"duplicados eliminados: {duplicates}")
print(f"eventos unicos: {len(unique)}")
print(f"guardado en: {output_file}")
