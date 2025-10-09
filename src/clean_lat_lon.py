import pandas as pd

lat_lon_places = pd.read_csv(
    '../data/AGEEML_20259251148648_utf.csv', low_memory=False)
lat_lon_places = lat_lon_places.drop(
    columns=['LATITUD', 'LONGITUD'], errors='ignore')
lat_lon_places.to_csv('../data/AGEEML_20259251148648_utf.csv', index=False)
