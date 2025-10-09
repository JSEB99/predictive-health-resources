import pandas as pd
import numpy as np
from variables import combinations


def truncar_1_decimal(x):
    return np.trunc(x * 10) / 10


# Global variables
RESOURCE_FILES = '../data/conjunto_de_datos_recursos_esep_2024'

egresos = pd.read_csv('../data/egresos_hospitalarios_issste2024.csv', sep=';')
clues = pd.read_excel(
    '../data/ESTABLECIMIENTO_SALUD_202508.xlsx', sheet_name='CLUES_202508')
resources = pd.read_csv(
    f'{RESOURCE_FILES}/conjunto_de_datos/conjunto_de_datos_recursos_esep_2024.csv')
ageb = pd.read_csv(f'{RESOURCE_FILES}/catalogos/tc_esep_ageb.csv')
lat_lon_places = pd.read_csv(
    '../data/AGEEML_20259251148648_utf.csv', low_memory=False)

lat_lon_places = lat_lon_places[~lat_lon_places['CVE_ENT'].isin(
    ['CD', 'CO', 'CQ', 'CT', 'CY', 'QY'])]
lat_lon_places['CVE_ENT'] = lat_lon_places['CVE_ENT'].astype(int)
lat_lon_places['CVE_MUN'] = lat_lon_places['CVE_MUN'].astype(int)
lat_lon_places['CVE_LOC'] = lat_lon_places['CVE_LOC'].astype(int)

ageb_lat_lon = pd.merge(
    lat_lon_places,
    ageb,
    left_on=['CVE_ENT', 'CVE_MUN', 'CVE_LOC'],
    right_on=['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD'],
    how='right'
)

ageb_lat_lon_cols = [
    'CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD', 'ENTIDAD',
    'MUNICIPIO', 'LOCALIDAD', 'AGEB', 'LAT_DECIMAL', 'LON_DECIMAL', 'POB_TOTAL']
ageb_lat_lon_cl = ageb_lat_lon[ageb_lat_lon_cols].copy()
# print(ageb_lat_lon_cl.shape) #!PASA

resources['sreageb'] = resources['sreageb'].str.lstrip('0')
ageb_lat_lon_cl['AGEB'] = ageb_lat_lon_cl['AGEB'].str.lstrip('0')

