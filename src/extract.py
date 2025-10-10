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
