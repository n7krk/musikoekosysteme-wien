# tabla de referencia unica de cifras citadas en el texto
# correr DESPUES de datenimport (vereine, v_bezirkskultur ya cargados)
# y despues de aplicar ohne_ausnahme() sobre vereine

import pandas as pd

vz = ohne_ausnahme(vereine)  # o vereine_zaehlbar, el nombre que uses vos

def suma_por_anio(df, col_ref, valor, col_monto='Betrag_EUR', col_anio='Jahr'):
    return df[df[col_ref] == valor].groupby(col_anio)[col_monto].sum()

ma7 = suma_por_anio(vz, 'Foerderung_ref', 'MA7')
bmkoes = suma_por_anio(vz, 'Foerderung_ref', 'BMKöS')
bmwkms = suma_por_anio(vz, 'Foerderung_ref', 'BMWKmS')
bezirk = v_bezirkskultur.groupby('Jahr')['Betrag_EUR'].sum()

anios = sorted(set(ma7.index) | set(bmkoes.index) | set(bmwkms.index) | set(bezirk.index))

tabla_ref = pd.DataFrame({
    'MA7': ma7,
    'BMKöS': bmkoes,
    'BMWKmS': bmwkms,
    'Bezirkskultur': bezirk,
}).reindex(anios).fillna(0)

tabla_ref['Total'] = tabla_ref.sum(axis=1)

# presupuesto municipal total por anio (los que ya calculaste a mano)
presupuesto_municipal = {
    2022: 29_069_378,
    2023: 34_810_060,
    2024: 40_337_226,
    # faltan 2025 y 2026 si existen esas cifras
}
tabla_ref['pct_presupuesto_MA7'] = tabla_ref.apply(
    lambda r: r['MA7'] / presupuesto_municipal[r.name] * 100 if r.name in presupuesto_municipal else None,
    axis=1
)

anio_pico = tabla_ref['Total'].idxmax()
print(tabla_ref.round(2))
print()
print(f"anio pico: {anio_pico}, total: {tabla_ref.loc[anio_pico, 'Total']:,.2f}, MA7 ese anio: {tabla_ref.loc[anio_pico, 'MA7']:,.2f}")

# wien modern % (si tenes la fila identificada por Verein_key)
wien_modern = vz[vz['Verein_key'] == 'wien modern']  # ajustar key exacta
wm_pct = wien_modern.groupby('Jahr')['Betrag_EUR'].sum() / ma7 * 100
print()
print("wien modern % de MA7 por anio:")
print(wm_pct.round(2))

tabla_ref.to_csv('tabla_referencia.csv')
