"""
vorstudie_scripts.py
=====================
Todos los scripts pendientes del pipeline de la Vorstudie, consolidados en
un solo archivo para que los corras en Jupyter celda por celda (separados
por # %% para Jupyter/VSCode) o los importes como funciones.

ORDEN DE EJECUCIÓN RECOMENDADO (no corras todo de una):
  1. normalizar_verein_key_dataset()   -- revisá la lista de "sin match" impresa
  2. tabelle1_historische_ma7_reihe()
  3. tabelle2_ma7_nach_sitzbezirk()
  4. tabelle3_bezirk_veranstaltungen_foerderung_jahr()  -- depende de 1
  5. tabelle4_programm_foerderung_jahr()  -- FIX del bug MA7-only
  6. tabelle5_musikbeirat_empfehlungen()  -- revisá "sin_clasificar" impreso
  7. tabelle_foerdersummen_jahr_quelle()
  8. tabelle_bezirkskultur_bezirk()
  9. sitzbezirk_bezirkskultur_empfaenger()  -- tabla SEPARADA de la 8, no fusionar
  10. tabelle_veranstaltungen_bezirk_jahr()
  11. graficas 5-8 (plotly, jupyter)
  12. mapas 1-4 (plotly, jupyter) -- requieren BEZIRKSGRENZEOGD.json en el mismo folder

PENDIENTES QUE ESTE ARCHIVO NO RESUELVE (necesitan tu revisión manual, no
son bugs de código):
  - fila(s) de IMPROPER WALLS con "Bildende Kunst": no existen en vereine.csv
    tal como está hoy. Confirmar origen antes de usarlas en el Bericht.
  - Salam Oida: las 5 filas tienen "— Ausnahme", incluidas 2 de categoría
    genérica (Kulturinitiativen). Confirmar si es exclusión total intencional
    (Verein no confirmado bajo Regla A) o bug pendiente.
  - Tabelle 5 / comparación monto recomendado vs. monto real: no se puede
    automatizar limpio (ver nota en el chat) -- requiere criterio manual
    línea por línea, igual que la nota al pie 15 ya existente en el Bericht.

Dependencias: pandas, plotly (pip install pandas plotly --break-system-packages
si hace falta el flag en tu entorno).
"""

import json
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# utilidades compartidas
# ---------------------------------------------------------------------------

