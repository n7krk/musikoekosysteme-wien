"""
FIGURES AUDITOR - Musikalische Ökosysteme in Wien
Independent script to verify, from scratch, every figure cited in the report.

How to use it:
1. Put in the same folder: vereine.csv, v_bezirkskultur.csv, dataset.csv,
   klingt_org_v2.csv, vereine_empfehlungen.csv
2. Run in Jupyter, cell by cell or all at once
3. Each block prints the CALCULATED value and the value CITED IN THE REPORT
   If they don't match, it prints DISCREPANCY

This script does not assume the report is correct. It only calculates
from the sources.

updated: 2026-09-01, with the figures verified today against
informe_31ago_4.docx and vorstudie_scripts.py. blocks 5 and 8 carry
warnings because their cited figure depends on decisions that were not
fully closed today (unified Bezirkskultur, klingt corpus).
"""

import pandas as pd

pd.set_option('display.float_format', lambda x: f'{x:,.0f}')

def check(label, calculado, citado):
    calculado = round(calculado, 2)
    citado = round(citado, 2)
    status = "OK" if calculado == citado else "*** DISCREPANCY ***"
    print(f"{label}")
    print(f"  calculated: {calculado:,.0f}  |  cited in report: {citado:,.0f}  |  {status}")
    print()


# =========================================================
# DATA LOADING
# =========================================================
v = pd.read_csv('vereine.csv', sep='\t')
v['Betrag_EUR'] = pd.to_numeric(v['Betrag_EUR'], errors='coerce')
v['Bezirk'] = v['Bezirk'].astype(str).str.strip()

vb = pd.read_csv('v_bezirkskultur.csv', sep='\t')
vb['Betrag_EUR'] = pd.to_numeric(vb['Betrag_EUR'], errors='coerce')

es_ausnahme = v['Fördergegenstand — Anmerkungen'].str.contains('— Ausnahme', regex=False, na=False)
v_zaehlbar = v[~es_ausnahme].copy()

print("="*60)
print("1. GENERAL CORPUS (2.2, 3.1)")
print("="*60)

check("Total entries in vereine.csv", len(v), 661)
check("Countable entries (without Ausnahme)", len(v_zaehlbar), 597)

ma7 = v_zaehlbar[v_zaehlbar['Foerderung_ref'] == 'MA7']

print("="*60)
print("2. HISTORICAL MA7 SERIES (3.1 / Tabelle 1 / Abbildung 2)")
print("="*60)

# values confirmed today (09/01) against informe_31ago_4.docx Tabelle 1
# and against tabelle1_historische_ma7_reihe() from vorstudie_scripts.py
serie_citada = {2022: 2326800, 2023: 3148500, 2024: 2846000, 2025: 2890700, 2026: 2978350}

for anio, citado in serie_citada.items():
    calculado = ma7[ma7['Jahr'] == anio]['Betrag_EUR'].sum()
    check(f"MA7 {anio}", calculado, citado)

print("="*60)
print("3. BMKoS (3.1)")
print("="*60)

bmkos = v_zaehlbar[v_zaehlbar['Foerderung_ref'] == 'BMKöS']
# confirmed today via tabelle_foerdersummen_jahr_quelle()
bmkos_citado = {2022: 1291430, 2023: 1538500, 2024: 1668950, 2025: 1271800, 2026: 504500}
for anio, citado in bmkos_citado.items():
    calculado = bmkos[bmkos['Jahr'] == anio]['Betrag_EUR'].sum()
    check(f"BMKöS {anio}", calculado, citado)

print("="*60)
print("4. BMWKMS (3.1)")
print("="*60)

bmwkms = v_zaehlbar[v_zaehlbar['Foerderung_ref'].str.upper() == 'BMWKMS']
# confirmed today via tabelle_foerdersummen_jahr_quelle()
bmwkms_citado = {2025: 104000, 2026: 194000}
for anio, citado in bmwkms_citado.items():
    calculado = bmwkms[bmwkms['Jahr'] == anio]['Betrag_EUR'].sum()
    check(f"BMWKMS {anio}", calculado, citado)

print("="*60)
print("5. BEZIRKSKULTUR (3.1) - unified v_bezirkskultur.csv")
print("="*60)
print("WARNING: today (09/01) it was confirmed that 419,034.59 is the")
print("already-unified total of the 149 rows in v_bezirkskultur.csv,")
print("WITHOUT excluding Floating Sound Gallery Vienna or SUENA (both")
print("cases already resolved). If your version of v_bezirkskultur.csv")
print("differs, these numbers won't match - check before assuming an error.")
print()

