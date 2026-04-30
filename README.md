Musikalische Ökosysteme in Wien — Vorstudie 2026

Exploratory study on the spatial distribution of music events and public funding 
structures within Vienna's independent experimental and electronic music scene.
Funded by MA7 (Stadt Wien, €3.000). Final report due September 30, 2026.

---

Repository Structure

dataset.csv
**What:** Central registry of documented music events in Vienna's independent 
experimental and electronic scene, 2022–2026.

Contains:One row per event with: date, venue, event name, event type, 
district (Bezirk), artists, organizer, responsible Verein, funding references, 
and documentation source.

How it was built: Manual extraction from primary sources (festival websites, 
klingt.org, esel.at, schalltaucherin.com, Instagram, porgy.at) combined with 
automated scraping of klingt.org using Python/BeautifulSoup4. All methodological 
decisions documented in RESEARCH_LOG.md.

Why it exists:Enables cross-referencing of events with venues (spatial 
distribution) and funding sources (public support structures). Primary input for 
frequency analysis in pandas and spatial visualization in QGIS.

Limitations: Uneven coverage by year and organizer. Pre-September 2025 funding 
marked as [nicht verifizierbar - vor IFG] due to absence of centralized public 
data before the IFG transparency law. Recurring series (Monday Improvisers Session, 
smallforms, etc.) documented with one real entry per year — full frequency available 
in klingt_events_vienna.csv.

Separator:** semicolon (;). Multiple values within fields separated by pipe (|).

---

venues.csv
What: Catalogue of physical spaces where corpus events take place.

Contains: One row per venue with: name, venue type, address, district, 
programmatic profile, website, geographic coordinates (lat/lon), corpus 
classification, notes, and status (aktiv/geschlossen/unbekannt).

How it was built: Identified from dataset events, complemented by the 
Independent Space Index (independentspaceindex.at), klingt.org, and prior 
knowledge of the scene. Coordinates verified manually via Google Maps.

Why it exists: Base layer for QGIS — each row is a point on the map. Enables 
spatial analysis: distribution by Bezirk, concentration of funded venues, 
identification of activity zones.

Inclusion criteria: Venues included if they meet at least one of the following:
- Primary or significant programming focus on experimental, improvised, electronic, 
  or contemporary music
- Documented presence of publicly funded music events
- Active role in the independent scene regardless of formal funding status

Excluded: spaces without a fixed physical location, spaces focused exclusively on 
visual art or dance, diplomatic or academic institutions without their own scene 
programming, venues with a single documented event and no ongoing role.

Venue types (venue_typ): Club / Kulturzentrum / Studio / Konzerthaus / Offspace 
/ Kirche / Akademisch / Außenraum / Museum. Categories optimized for QGIS filtering, 
not ethnographic description.

Separator: comma (,).

---

klingt_events_vienna.csv
What: Full extraction of Viennese events from klingt.org, 2022–2026.

Contains: One row per event with: date, event name, venue. No artist, 
funding, or organizer data.

How it was built: Automated scraping via Python 3.12, requests, and 
BeautifulSoup4 using POST form submission. Deduplication applied before filtering. 
Vienna filtering by cross-reference with venues.csv. Case normalization applied 
to venue names.

Why it exists: Complements dataset.csv for frequency analysis — 997 events 
with systematic coverage vs. 285 events with full detail. Enables identification 
of temporal and venue patterns not visible in the manual dataset.

Limitations: Coverage limited to venues indexed on klingt.org. No artist or 
funding data.

Separator:** semicolon (;).

---

quellen_events.csv
What: Catalogue of sources used to document events.

Contains: One row per source with: institution, institution type, information 
type, granularity, URL, format, source type, limitations, years covered, and 
action taken.

Why it exists: Documents data traceability — what was searched, where, what 
was found, and what limitations apply. Essential for the methodology section of 
the final report.

---

quellen_foerderungen.csv
What: Catalogue of data sources on public cultural funding in Vienna.

Contains: One row per source with: institution, institution type, information 
type, granularity, URL, format, source type, limitations, years covered, and 
action taken.

Why it exists: Maps what funding data exists, where it is, and what can be 
extracted. The opacity of pre-IFG data (before September 2025) is itself a 
finding documented here — the absence of centralized sources for 2022–2024 
reflects a structural characteristic of the ecosystem, not a gap in the research.

---

Key Methodological Decisions
See RESEARCH_LOG.md for full documentation of all decisions, problems, and 
limitations encountered during data collection.

Special Field Values
- `[nicht dokumentiert]` — information exists but is not publicly available
- `[nicht öffentlich]` — deliberately not published (e.g. RSVP-only locations)
- `[manuell rekonstruierbar]` — available on Instagram but extraction 
  disproportionate to Vorstudie scope
- `[nicht verifizierbar - vor IFG]` — funding unverifiable before IFG law 
  (September 2025)

Tools
- Obsidian
- Python 3.12, requests, BeautifulSoup4 — scraping
- OpenRefine — data cleaning
- QGIS — spatial analysis (May 2026)
- pandas / matplotlib — frequency analysis and visualization (May 2026)