def _to_num(serie_str):
    """Convierte strings 'de coma decimal / punto de miles' a float."""
    return (serie_str.str.replace('.', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .astype(float))


def _filtrar_ausnahme(df, col='Fördergegenstand — Anmerkungen'):
    """Devuelve el df sin las filas marcadas '— Ausnahme'."""
    es_ausnahme = df[col].str.contains('— Ausnahme', regex=False, na=False)
    return df[~es_ausnahme].copy()


# ---------------------------------------------------------------------------
# 1. normalizar_verein_key_dataset
# Para qué: agrega Verein_key a dataset.csv con la MISMA normalización que
# ya usa vereine.csv, para cruzar eventos <-> financiación de forma segura.
# Output: dataset_con_key.csv
# ---------------------------------------------------------------------------

def _normalizar_key_fallback(nombre):
    if not isinstance(nombre, str):
        return None
    n = nombre.lower().strip()
    n = n.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    n = re.sub(r'[^a-z0-9]+', ' ', n).strip()
    return n


def normalizar_verein_key_dataset(path_vereine='vereine.csv', path_dataset='dataset.csv'):
    v = pd.read_csv(path_vereine, sep='\t', dtype=str)
    ds = pd.read_csv(path_dataset, sep='\t', dtype=str)

    lookup = v.drop_duplicates('Verein')[['Verein', 'Verein_key']].set_index('Verein')['Verein_key'].to_dict()

    ds = ds.copy()
    ds['Verein_key'] = ds['Verein'].map(lookup)
    sin_match = ds['Verein_key'].isna()
    ds.loc[sin_match, 'Verein_key'] = ds.loc[sin_match, 'Verein'].apply(_normalizar_key_fallback)
    ds['Verein_en_vereine_csv'] = ~sin_match

    print(f"[normalizar_verein_key_dataset] Filas dataset.csv: {len(ds)}")
    print(f"[normalizar_verein_key_dataset] Sin match exacto en vereine.csv: {sin_match.sum()}")
    print("Nombres sin match (revisar si son legítimamente externos):")
    for n in sorted(ds.loc[sin_match, 'Verein'].unique()):
        print(" -", n)

    ds.to_csv('dataset_con_key.csv', sep='\t', index=False)
    return ds


# ---------------------------------------------------------------------------
# 2. Tabelle 1: Historische MA7-Reihe des dokumentierten Ökosystems (2022-2026)
# Solo MA7 (para financiación total ver tabelle_foerdersummen_jahr_quelle)
# ---------------------------------------------------------------------------

def tabelle1_historische_ma7_reihe(path='vereine.csv'):
    v = pd.read_csv(path, sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v = _filtrar_ausnahme(v)
    ma7 = v[v['Foerderung_ref'] == 'MA7']

    tab = ma7.groupby('Jahr').agg(
        Foerderung_MA7_EUR=('Betrag_EUR_num', 'sum'),
        n_Vereine=('Verein_key', 'nunique')
    ).reset_index().sort_values('Jahr')

    print(tab.to_string(index=False))
    tab.to_csv('tabelle1_historische_ma7_reihe.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 3. Tabelle 2: MA7 Gesamtförderung nach Bezirk (rechtlicher Sitz, 2022-2026)
# Domicilio legal del Verein -- NO cruza con v_bezirkskultur.csv.
# ---------------------------------------------------------------------------

def tabelle2_ma7_nach_sitzbezirk(path='vereine.csv'):
    v = pd.read_csv(path, sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v = _filtrar_ausnahme(v)
    ma7 = v[v['Foerderung_ref'] == 'MA7']

    tab = ma7.groupby('Bezirk').agg(
        Foerderung_MA7_EUR=('Betrag_EUR_num', 'sum'),
        n_Vereine=('Verein_key', 'nunique')
    ).reset_index()

    todos_bezirke = pd.DataFrame({'Bezirk': [str(i) for i in range(1, 24)]})
    tab = todos_bezirke.merge(tab, on='Bezirk', how='left').fillna(0)
    tab['Bezirk'] = tab['Bezirk'].astype(int)
    tab = tab.sort_values('Bezirk')

    print(tab.to_string(index=False))
    tab.to_csv('tabelle2_ma7_nach_sitzbezirk.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 4. Tabelle 3: Bezirk x Veranstaltungen x Förderung x Jahr (2022-2026)
# CUIDADO: financiación agregada UNA VEZ por Verein_key+Jahr antes de cruzar
# con eventos, para no multiplicar la plata por cada evento adicional.
# Input: dataset_con_key.csv (paso 1), vereine.csv
# ---------------------------------------------------------------------------

def tabelle3_bezirk_veranstaltungen_foerderung_jahr(path_ds='dataset_con_key.csv', path_v='vereine.csv'):
    ds = pd.read_csv(path_ds, sep='\t', dtype=str)
    v = pd.read_csv(path_v, sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v = _filtrar_ausnahme(v)

    foerderung_verein_jahr = v.groupby(['Verein_key', 'Jahr'])['Betrag_EUR_num'].sum().reset_index()

    ds = ds.copy()
    ds['Jahr'] = ds['Datum'].str[:4]
    eventos_bezirk_jahr = ds.groupby(['Bezirk', 'Jahr']).agg(
        n_Veranstaltungen=('Event_Name', 'count'),
        Vereine_involucrados=('Verein_key', lambda x: list(x.unique()))
    ).reset_index()

    filas = []
    for _, row in eventos_bezirk_jahr.iterrows():
        foerderung = foerderung_verein_jahr[
            (foerderung_verein_jahr['Verein_key'].isin(row['Vereine_involucrados'])) &
            (foerderung_verein_jahr['Jahr'] == row['Jahr'])
        ]['Betrag_EUR_num'].sum()
        filas.append({
            'Bezirk': row['Bezirk'],
            'Jahr': row['Jahr'],
            'n_Veranstaltungen': row['n_Veranstaltungen'],
            'Foerderung_zugehoeriger_Vereine_EUR': foerderung
        })

    tab = pd.DataFrame(filas).sort_values(['Jahr', 'Bezirk'])
    print(tab.to_string(index=False))
    print("\nOJO: 'Foerderung_zugehoeriger_Vereine_EUR' es la financiación anual de los")
    print("Vereine con algún evento en ese Bezirk-Jahr, NO 'plata gastada en ese Bezirk'.")
    tab.to_csv('tabelle3_bezirk_veranstaltungen_foerderung_jahr.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 5. Tabelle 4: Programm x Förderung nach Jahr (2022-2026) -- FIX del bug
# conocido (versión anterior solo sumaba MA7, ignoraba BMKöS_BMWKmS).
# ---------------------------------------------------------------------------

def tabelle4_programm_foerderung_jahr(path='vereine.csv'):
    v = pd.read_csv(path, sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v = _filtrar_ausnahme(v)

    tab = v.groupby(['Programm', 'Jahr']).agg(
        Foerderung_gesamt_EUR=('Betrag_EUR_num', 'sum'),
        n_Vereine=('Verein_key', 'nunique')
    ).reset_index().sort_values(['Programm', 'Jahr'])

    print(tab.to_string(index=False))
    tab.to_csv('tabelle4_programm_foerderung_jahr.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 6. Tabelle 5: Empfehlungen des Musikbeirats und Beschlussstatus (2025-2026)
# NO hay columna de estado limpia en vereine_empfehlungen.csv -- clasifica
# por texto en Anmerkungen. REVISÁ 'sin_clasificar' antes de confiar.
# ---------------------------------------------------------------------------

def _clasificar_status(anmerkung):
    if not isinstance(anmerkung, str):
        return 'sin_clasificar'
    a = anmerkung.lower()
    if 'keine förderzusage' in a:
        return 'Empfehlung ohne Förderzusage'
    if a.strip() == 'empfehlung':
        return 'Empfehlung — Status nicht dokumentiert'
    if 'projekt:' in a:
        return 'Empfehlung mit Projektbezug — Status nicht dokumentiert'
    return 'sin_clasificar'


def tabelle5_musikbeirat_empfehlungen(path='vereine_empfehlungen.csv'):
    emp = pd.read_csv(path, sep='\t', dtype=str)
    emp['Beschlussstatus'] = emp['Anmerkungen'].apply(_clasificar_status)

    sin_clasificar = emp[emp['Beschlussstatus'] == 'sin_clasificar']
    print(f"[tabelle5] Filas sin clasificar: {len(sin_clasificar)}")
    if len(sin_clasificar):
        print(sin_clasificar[['Verein', 'Jahr', 'Anmerkungen']].to_string(index=False))

    tab = emp[['Verein', 'Jahr', 'Betrag_EUR', 'Beschlussstatus', 'Anmerkungen']].sort_values(['Jahr', 'Verein'])
    print(tab.to_string(index=False))
    tab.to_csv('tabelle5_musikbeirat_empfehlungen.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 7. tabelle_foerdersummen_jahr_quelle: Förderung total nach Jahr x Quelle
# (a diferencia de Tabelle 1 que es MA7 solamente)
# ---------------------------------------------------------------------------

def tabelle_foerdersummen_jahr_quelle(path='vereine.csv'):
    v = pd.read_csv(path, sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v = _filtrar_ausnahme(v)

    tab = v.groupby(['Jahr', 'Foerderung_ref'])['Betrag_EUR_num'].sum().reset_index()
    tab = tab.rename(columns={'Foerderung_ref': 'Quelle', 'Betrag_EUR_num': 'Foerderung_EUR'})
    tab = tab.sort_values(['Jahr', 'Quelle'])

    print(tab.to_string(index=False))
    tab.to_csv('tabelle_foerdersummen_jahr_quelle.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 8. tabelle_bezirkskultur_bezirk: Bezirkskultur-Förderung nach Bezirk
# (dónde se financió -- Förderung_Bezirk propio de v_bezirkskultur.csv,
# NO domicilio legal del Verein. Ver script 9 para esa tabla separada.)
# ---------------------------------------------------------------------------

def tabelle_bezirkskultur_bezirk(path='v_bezirkskultur.csv'):
    vb = pd.read_csv(path, sep='\t', dtype=str)
    vb['Betrag_EUR_num'] = _to_num(vb['Betrag_EUR'])

    tab = vb.groupby('Förderung_Bezirk').agg(
        Foerderung_EUR=('Betrag_EUR_num', 'sum'),
        n_Foerderungen=('Verein', 'count')
    ).reset_index().sort_values('Foerderung_EUR', ascending=False)

    nd = tab[tab['Förderung_Bezirk'] == '[nicht dokumentiert]']
    print(f"[tabelle_bezirkskultur_bezirk] '[nicht dokumentiert]': {nd['n_Foerderungen'].sum() if len(nd) else 0} de {len(vb)} filas totales")
    print(tab.to_string(index=False))
    tab.to_csv('tabelle_bezirkskultur_bezirk.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 9. sitzbezirk_bezirkskultur_empfaenger: Sitzbezirk de los Vereine que
# recibieron Bezirkskultur. Tabla NARRATIVA APARTE de la 8 -- NO fusionar.
# Continuación de 01_cruce_bezirkskultur_por_bezirk.py.
# ---------------------------------------------------------------------------

def sitzbezirk_bezirkskultur_empfaenger(path_vereine='vereine.csv', path_vbk='v_bezirkskultur.csv'):
    v = pd.read_csv(path_vereine, sep='\t', dtype=str).dropna(subset=['Verein_key'])
    vb = pd.read_csv(path_vbk, sep='\t', dtype=str)

    bezirk_por_verein = v.groupby('Verein_key')['Bezirk'].nunique()
    keys_consistentes = bezirk_por_verein[bezirk_por_verein == 1].index
    lookup = v[v['Verein_key'].isin(keys_consistentes)].groupby('Verein_key')['Bezirk'].first().to_dict()

    def buscar_bezirk(nombre_corto):
        n = nombre_corto.lower().strip().replace('+', ' ')
        for key, bezirk in lookup.items():
            if not isinstance(key, str):
                continue
            key_norm = key.replace('+', ' ')
            primer_tramo = key_norm.split(' - ')[0].split(',')[0].strip()
            if n in key_norm or primer_tramo in n or n == primer_tramo:
                return bezirk
        return None

    vb = vb.copy()
    vb['Sitzbezirk_Verein'] = vb['Verein'].apply(buscar_bezirk)
    vb['Bezirk_diskrepanz'] = vb['Sitzbezirk_Verein'] != vb['Förderung_Bezirk']

    sin_bezirk = vb[vb['Sitzbezirk_Verein'].isna()]['Verein'].unique().tolist()
    print('[sitzbezirk_bezirkskultur_empfaenger] Sin Sitzbezirk asignado (revisión manual):', sin_bezirk)
    print(f"Filas con Sitzbezirk != Förderung_Bezirk: {vb['Bezirk_diskrepanz'].sum()} de {len(vb)}")

    vb.to_csv('sitzbezirk_bezirkskultur_empfaenger.csv', sep='\t', index=False)
    return vb


# ---------------------------------------------------------------------------
# 10. tabelle_veranstaltungen_bezirk_jahr: conteo de eventos por Bezirk x Jahr
# No necesita cruce con vereine.csv (a diferencia de Tabelle 3).
# ---------------------------------------------------------------------------

def tabelle_veranstaltungen_bezirk_jahr(path='dataset.csv'):
    ds = pd.read_csv(path, sep='\t', dtype=str)
    ds = ds.copy()
    ds['Jahr'] = ds['Datum'].str[:4]

    tab = ds.groupby(['Bezirk', 'Jahr']).size().reset_index(name='n_Veranstaltungen')

    bezirke = [str(i) for i in range(1, 24)]
    jahre = sorted(ds['Jahr'].unique())
    idx = pd.MultiIndex.from_product([bezirke, jahre], names=['Bezirk', 'Jahr'])
    tab = tab.set_index(['Bezirk', 'Jahr']).reindex(idx, fill_value=0).reset_index()
    tab['Bezirk'] = tab['Bezirk'].astype(int)
    tab = tab.sort_values(['Jahr', 'Bezirk'])

    print(tab.to_string(index=False))
    tab.to_csv('tabelle_veranstaltungen_bezirk_jahr.csv', sep='\t', index=False)
    return tab


# ---------------------------------------------------------------------------
# 11. Gráficas Plotly 5-8 (Jupyter)
# Márgenes/tamaños ajustados para que nombres largos en alemán no se corten.
# ---------------------------------------------------------------------------

def _cargar_para_graficas():
    ds = pd.read_csv('dataset_con_key.csv', sep='\t', dtype=str)
    v = pd.read_csv('vereine.csv', sep='\t', dtype=str)
    v['Betrag_EUR_num'] = _to_num(v['Betrag_EUR'])
    v['contable'] = ~v['Fördergegenstand — Anmerkungen'].str.contains('— Ausnahme', regex=False, na=False)
    ds = ds.copy()
    ds['Jahr_Monat'] = ds['Datum'].str[:7]
    return ds, v


def grafica5_zeitreihe(ds):
    tab = ds.groupby('Jahr_Monat').size().reset_index(name='n_Veranstaltungen')
    fig = px.bar(tab, x='Jahr_Monat', y='n_Veranstaltungen',
                 title='Veranstaltungen pro Monat (2022-2026)')
    fig.update_layout(xaxis_tickangle=-45, margin=dict(b=120))
    fig.write_html('grafica5_veranstaltungen_zeitreihe.html')
    return fig


def grafica6_top_vereine(ds, v):
    n_eventos = ds.groupby('Verein_key').size().rename('n_Veranstaltungen')
    eur_total = v[v['contable']].groupby('Verein_key')['Betrag_EUR_num'].sum().rename('Foerderung_EUR')
    nombre = v.drop_duplicates('Verein_key').set_index('Verein_key')['Verein']

    tab = pd.concat([n_eventos, eur_total], axis=1).fillna(0)
    tab['Verein'] = tab.index.map(nombre)
    tab = tab.dropna(subset=['Verein']).sort_values('Foerderung_EUR', ascending=False).head(25)

    fig = px.scatter(tab, x='n_Veranstaltungen', y='Foerderung_EUR', text='Verein',
                      title='Top 25 Vereine: Veranstaltungen vs. Förderung (EUR)')
    fig.update_traces(textposition='top center')
    fig.update_layout(margin=dict(l=80, r=80, t=80, b=80))
    fig.write_html('grafica6_top_vereine_eventos_foerderung.html')
    return fig


def grafica7_heatmap_bezirk_verein(ds):
    tab = ds.groupby(['Bezirk', 'Verein']).size().reset_index(name='n')
    top_vereine = tab.groupby('Verein')['n'].sum().sort_values(ascending=False).head(30).index
    tab = tab[tab['Verein'].isin(top_vereine)]
    pivot = tab.pivot(index='Verein', columns='Bezirk', values='n').fillna(0)

    fig = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Viridis'))
    fig.update_layout(title='Bezirk x Verein (Top 30 nach Anzahl Veranstaltungen)',
                       height=max(600, 20 * len(pivot)), margin=dict(l=250))
    fig.write_html('grafica7_heatmap_bezirk_verein.html')
    return fig


def grafica8_typ_por_bezirk(ds):
    tab = ds.groupby(['Bezirk', 'Event_Typ']).size().reset_index(name='n')
    fig = px.bar(tab, x='Bezirk', y='n', color='Event_Typ', barmode='stack',
                 title='Event_Typ Verteilung nach Bezirk',
                 category_orders={'Bezirk': [str(i) for i in range(1, 24)]})
    fig.update_layout(margin=dict(b=100))
    fig.write_html('grafica8_event_typ_por_bezirk.html')
    return fig


def correr_graficas_5_a_8():
    ds, v = _cargar_para_graficas()
    grafica5_zeitreihe(ds)
    grafica6_top_vereine(ds, v)
    grafica7_heatmap_bezirk_verein(ds)
    grafica8_typ_por_bezirk(ds)
    print("4 gráficas exportadas como .html")


# ---------------------------------------------------------------------------
# 12. Mapas Plotly 1-4 (Jupyter)
# Geojson: BEZIRKSGRENZEOGD.json (Bezirksgrenzen Wien, data.gv.at).
# Campo de cruce CONFIRMADO: 'BEZNR' (entero simple 1-23, sin ceros a la
# izquierda -- coincide directo con str(Bezirk), sin padding necesario).
# ---------------------------------------------------------------------------

GEOJSON_PATH = 'BEZIRKSGRENZEOGD.json'
CAMPO_ID_GEOJSON = 'BEZNR'


def _cargar_geojson():
    with open(GEOJSON_PATH, encoding='utf-8') as f:
        return json.load(f)


def mapa1_densidad_eventos(tab_eventos_bezirk):
    """tab_eventos_bezirk: salida de tabelle_veranstaltungen_bezirk_jahr(),
    agregada total (no por año) para el mapa."""
    geo = _cargar_geojson()
    tab = tab_eventos_bezirk.groupby('Bezirk')['n_Veranstaltungen'].sum().reset_index()
    tab['Bezirk'] = tab['Bezirk'].astype(str)

    fig = px.choropleth_mapbox(tab, geojson=geo, locations='Bezirk',
                                featureidkey=f'properties.{CAMPO_ID_GEOJSON}',
                                color='n_Veranstaltungen', color_continuous_scale='Viridis',
                                mapbox_style='carto-positron', zoom=10,
                                center={'lat': 48.2082, 'lon': 16.3738}, opacity=0.7,
                                title='Veranstaltungsdichte nach Bezirk (2022-2026)')
    fig.write_html('mapa1_dichte_eventos_bezirk.html')
    return fig


def mapa2_venues(path_venues='venues.csv'):
    """No necesita geojson -- usa lat/lon directo de venues.csv (0 nulos)."""
    venues = pd.read_csv(path_venues, sep='\t', dtype=str)
    venues = venues.copy()
    venues['lat'] = venues['lat'].astype(float)
    venues['lon'] = venues['lon'].astype(float)

    fig = px.scatter_mapbox(venues, lat='lat', lon='lon', color='Klassifiezierung',
                             hover_name='Venue', hover_data=['Adresse', 'Programmprofil'],
                             mapbox_style='carto-positron', zoom=11,
                             center={'lat': 48.2082, 'lon': 16.3738},
                             title='Venues nach Klassifizierung')
    fig.write_html('mapa2_venues_klassifizierung.html')
    return fig


def mapa3_foerderung_sitzbezirk(tab2):
    """tab2: salida de tabelle2_ma7_nach_sitzbezirk()."""
    geo = _cargar_geojson()
    tab = tab2.copy()
    tab['Bezirk'] = tab['Bezirk'].astype(str)

    fig = px.choropleth_mapbox(tab, geojson=geo, locations='Bezirk',
                                featureidkey=f'properties.{CAMPO_ID_GEOJSON}',
                                color='Foerderung_MA7_EUR', color_continuous_scale='Plasma',
                                mapbox_style='carto-positron', zoom=10,
                                center={'lat': 48.2082, 'lon': 16.3738}, opacity=0.7,
                                title='MA7-Förderung nach Sitzbezirk (2022-2026)')
    fig.write_html('mapa3_foerderung_sitzbezirk.html')
    return fig


def mapa4_eventos_vs_foerderung(tab_eventos_bezirk, tab2):
    geo = _cargar_geojson()
    ev = tab_eventos_bezirk.groupby('Bezirk')['n_Veranstaltungen'].sum().reset_index()
    ev['Bezirk'] = ev['Bezirk'].astype(str)
    tab2 = tab2.copy()
    tab2['Bezirk'] = tab2['Bezirk'].astype(str)

    merged = ev.merge(tab2, on='Bezirk', how='outer').fillna(0)
    fig = px.choropleth_mapbox(merged, geojson=geo, locations='Bezirk',
                                featureidkey=f'properties.{CAMPO_ID_GEOJSON}',
                                color='n_Veranstaltungen', color_continuous_scale='Viridis',
                                mapbox_style='carto-positron', zoom=10,
                                center={'lat': 48.2082, 'lon': 16.3738}, opacity=0.6,
                                hover_data=['Foerderung_MA7_EUR'],
                                title='Veranstaltungen vs. Förderung nach Bezirk')
    fig.write_html('mapa4_eventos_vs_foerderung.html')
    return fig


def correr_mapas(tab_eventos_bezirk, tab2):
    mapa1_densidad_eventos(tab_eventos_bezirk)
    mapa2_venues()
    mapa3_foerderung_sitzbezirk(tab2)
    mapa4_eventos_vs_foerderung(tab_eventos_bezirk, tab2)
    print("4 mapas exportados como .html")


# ---------------------------------------------------------------------------
# main -- corre todo en orden. Comentá lo que no quieras correr todavía.
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    normalizar_verein_key_dataset()
    tabelle1_historische_ma7_reihe()
    tab2 = tabelle2_ma7_nach_sitzbezirk()
    tabelle3_bezirk_veranstaltungen_foerderung_jahr()
    tabelle4_programm_foerderung_jahr()
    tabelle5_musikbeirat_empfehlungen()
    tabelle_foerdersummen_jahr_quelle()
    tabelle_bezirkskultur_bezirk()
    sitzbezirk_bezirkskultur_empfaenger()
    tab_ev = tabelle_veranstaltungen_bezirk_jahr()
    correr_graficas_5_a_8()
    correr_mapas(tab_ev, tab2)