resources_cl = pd.merge(
    resources,
    ageb_lat_lon_cl,
    left_on=['sreentidad', 'sremunic', 'sreageb'],
    right_on=['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'AGEB'],
    how='left'
)
# print(resources_cl.shape) #!PASA
# print(resources_cl.isna().sum(), len(resources_cl)) #!PASA
# Drop nan (few nan values)
resources_cl.dropna(inplace=True)
# print(resources_cl.shape) #!PASA

no_choosen_cols_res = ['sreconsec', 'sretamloc',
                       'sretipoest', 'sreageb', 'sreentidad', 'sremunic', 'AGEB']
resources_cl_unique = resources_cl.drop(columns=no_choosen_cols_res)

resources_cl_agg = resources_cl_unique.groupby([
    'sreanio', 'CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD', 'ENTIDAD', 'MUNICIPIO', 'LOCALIDAD',
    'LAT_DECIMAL', 'LON_DECIMAL', 'POB_TOTAL'
]).sum()

resources_cl_agg.reset_index(inplace=True)

# print(resources_cl_agg.shape) #!PASA

egresos.replace({'clues': {'PENDIENTE': 'JCIST000132'}}, inplace=True)

clues_sel_cols = [
    'CLUES', 'CLAVE DE LA INSTITUCION', 'NOMBRE DE LA INSTITUCION', 'CLAVE DE LA ENTIDAD', 'ENTIDAD',
    'CLAVE DEL MUNICIPIO', 'MUNICIPIO', 'CLAVE DE LA LOCALIDAD', 'LOCALIDAD', 'NOMBRE DE LA UNIDAD',
    'CODIGO POSTAL', 'LATITUD', 'LONGITUD', 'NIVEL ATENCION']
clues_cl = clues[clues_sel_cols].copy()
clues_cl['CLUES'] = clues_cl['CLUES'].str.strip().str.upper()

egresos_cl = egresos.drop(columns=['entidad', 'unidad'])
egresos_cl['clues'] = egresos_cl['clues'].str.strip().str.upper()

# print(egresos_cl.shape, clues_cl.shape) #!PASA

egresos_clues_cl = pd.merge(
    egresos_cl, clues_cl, left_on='clues', right_on='CLUES', how='left')
# print(egresos_clues_cl.shape) #!PASA


egresos_clues_cl.loc[:, 'lat_trunc'] = truncar_1_decimal(
    egresos_clues_cl['LATITUD'])
egresos_clues_cl.loc[:, 'lon_trunc'] = truncar_1_decimal(
    egresos_clues_cl['LONGITUD'])
resources_cl_agg.loc[:, 'lat_trunc_res'] = truncar_1_decimal(
    resources_cl_agg['LAT_DECIMAL'])
resources_cl_agg.loc[:, 'lon_trunc_res'] = truncar_1_decimal(
    resources_cl_agg['LON_DECIMAL'])

# print(f'{resources_cl_agg[['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD', 'lat_trunc_res', 'lon_trunc_res']].duplicated().sum()=}')
# print(f'{egresos_clues_cl[['CLAVE DE LA ENTIDAD', 'CLAVE DEL MUNICIPIO', 'CLAVE DE LA LOCALIDAD', 'lat_trunc', 'lon_trunc']].duplicated().sum()=}')

# print(egresos_clues_cl[~egresos_clues_cl[['CLAVE DE LA ENTIDAD', 'CLAVE DEL MUNICIPIO',
#       'CLAVE DE LA LOCALIDAD', 'lat_trunc', 'lon_trunc']].duplicated()])

egresos_resources = pd.merge(
    resources_cl_agg,
    egresos_clues_cl,
    left_on=['CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO',
             'CLAVE_LOCALIDAD', 'lat_trunc_res', 'lon_trunc_res'],
    right_on=['CLAVE DE LA ENTIDAD', 'CLAVE DEL MUNICIPIO',
              'CLAVE DE LA LOCALIDAD', 'lat_trunc', 'lon_trunc'],
    how='inner'
)
# print(egresos_resources.shape) #!PASA

choosen_cols_eg_res = [
    'CLAVE_ENTIDAD', 'CLAVE_MUNICIPIO', 'CLAVE_LOCALIDAD', 'ENTIDAD_x', 'MUNICIPIO_x', 'LOCALIDAD_x',
    'POB_TOTAL', 'CLUES'
]
egresos_resources.drop(columns=choosen_cols_eg_res, inplace=True)
rename_dict = {
    # Año y localización
    'sreanio': 'anio',
    'sreentidad': 'clave_entidad',
    'sremunic': 'clave_municipio',
    'sreconsec': 'consecutivo',
    'sretamloc': 'tamano_localidad',
    'sretipoest': 'tipo_establecimiento',
    'sreageb': 'ageb',

    # Coordenadas
    'LAT_DECIMAL': 'lat_decimal',
    'LON_DECIMAL': 'lon_decimal',
    'LATITUD': 'latitud',
    'LONGITUD': 'longitud',
    'lat_trunc_res': 'lat_trunc_res',
    'lon_trunc_res': 'lon_trunc_res',
    'lat_trunc': 'lat_trunc',
    'lon_trunc': 'lon_trunc',

    # Datos de egresos
    'clues': 'clues',
    'edad_anios': 'edad_anios',
    'sexo': 'sexo',
    'servicio_troncal': 'servicio_troncal',
    'tipo_derechohabiente': 'tipo_derechohabiente',
    'fecha_ingreso': 'fecha_ingreso',
    'fecha_egreso': 'fecha_egreso',
    'diagnostico_principal_cie10': 'diagnostico_principal_cie10',
    'descripcion_cie_010': 'descripcion_diagnostico',

    # Institución y unidad médica
    'CLAVE DE LA INSTITUCION': 'clave_institucion',
    'NOMBRE DE LA INSTITUCION': 'nombre_institucion',
    'CLAVE DE LA ENTIDAD': 'clave_entidad_egresos',
    'ENTIDAD_y': 'nombre_entidad',
    'CLAVE DEL MUNICIPIO': 'clave_municipio_egresos',
    'MUNICIPIO_y': 'nombre_municipio',
    'CLAVE DE LA LOCALIDAD': 'clave_localidad',
    'LOCALIDAD_y': 'nombre_localidad',
    'NOMBRE DE LA UNIDAD': 'nombre_unidad',
    'CODIGO POSTAL': 'codigo_postal',
    'NIVEL ATENCION': 'nivel_atencion',

    # Recursos humanos y materiales (fragmento, puedes extenderlo más si gustas)
    'sre378_nh': 'personal_medico_nomina',
    'sre378_ae': 'personal_medico_acuerdo',
    'sre379_nh': 'contacto_directo_paciente_nomina',
    'sre379_ae': 'contacto_directo_paciente_acuerdo',
    'sre380_nh': 'medicos_generales_nomina',
    'sre380_ae': 'medicos_generales_acuerdo',
    'sre381_nh': 'especialistas_nomina',
    'sre381_ae': 'especialistas_acuerdo',
    'sre382_nh': 'ginecoobstetras_nomina',
    'sre382_ae': 'ginecoobstetras_acuerdo',
    'sre383_nh': 'pediatras_nomina',
    'sre383_ae': 'pediatras_acuerdo',
    'sre384_nh': 'cirujanos_nomina',
    'sre384_ae': 'cirujanos_acuerdo',
    'sre385_nh': 'internistas_nomina',
    'sre385_ae': 'internistas_acuerdo',
    'sre386_nh': 'anestesiologos_nomina',
    'sre386_ae': 'anestesiologos_acuerdo',
    'sre387_nh': 'otros_especialistas_nomina',
    'sre387_ae': 'otros_especialistas_acuerdo',
    'sre388_nh': 'odontologos_nomina',
    'sre388_ae': 'odontologos_acuerdo',
    'sre389_nh': 'residentes_nomina',
    'sre389_ae': 'residentes_acuerdo',
    'sre390_nh': 'pasantes_nomina',
    'sre390_ae': 'pasantes_acuerdo',
    'sre391_nh': 'medicos_otras_labores_nomina',
    'sre391_ae': 'medicos_otras_labores_acuerdo',
    'sre392': 'personal_no_medico',
    'sre393': 'diagnostico_medico',
    'sre394': 'tratamiento_medico',
    'sre395': 'personal_paramedico',
    'sre396': 'auxiliares_enfermeria',
    'sre397': 'enfermeras_generales',
    'sre398': 'enfermeras_especializadas',
    'sre399': 'pasantes_enfermeria',
    'sre400': 'otras_enfermeras',
    'sre401': 'otro_personal_paramedico',
    'sre402': 'personal_administrativo',
    'sre403': 'otro_personal',
    'sre404': 'consultorios',
    'sre405': 'consultorios_generales',
    'sre406': 'consultorios_especialidad',
    'sre407': 'camas_censables',
    'sre408': 'camas_medicina_interna',
    'sre409': 'camas_cirugia',
    'sre410': 'camas_ginecoobstetricia',
    'sre411': 'camas_pediatria',
    'sre412': 'camas_otras',
    'sre413': 'camas_no_censables',
    'sre414': 'camas_cuidado_intensivo',
    'sre415': 'camas_cuidado_intermedio',
    'sre416': 'camas_no_censables_otras',
    'sre417': 'lab_analisis_clinicos',
    'sre418': 'lab_anatomia_patologica',
    'sre419': 'salas_radiologia',
    'sre420': 'equipos_rayos_x',
    'sre421': 'area_radioterapia',
    'sre422': 'equipos_radioterapia',
    'sre423': 'quirofanos',
    'sre424': 'salas_expulsion',
    'sre425': 'incubadoras',
    'sre426': 'cunas_rn',
    'sre427': 'area_pediatria',
    'sre428': 'area_urgencias',
    'sre429': 'area_aislamiento',
    'sre430': 'resonancia_magnetica',
    'sre431': 'equipo_dialisis',
    'sre432': 'hemodialisis',
    'sre433': 'mamografia',
    'sre434': 'ultrasonido',
    'sre435': 'electrocardiografo',
    'sre436': 'endoscopio',
    'sre437': 'electroencefalografo',
    'sre438': 'litotriptores',
    'sre439': 'tac_scanner',
    'sre440': 'bomba_cobalto',
    'sre441': 'bancos_sangre',
    'sre442': 'uci',
    'sre443': 'uci_adultos',
    'sre444': 'uci_neonatal',
    'sre445': 'unidades_dentales'
}

egresos_resources.rename(columns=rename_dict, inplace=True)
# print(egresos_resources.shape)

for key, value in combinations.items():
    egresos_resources[key] = egresos_resources[value].sum(axis=1)
    egresos_resources = egresos_resources.drop(columns=value)

# print(egresos_resources.shape) #!PASA

del_cols = [
    'lat_trunc_res', 'lon_trunc_res', 'nombre_unidad', 'latitud', 'longitud', 'clave_institucion',
    'lat_trunc', 'lon_trunc', 'nombre_institucion', 'anio', 'tipo_derechohabiente'
]
egresos_resources = egresos_resources.drop(columns=del_cols)

print(egresos_resources.shape)
print(egresos_resources.dtypes)
