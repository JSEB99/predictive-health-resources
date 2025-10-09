# Extract, download & organize necessary files

# Libraries
from bs4 import BeautifulSoup
import requests
import os
import shutil
import zipfile
import re
from tqdm import tqdm


def check_file(file_name: str):
    return file_name in os.listdir(output_dir)


def extract_file_name(url: str):
    base_url = url.split('?')[0]
    extension = base_url.split('.')[-1]
    match = re.search(rf'\/([^/]+)\.{extension}$', base_url)
    # if extension == 'zip':
    #     return match.group(1), extension
    return match.group(0), extension


def keep_required_files(files: list, output_dir):
    for nombre in os.listdir(output_dir):
        ruta_completa = os.path.join(output_dir, nombre)
        if nombre not in files:
            try:
                if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                    os.remove(ruta_completa)
                elif os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
                print(f'❌ Eliminado: {nombre}')
            except Exception as e:
                print(f'⚠️ No se pudo eliminar {nombre}: {e}')
        else:
            print(f'✅ Conservado: {nombre}')
# Variables


# print(extract_file_name(
#     'https://www.inegi.org.mx/contenidos/programas/salud/datosabiertos/conjunto_de_datos_esep_2024_csv.zip'))


output_dir = '../data/'
os.makedirs(output_dir, exist_ok=True)

output_files = [
    'AGEEML_20259251148648_utf.csv',
    'conjunto_de_datos_recursos_esep_2024',
    'egresos_hospitalarios_issste2024.csv',
    'egresos_resources.csv',
    'egresos_resources_final.csv',
    'ESTABLECIMIENTO_SALUD_202508.xlsx',
    'final_egres_res.csv'
]

urls = {
    'https://datos.gob.mx/dataset/datos_egresos_hospitalarios': {
        'element': 'a',
        'class': 'btn btn-outline-primary',
        'search_for': '2024',
        'extract': True,
    },
    'http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html': {
        'element': 'a',
        'class': None,
        'search_for': 'ESTABLECIMIENTO_SALUD',
        'extract': True
    },
    'https://www.inegi.org.mx/contenidos/programas/salud/datosabiertos/conjunto_de_datos_esep_2024_csv.zip': {
        'extract': False
    },
    'https://www.inegi.org.mx/contenidos/app/ageeml/min_con_acento_baja.zip': {
        'extract': False
    }
}

try:
    for key, values in urls.items():
        if values['extract']:
            content = requests.get(key)
            soup = BeautifulSoup(content.text, 'lxml')
            elements = soup.find_all(values['element'], class_=values['class'])
            for element in elements:
                hrefs = element.get('href', '')
                if values['search_for'] in hrefs:
                    print(
                        f'Enlace del archivo con "{values['search_for']}": {hrefs}')
                    break
        else:
            hrefs = key
        file, extension = extract_file_name(hrefs)
        if not check_file(file):
            response = requests.get(hrefs, stream=True)
            total = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            print(f'{response=}')
            with open(output_dir+file, 'wb') as f, tqdm(
                desc=file,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    bar.update(len(data))
        if extension == 'zip':
            print(output_dir+file)
            with zipfile.ZipFile(output_dir+file, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            print(f'Archivo {file} extraido satisfactoriamente')
    keep_required_files(output_files, output_dir)

except Exception as e:
    print(f'Ocurrió un error {e}')


# cont1 = requests.get(
#     'https://datos.gob.mx/dataset/datos_egresos_hospitalarios')
# cont2 = requests.get(
#     'http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html')
# cont3 = requests.get(
#     'http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html')

# if cont1.status_code == 200:
#     soup1 = BeautifulSoup(cont1.text, 'lxml')
#     link_btn = soup1.find_all('a', class_='btn btn-outline-primary')
#     for a in link_btn:
#         href = a.get('href', '')
#         if '2024' in href:
#             print('Enlace del archivo de egresos 2024:', href)
#             break
# else:
#     print('Ocurrio un error con el archivo (código de estado):', cont1.status_code)
# if cont2.status_code == 200:
#     soup2 = BeautifulSoup(cont2.text, 'lxml')
#     link_btn2 = soup2.find_all('a')
#     for a in link_btn2:
#         href = a.get('href', '')
#         if 'ESTABLECIMIENTO_SALUD' in href:
#             print('Enlace del archivo de establecimientos:', href)
#             break
# else:
#     print('Ocurrio un error con el archivo (código de estado):', cont2.status_code)
# if cont3.status_code == 200:
#     soup3 = BeautifulSoup(cont3.text, 'lxml')
#     link_btn3 = soup3.find_all('a')
#     for a in link_btn3:
#         href = a.get('href', '')
#         if 'ESTABLECIMIENTO_SALUD' in href:
#             print('Enlace del archivo de establecimientos:', href)
#             break
# else:
#     print('Ocurrio un error con el archivo (código de estado):', cont3.status_code)


# match = re.search(r'([^/]+)_csv\.zip$', urls[1])

# if match:
#     nombre_base = match.group(1)
#     print(nombre_base)  # → conjunto_de_datos_esep_2024
# else:
#     print('No se encontró coincidencia')
# # Nombre del archivo zip a guardar
# zip_path = nombre_base

# # Carpeta donde se extraerán los archivos
# extract_dir = nombre_base

# # Paso 1: Descargar el archivo
# print('Descargando ZIP...')
# response = requests.get(urls[1])

# if response.status_code == 200:
#     with open(zip_path, 'wb') as f:
#         f.write(response.content)
#     print(f'Archivo guardado como {zip_path}')
# else:
#     print(f'Error al descargar el archivo: {response.status_code}')
#     exit()

# # Paso 2: Extraer el ZIP
# print(f'Extrayendo archivos en {extract_dir}...')
# os.makedirs(extract_dir, exist_ok=True)

# with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#     zip_ref.extractall(extract_dir)

# print('Extracción completa ✅')
