"""
01_bezirkskultur_bezirk_zuordnung.py

Cruza v_bezirkskultur.csv contra vereine.csv para obtener el Bezirk de cada
Verein, SIN modificar ni guardar ningun archivo nuevo. El cruce es por
nombre de Verein, usando el historial de Bezirk ya documentado en vereine.csv.

Un Verein solo recibe Bezirk si tiene un unico valor consistente en todo su
historial en vereine.csv. Si el historial tiene valores contradictorios
(ej. reubicaciones no reales / errores de carga), o si el nombre no matchea,
queda como None y hay que resolverlo a mano.

Uso:
    from bezirkskultur_bezirk_zuordnung import bezirkskultur_mit_bezirk
    df = bezirkskultur_mit_bezirk()
"""
import pandas as pd


def bezirkskultur_mit_bezirk(path_vereine='vereine.csv', path_vbk='v_bezirkskultur.csv'):
    v = pd.read_csv(path_vereine, sep='\t').dropna(subset=['Verein_key'])
    vb = pd.read_csv(path_vbk, sep='\t')

    bezirk_por_verein = v.groupby('Verein_key')['Bezirk'].nunique()
    keys_consistentes = bezirk_por_verein[bezirk_por_verein == 1].index
    lookup = v[v['Verein_key'].isin(keys_consistentes)].groupby('Verein_key')['Bezirk'].first().to_dict()

    def buscar_bezirk(nombre_corto):
        n = nombre_corto.lower().strip().replace('+', ' ')
        for key, bezirk in lookup.items():
            if not isinstance(key, str):
                continue
            primer_tramo = key.split(' - ')[0].split(',')[0].strip()
            if n in key or primer_tramo in n or n == primer_tramo:
                return bezirk
        return None

    vb = vb.copy()
    vb['Bezirk'] = vb['Verein'].apply(buscar_bezirk)
    return vb


if __name__ == '__main__':
    df = bezirkskultur_mit_bezirk()
    print(df[['Verein', 'Jahr', 'Betrag_EUR', 'Bezirk']].to_string())
    sin_bezirk = df[df['Bezirk'].isna()]['Verein'].unique().tolist()
    print()
    print('Sin Bezirk asignado (requiere revision manual):', sin_bezirk)
    print('Total Bezirkskultur:', df['Betrag_EUR'].sum())
