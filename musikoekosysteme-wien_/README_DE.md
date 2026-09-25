# Musikalische Ökosysteme in Wien: Vorstudie 2026

Dieses Repository dokumentiert den Datensatz, die Analyseschritte und die Visualisierungen der Vorstudie zur Verteilung öffentlicher Mittel für Kultur und Veranstaltungsaktivitäten im Bereich der experimentellen, improvisierten und elektronischen Musik in Wien im Zeitraum von 2022 bis 2026. Die Vorstudie wurde im Rahmen eines Forschungsstipendiums des Kultursekretariats der Stadt Wien (MA 7) durchgeführt. Die Forschungsarbeit fand zwischen April und Juni 2026 statt.


Der vollständige Bericht mit der Interpretation der Ergebnisse liegt als PDF in diesem Repository vor.

## Struktur

```
musikoekosysteme_wien/
├── daten/          Quell-CSVs und Bezirksgrenzen (siehe unten)
├── geo/            BEZIRKSGRENZEOGD.json, Bezirksgrenzen Wien
├── outputs/
│   ├── karten/      Karte 1–6, als PNG und HTML
│   ├── abbildungen/ Abbildung 1–8, als PNG (HTML für Abbildung 1 fehlt, siehe unten)
│   └── tabellen/    Tabelle 1–4, als CSV
├── musikoekosysteme-wien_scripts.ipynb   Notebook zur Verifikation der zentralen Kennzahlen
├── Bericht_final.pdf
├── README.md (diese Datei)
└── README_EN.md
```

## Daten (`daten/`)

| Datei | Inhalt |
|---|---|
| `vereine.csv` | Förderentscheidungen (MA 7, BMKöS, BMWKMS) pro Verein, Jahr und Förderlinie |
| `foerderungen_bezirkskultur.csv` | Bezirkskulturförderung, dezentral von den 23 Wiener Bezirken vergeben |
| `dataset_key.csv` | Manuell erhobener Veranstaltungsdatensatz (384 Einträge), mit Verein-Schlüssel zur Verknüpfung mit `vereine.csv` |
| `klingt.org_v2.csv` | Aus klingt.org extrahierter Veranstaltungskorpus (1.449 Einträge, 2022–2026) |
| `kombinierter_korpus.csv` | Deduplizierte Zusammenführung von `dataset_key.csv` und `klingt.org_v2.csv` (1.734 eindeutige Veranstaltungen) |
| `venues.csv` | Spielstätten mit Adresse, Bezirk und Klassifizierung |
| `vereine_empfehlungen.csv` | Empfehlungen des Musikbeirats 2025–2026, zum Abgleich mit bestätigten Beschlüssen in `vereine.csv` |

Die Quelldaten wurden über drei Monate hinweg manuell und halbmanuell recherchiert: Abgleich mit dem Transparenzportal IFG, den Förderberichten der Stadt Wien (Magistratsabteilung 5), dem Kunst-, Kultur- und Wissenschaftsbericht der Stadt Wien sowie den Kunst- und Kulturberichten des Bundes. Die Rekonstruktion dieser Quelldaten von Grund auf ist nicht Teil dieses Repositories; dieses README setzt voraus, dass sie bereits in `daten/` vorliegen.

## Methodik in Kürze

Die vollständige methodische Dokumentation befindet sich im Bericht, in den Abschnitten 2.1 bis 2.8 sowie 5.5. Zentrale Punkte:

- **Zuordnung nach Vereinssitz, nicht nach Aktivitätsort**: Die Förderung wird dem rechtlichen Sitz (Bezirk) des empfangenden Vereins zugeordnet, da öffentliche Quellen keine venue-genaue Zuordnung ermöglichen. Diese Diskrepanz zwischen Sitzbezirk und tatsächlichem Aktivitätsgebiet ist selbst ein zentraler Befund der Studie (Abschnitt 5.3), keine zu bereinigende Einschränkung.
- **Disziplinäre Zuordnung** (welche Förderzeilen als musikbezogen gelten) folgt einer dreistufigen Regel (Regel A, B, C), die in Abschnitt 2.2.1 dokumentiert ist.
- **Deduplizierung**: Bei mehreren Quellen, die denselben Beschluss dokumentieren, hat der Förderbericht Vorrang vor dem Transparenzportal IFG sowie dem Kunst-, Kultur- und Wissenschaftsbericht (KKWB).

## Karten und Diagramme

Alle Visualisierungen wurden mit Plotly (Python) erstellt, abweichend von der ursprünglich geplanten QGIS-Lösung, um Datenverarbeitung und Kartenerstellung in einem einzigen reproduzierbaren Workflow zu vereinen.

**Karten** (`outputs/karten/`), alle auf Basis von `BEZIRKSGRENZEOGD.json`:
- Karte 1: Musikalische Aktivität nach Bezirk (Veranstaltungsort)
- Karte 2: MA 7-Förderung nach Bezirk des Vereinssitzes
- Karte 3: Diskrepanz zwischen Aktivitäts-Rang und Förderungs-Rang je Bezirk (nicht als direktes Verhältnis, da dieses bei Bezirken mit sehr wenigen Veranstaltungen instabil wird und einzelne Ausreißer überbetont)
- Karte 4: Bezirkskulturförderung nach Bezirk
- Karte 5: Gesamtförderung aller Quellen nach Bezirk, logarithmische Farbskala (aufgrund der großen Spannweite der Werte)
- Karte 6: Dichte der Spielstätten nach Bezirk

**Abbildungen** (`outputs/abbildungen/`):
- Abbildung 1: Förderung nach Quelle und Jahr (HTML-Version nicht mehr auffindbar, nur PNG vorhanden)
- Abbildung 2: Historische MA 7-Reihe
- Abbildung 3: Verteilung des Korpus nach Programmkategorie
- Abbildung 4: Jährliches Wachstum des Veranstaltungskorpus (Rückgang 2026 spiegelt den unvollständigen Erhebungszeitraum wider, keinen realen Aktivitätsrückgang)
- Abbildung 5: Veranstaltungen pro Monat, Zeitreihe
- Abbildung 6: Top 25 Vereine, Förderung im Vergleich zur Anzahl dokumentierter Veranstaltungen
- Abbildung 7: Bezirk x Verein, Heatmap
- Abbildung 8: Verteilung der Event-Typen nach Bezirk

## Notebook zur Verifikation (`musikoekosysteme-wien_scripts.ipynb`)

Prüft die im Bericht zitierten Kernzahlen direkt gegen `daten/`: die Gesamtsumme 2023, die Förderreihen nach Quelle und Jahr, die Bezirksverteilung, die Konzentration der drei größten Bezirke und die Anzahl eindeutiger Programme mit ihrer Kontinuität. Enthält außerdem eine Liste bekannter Stellen, an denen die Rohdaten menschliches Urteil statt automatischer Verarbeitung erfordern (siehe letzter Abschnitt des Notebooks).

Vor jeder neuen Sitzung zuerst den Abschnitt „Setup" ausführen; das Notebook geht davon aus, dass es im Wurzelverzeichnis dieses Repositories ausgeführt wird.

## Installation

```
pip install -r requirements.txt
```

## Zitation

Der Datensatz ist zusätzlich mit DOI auf Zenodo archiviert: https://doi.org/10.5281/zenodo.22962935