check("v_bezirkskultur.csv - row count", len(vb), 149)
check("v_bezirkskultur.csv - total EUR", vb['Betrag_EUR'].sum(), 419034.59)
check("Bezirkskultur 2022", vb[vb['Jahr']==2022]['Betrag_EUR'].sum(), 84984.59)
check("Bezirkskultur 2023", vb[vb['Jahr']==2023]['Betrag_EUR'].sum(), 84600.00)
check("Bezirkskultur 2024", vb[vb['Jahr']==2024]['Betrag_EUR'].sum(), 100050.00)
check("Bezirkskultur 2025", vb[vb['Jahr']==2025]['Betrag_EUR'].sum(), 107300.00)
check("Bezirkskultur 2026", vb[vb['Jahr']==2026]['Betrag_EUR'].sum(), 42100.00)

print("="*60)
print("6. WIEN MODERN 2023 (3.1)")
print("="*60)

wm2023 = v_zaehlbar[(v_zaehlbar['Verein'].str.contains('Wien Modern', case=False, na=False)) &
                     (v_zaehlbar['Jahr'] == 2023) & (v_zaehlbar['Foerderung_ref'] == 'MA7')]
check("Wien Modern MA7 2023", wm2023['Betrag_EUR'].sum(), 1290000)

ma7_2023_total = ma7[ma7['Jahr'] == 2023]['Betrag_EUR'].sum()
pct = wm2023['Betrag_EUR'].sum() / ma7_2023_total * 100 if ma7_2023_total else 0
print(f"Wien Modern as % of MA7 2023: {pct:.2f}%  |  cited in report: 40.97%")
print()

print("="*60)
print("7. PEAK YEAR AND COMBINED TOTAL (context/section 1, 3.1)")
print("="*60)
print("confirmed today: 2023 is the peak year, not 2024.")

bezirkskultur_por_anio = {2022: 84984.59, 2023: 84600.00, 2024: 100050.00, 2025: 107300.00, 2026: 42100.00}
for anio in [2022, 2023, 2024, 2025, 2026]:
    ma7_a = ma7[ma7['Jahr']==anio]['Betrag_EUR'].sum()
    bmkos_a = bmkos[bmkos['Jahr']==anio]['Betrag_EUR'].sum()
    bmwkms_a = bmwkms[bmwkms['Jahr']==anio]['Betrag_EUR'].sum()
    bk_a = bezirkskultur_por_anio.get(anio, 0)
    total = ma7_a + bmkos_a + bmwkms_a + bk_a
    print(f"  {anio}: {total:,.2f} EUR")
check("Total 2023 (peak year)", ma7[ma7['Jahr']==2023]['Betrag_EUR'].sum() +
      bmkos[bmkos['Jahr']==2023]['Betrag_EUR'].sum() +
      bmwkms[bmwkms['Jahr']==2023]['Betrag_EUR'].sum() +
      bezirkskultur_por_anio[2023], 4771600)

print("="*60)
print("8. EVENT CORPUS klingt.org / dataset.csv (2.1)")
print("="*60)
print("IMPORTANT WARNING: the klingt.org pipeline was rebuilt from")
print("scratch today (09/01). see the separate pipeline_klingt/ folder")
print("and its README before trusting these numbers. they are a FLOOR,")
print("not a closed figure (~1,261 events with a venue remain unclassified).")
print()

try:
    klingt_v2 = pd.read_csv('klingt_org_v2.csv', sep='\t')
    ds = pd.read_csv('dataset.csv', sep='\t')

    klingt_v2['_d'] = pd.to_datetime(klingt_v2['Datum'], errors='coerce').dt.date
    ds['_d'] = pd.to_datetime(ds['Datum'], errors='coerce').dt.date
    klingt_v2['_v'] = klingt_v2['Venue'].astype(str).str.strip().str.lower()
    ds['_v'] = ds['Venue'].astype(str).str.strip().str.lower()
    klingt_v2['_k'] = klingt_v2['_d'].astype(str) + '|' + klingt_v2['_v']
    ds['_k'] = ds['_d'].astype(str) + '|' + ds['_v']

    overlap = klingt_v2['_k'].isin(ds['_k']).sum()
    unmatched = len(klingt_v2) - overlap
    combined = len(ds) + unmatched

    check("overlap (Date+Venue in both sources)", overlap, 84)
    check("klingt unmatched to dataset", unmatched, 1365)
    check("combined corpus", combined, 1749)
except FileNotFoundError:
    print("WARNING: klingt_org_v2.csv not found - run first")
    print("pipeline_klingt/rebuild_klingt_pipeline_v2.py")

print("="*60)
print("END OF AUDIT. Review any line marked *** DISCREPANCY ***")
print("="*60)
