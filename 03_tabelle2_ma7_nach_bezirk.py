"""
03_tabelle2_ma7_nach_bezirk.py

Genera Tabelle 2: MA7 Gesamtfoerderung nach Bezirk (rechtlicher Sitz), 2022-2026.
Solo Foerderung_ref == 'MA7' y Typ == 'Beschluss' (Tabelle 2 es MA7-only, no
incluye BMKoeS ni Bezirkskultur -- eso va en tablas/parrafos separados).

Uso:
    from _03_tabelle2_ma7_nach_bezirk import tabelle2_ma7_nach_bezirk
    tabla = tabelle2_ma7_nach_bezirk()
"""
import pandas as pd


def tabelle2_ma7_nach_bezirk(path_vereine='vereine.csv'):
    v = pd.read_csv(path_vereine, sep='\t')
    v['Betrag_EUR'] = pd.to_numeric(v['Betrag_EUR'], errors='coerce')
    v['Bezirk'] = v['Bezirk'].astype(str).str.strip()

    ma7 = v[(v['Foerderung_ref'] == 'MA7') & (v['Typ'] == 'Beschluss')]

    tabla = ma7.groupby('Bezirk')['Betrag_EUR'].sum().sort_values(ascending=False)

    # separar los 20 Bezirke numerados (para Karte 2/3) de Klagenfurt / nicht dokumentiert
    numerados = tabla[tabla.index.str.isdigit()].sort_index(key=lambda x: x.astype(int))
    fuera_de_wien = tabla[~tabla.index.str.isdigit()]

    resultado = pd.concat([numerados, fuera_de_wien])
    return resultado


if __name__ == '__main__':
    tabla = tabelle2_ma7_nach_bezirk()
    print(tabla)
    print()
    print('Gesamt:', tabla.sum())
