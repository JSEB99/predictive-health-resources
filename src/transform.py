# Libraries
import polars as pl
from variables import rename_dict

pl.Config.set_tbl_cols(18)
# Global variables
RESOURCE_FILES = '../data/conjunto_de_datos_recursos_esep_2024'

# Files
egresos = pl.scan_csv(
    '../data/egresos_hospitalarios_issste2024.csv', separator=';')
clues = pl.read_excel(
    '../data/ESTABLECIMIENTO_SALUD_202508.xlsx', sheet_name='CLUES_202508').lazy()
resources = pl.scan_csv(
    f'{RESOURCE_FILES}/conjunto_de_datos/conjunto_de_datos_recursos_esep_2024.csv')
ageb = pl.scan_csv(f'{RESOURCE_FILES}/catalogos/tc_esep_ageb.csv')
lat_lon_places = pl.scan_csv(
    '../data/AGEEML_20259251148648_utf.csv',
    schema_overrides={'CVE_ENT': pl.Utf8,
                      'LON_DECIMAL': pl.Float64},
    encoding='utf8'
)

# 1️⃣ Link AGEB - Latitude Longitude Files
# 1. Clean string values
lat_lon_places = lat_lon_places.filter(
    (~pl.col('CVE_ENT').is_in(['CD', 'CO', 'CQ', 'CT', 'CY', 'QY'])))
# 2. Change datatypes
lat_lon_places = lat_lon_places.cast({'CVE_ENT': pl.Int64})
# 3. Drop unnecesary columns
lat_lon_places = lat_lon_places.drop(
    ['Estatus', 'POB_MASCULINA', 'POB_FEMENINA', 'CVE_CARTA', 'TOTAL DE VIVIENDAS HABITADAS'])
# 4. Join files
ageb_lat_lon = lat_lon_places.join(
    ageb,
    left_on=['CVE_ENT', 'CVE_MUN', 'CVE_LOC'],
    right_on=['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD'],
    how='right'
)
# 5. Select columns
ageb_lat_lon = ageb_lat_lon.select(pl.col(
    [
        'CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD', 'ENTIDAD',
        'MUNICIPIO', 'LOCALIDAD', 'AGEB', 'LAT_DECIMAL', 'LON_DECIMAL', 'POB_TOTAL'
    ]
))
# 2️⃣ Link Resources - AGEB_Latitude_longitude Files
# 1. Clean AGEB Codes
ageb_lat_lon = ageb_lat_lon.with_columns(
    pl.col('AGEB').str.strip_chars_start('0').alias('AGEB')
)
resources = resources.with_columns(
    pl.col('sreageb').str.strip_chars_start('0').alias('sreageb')
)
# 2. Join
resources_cl = resources.join(
    ageb_lat_lon,
    left_on=['sreentidad', 'sremunic', 'sreageb'],
    right_on=['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'AGEB'],
    how='left'
)

# 3. Drop nan/nulls
resources_cl = resources_cl.drop_nulls()
# 4. Drop columns
resources_cl = resources_cl.drop(
    ['sreconsec', 'sretamloc', 'sretipoest', 'sreageb'])
# print(resources_cl.collect().shape)
# 5. Group By
resources_cl_agg = resources_cl.group_by([
    'sreanio', 'sreentidad', 'sremunic', 'CLAVE_LOCALIDAD', 'ENTIDAD', 'MUNICIPIO', 'LOCALIDAD',
    'LAT_DECIMAL', 'LON_DECIMAL', 'POB_TOTAL'
]).sum()


# 3️⃣ Link Egresos - CLUES
# 1. Clean Egresos
egresos = egresos.with_columns(pl.col(
    'clues').replace('PENDIENTE', 'JCIST000132').alias('clues'))
# 2. Filter CLUES
clues_sel_cols = [
    'CLUES', 'CLAVE DE LA INSTITUCION', 'NOMBRE DE LA INSTITUCION', 'CLAVE DE LA ENTIDAD', 'ENTIDAD',
    'CLAVE DEL MUNICIPIO', 'MUNICIPIO', 'CLAVE DE LA LOCALIDAD', 'LOCALIDAD', 'NOMBRE DE LA UNIDAD',
    'CODIGO POSTAL', 'LATITUD', 'LONGITUD', 'NIVEL ATENCION']
clues_cl = clues.select(pl.col(clues_sel_cols))
# 3. Transform CLUES
clues_cl = clues_cl.with_columns(
    pl.col('CLUES').str.strip_chars().str.to_uppercase().alias('CLUES'))
# 4. Drop columns & transform clues to uppercase
egresos_cl = egresos.with_columns(
    pl.col('clues').str.strip_chars().str.to_uppercase().alias('CLUES'))
egresos_cl = egresos_cl.drop(['entidad', 'unidad', 'clues'])
# 5. Join
egresos_clues_cl = egresos_cl.join(
    clues_cl,
    on='CLUES',
    how='left'
)
# # 4️⃣ Link Egresos - Resources
# 1. Clean Egresos - Resources
egresos_clues_cl = egresos_clues_cl.cast(
    {'LATITUD': pl.Float64, 'LONGITUD': pl.Float64})
egresos_clues_cl = egresos_clues_cl.cast({
    'CLAVE DE LA ENTIDAD': pl.Int64,
    'CLAVE DEL MUNICIPIO': pl.Int64,
    'CLAVE DE LA LOCALIDAD': pl.Int64
})


def truncar_1_decimal_expr(col):
    return (pl.col(col) * 10).floor() / 10


# Para egresos_clues_cl
egresos_clues_cl = egresos_clues_cl.with_columns([
    truncar_1_decimal_expr('LATITUD').alias('lat_trunc'),
    truncar_1_decimal_expr('LONGITUD').alias('lon_trunc')
])

# Para resources_cl_agg
resources_cl_agg = resources_cl_agg.with_columns([
    truncar_1_decimal_expr('LAT_DECIMAL').alias('lat_trunc_res'),
    truncar_1_decimal_expr('LON_DECIMAL').alias('lon_trunc_res')
])

test = resources_cl_agg.select(pl.col(
    ['sreentidad', 'sremunic', 'CLAVE_LOCALIDAD', 'lat_trunc_res', 'lon_trunc_res']))
test2 = egresos_clues_cl.select(pl.col(
    ['CLAVE DE LA ENTIDAD', 'CLAVE DEL MUNICIPIO', 'CLAVE DE LA LOCALIDAD', 'lat_trunc', 'lon_trunc']))


# 2. Join
egresos_resources = resources_cl_agg.join(
    egresos_clues_cl,
    left_on=['sreentidad', 'sremunic',
             'CLAVE_LOCALIDAD', 'lat_trunc_res', 'lon_trunc_res'],
    right_on=['CLAVE DE LA ENTIDAD', 'CLAVE DEL MUNICIPIO',
              'CLAVE DE LA LOCALIDAD', 'lat_trunc', 'lon_trunc'],
    how='inner'
)
choosen_cols_eg_res = ['ENTIDAD_right', 'MUNICIPIO_right', 'LOCALIDAD_right', 'POB_TOTAL'
                       ]
egresos_resources = egresos_resources.drop(choosen_cols_eg_res)

egresos_resources = egresos_resources.rename(rename_dict)
