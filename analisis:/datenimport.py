import re
import json
import pandas as pd

# ---------- 1. lectura de los 6 csv ----------
vereine = pd.read_csv('vereine.csv', sep='\t')
vereine['Betrag_EUR'] = pd.to_numeric(vereine['Betrag_EUR'], errors='coerce')
vereine['Bezirk'] = vereine['Bezirk'].astype(str).str.strip()
vereine['Jahr'] = pd.to_numeric(vereine['Jahr'], errors='coerce').astype('Int64')

bezirkskultur = pd.read_csv('v_bezirkskultur.csv', sep='\t')
bezirkskultur['Betrag_EUR'] = pd.to_numeric(bezirkskultur['Betrag_EUR'], errors='coerce')
bezirkskultur['Jahr'] = pd.to_numeric(bezirkskultur['Jahr'], errors='coerce').astype('Int64')

dataset = pd.read_csv('dataset.csv', sep='\t')
dataset['Jahr'] = pd.to_datetime(dataset['Datum'], errors='coerce').dt.year
dataset['Bezirk'] = dataset['Bezirk'].astype(str).str.strip()

klingt = pd.read_csv('klingt_org.csv', sep='\t')
klingt['Jahr'] = pd.to_datetime(klingt['Datum'], errors='coerce').dt.year

venues = pd.read_csv('venues.csv', sep='\t')
venues['lat'] = pd.to_numeric(venues['lat'], errors='coerce')
venues['lon'] = pd.to_numeric(venues['lon'], errors='coerce')

empfehlungen = pd.read_csv('vereine_empfehlungen.csv', sep='\t')
empfehlungen['Betrag_EUR'] = pd.to_numeric(empfehlungen['Betrag_EUR'], errors='coerce')

with open(GEOJSON_PATH, encoding='utf-8') as f:
    geo_bezirke = json.load(f)

# ---------- 2. normalizador fallback (confirmado por vos, sin cambios) ----------
def normalisiere_key_fallback(name):
    if not isinstance(name, str):
        return None
    n = name.lower().strip()
    n = n.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    n = re.sub(r'[^a-z0-9]+', ' ', n).strip()
    return n

# ---------- 3. ASUNCION: Verein_key en vereine.csv se genera con el mismo normalizador ----------
# esto es lo que NO teniamos documentado. si tu Verein_key original en vereine
# usaba otra logica (por ejemplo sin reemplazo de umlauts, como se menciono en
# otra sesion para IGNM: ".lower().strip()" plano, sin ae/oe/ue), avisame y
# cambio esta linea. por ahora uso el mismo fallback que ya usabas para dataset/klingt,
# para que las tres columnas Verein_key sean consistentes entre si.
vereine['Verein_key'] = vereine['Verein'].apply(normalisiere_key_fallback)

# ---------- 4. patch manual IGNM ----------
# reconstruido de la conversacion previa, clave en minuscula porque el lookup
# hace name.lower().strip() como primer paso adentro del fallback tambien.
# ajustar el string de la izquierda si el nombre exacto en dataset.csv/klingt_org.csv es distinto.
patch_manual = {
    'ignm – internationale gesellschaft für neue musik österreich': 'internationale gesellschaft für neue musik, sektion österreich',
}

lookup_key = vereine.drop_duplicates('Verein').set_index('Verein')['Verein_key'].to_dict()

def aplica_key(df):
    df['Verein_key'] = df['Verein'].map(lookup_key)
    ohne_match = df['Verein_key'].isna()
    df.loc[ohne_match, 'Verein_key'] = df.loc[ohne_match, 'Verein'].apply(normalisiere_key_fallback)
    # patch manual encima, por si el nombre cae en el diccionario de excepciones
    for nombre_raw, key_correcta in patch_manual.items():
        mask = df['Verein'].astype(str).str.lower().str.strip() == nombre_raw
        df.loc[mask, 'Verein_key'] = key_correcta
    df['Verein_in_vereine_csv'] = df['Verein_key'].isin(vereine['Verein_key'])
    return df

dataset = aplica_key(dataset)
klingt = aplica_key(klingt)

print('vereine:', vereine.shape)
print('bezirkskultur:', bezirkskultur.shape)
print('dataset:', dataset.shape)
print('klingt:', klingt.shape)
print('venues:', venues.shape)
print('empfehlungen:', empfehlungen.shape)
