"""
02_summe_nach_quelle_und_jahr.py

Suma MA7 + BMKoeS + BMWKmS + Bezirkskultur por anio, combinando vereine.csv
(que ya trae MA7/BMKoeS/BMWKmS, mas Bezirkskultur 2025-2026 si la hubiera)
con v_bezirkskultur.csv (Bezirkskultur 2022-2024, via cruce del script 01).

Usar este numero para el parrafo de 1. Kontext ("Das Jahr 2024 stellte das
historische Maximum... X Euro aus MA7, BMKoeS und Bezirkskultur").

Solo cuenta Typ == 'Beschluss' (nunca Empfehlung).

Uso:
    from _01_bezirkskultur_bezirk_zuordnung import bezirkskultur_mit_bezirk
    from _02_summe_nach_quelle_und_jahr import summe_nach_quelle_und_jahr
    tabla = summe_nach_quelle_und_jahr()
"""
import pandas as pd

try:
    from importlib.machinery import SourceFileLoader
    _cruce = SourceFileLoader('cruce', '01_bezirkskultur_bezirk_zuordnung.py').load_module()
    bezirkskultur_mit_bezirk = _cruce.bezirkskultur_mit_bezirk
except Exception:
    # fallback si se importa como paquete normal
    from importlib import import_module
    bezirkskultur_mit_bezirk = import_module('01_bezirkskultur_bezirk_zuordnung').bezirkskultur_mit_bezirk


def summe_nach_quelle_und_jahr(path_vereine='vereine.csv', path_vbk='v_bezirkskultur.csv'):
    v = pd.read_csv(path_vereine, sep='\t')
    v['Betrag_EUR'] = pd.to_numeric(v['Betrag_EUR'], errors='coerce')
    v = v[v['Typ'] == 'Beschluss']

    vbk = bezirkskultur_mit_bezirk(path_vereine, path_vbk)
    vbk['Betrag_EUR'] = pd.to_numeric(vbk['Betrag_EUR'], errors='coerce')
    vbk['Jahr'] = pd.to_numeric(vbk['Jahr'], errors='coerce')
    vbk['Foerderung_ref'] = 'Bezirkskultur'

    combinado = pd.concat([
        v[['Jahr', 'Foerderung_ref', 'Betrag_EUR']],
        vbk[['Jahr', 'Foerderung_ref', 'Betrag_EUR']]
    ], ignore_index=True)

    tabla = combinado.pivot_table(
        index='Jahr', columns='Foerderung_ref', values='Betrag_EUR',
        aggfunc='sum', fill_value=0
    )
    tabla['TOTAL'] = tabla.sum(axis=1)
    return tabla


if __name__ == '__main__':
    tabla = summe_nach_quelle_und_jahr()
    print(tabla)
