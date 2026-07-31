"""
04_allgemeine_verifikation.py

Calcula todas las cifras verificables del corpus, desde cero, cada vez que se
corre. A diferencia de una version anterior de este script, NO compara contra
numeros escritos a mano (esos quedan viejos apenas se agrega una fila nueva
a vereine.csv). Este script es la fuente de verdad -- se compara su output
contra lo que dice el Bericht en el momento de revisar, no al reves.

Uso:
    python 04_allgemeine_verifikation.py
o en Jupyter:
    from _04_allgemeine_verifikation import allgemeine_verifikation
    resultados = allgemeine_verifikation()
"""
import pandas as pd


def allgemeine_verifikation(path_vereine='vereine.csv'):
    v = pd.read_csv(path_vereine, sep='\t')
    v['Betrag_EUR'] = pd.to_numeric(v['Betrag_EUR'], errors='coerce')
    beschluss = v[v['Typ'] == 'Beschluss']

    resultados = {}

    resultados['filas_totales'] = len(v)
    resultados['filas_beschluss'] = len(beschluss)

    for fuente in ['MA7', 'BMKöS', 'BMWKmS', 'Bezirkskultur']:
        serie = beschluss[beschluss['Foerderung_ref'].str.upper() == fuente.upper()].groupby('Jahr')['Betrag_EUR'].sum()
        resultados[f'serie_{fuente}'] = serie

    # duplicados exactos (mismo Verein/Jahr/Betrag/Foerderung_ref/Typ) -- revisar
    # manualmente si son duplicados reales o dos proyectos distintos con igual monto
    dups = v[v.duplicated(subset=['Verein', 'Jahr', 'Betrag_EUR', 'Foerderung_ref', 'Typ'], keep=False)]
    resultados['posibles_duplicados'] = dups[['Verein', 'Jahr', 'Betrag_EUR', 'Foerderung_ref', 'Quelle']]

    return resultados


if __name__ == '__main__':
    r = allgemeine_verifikation()
    print(f"Filas totales: {r['filas_totales']}  |  Beschluss: {r['filas_beschluss']}")
    print()
    for fuente in ['MA7', 'BMKöS', 'BMWKmS', 'Bezirkskultur']:
        print(f"--- {fuente} ---")
        print(r[f'serie_{fuente}'])
        print()
    print("--- posibles duplicados (revisar Quelle antes de asumir que son error) ---")
    print(r['posibles_duplicados'].to_string() if len(r['posibles_duplicados']) else "  (ninguno)")
