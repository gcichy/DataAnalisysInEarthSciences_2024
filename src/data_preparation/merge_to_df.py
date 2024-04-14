import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import time
import zipfile
import sys
import select
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

def subset_stations(input_directory):
    '''
        In this function df with station codes is loaded. Data is processed, transformed to GeopandasDF, 
        joined to the GeopandasDF containing 'Województwa' and subset to contain only stations from 'podkarpackie'.
    '''
    try:
        stations = pd.read_csv(os.path.join(input_directory,'kody_stacji.csv'), encoding='cp1250',delimiter=';')
        stations.columns = ['LP.', 'ID', 'Nazwa', 'Rzeka', 'Szerokość geograficzna',
        'Długość geograficzna', 'Wysokość n.p.m.']

        stations = stations.apply(lambda row: _change_col_order(row),axis=1)

        stations['lon'] = stations.apply(lambda row: _convert_to_lon_lat(str(row['Długość geograficzna'])), axis=1)
        stations['lat'] = stations.apply(lambda row: _convert_to_lon_lat(str(row['Szerokość geograficzna'])), axis=1)
        
        stations = gpd.GeoDataFrame(stations, geometry=gpd.points_from_xy(stations['lon'], stations['lat']))
        
        stations.set_crs('EPSG:9702',inplace=True)
        
        woj = _get_regions(input_directory)
        
        joined = gpd.sjoin(stations, woj, op='within')
        stations_podkarp = joined[joined['JPT_NAZWA_'] == 'podkarpackie']
        
        stations_podkarp = stations_podkarp[['ID','Nazwa','Rzeka','Wysokość n.p.m.','geometry','JPT_NAZWA_']]
        stations_podkarp.columns = ['ID','Nazwa','Rzeka','Wysokość n.p.m.','geometry','Województwo']
    except Exception as e:
        raise Exception('Error caught while creating stations df (merge_to_df.py -> subset_stations()):' + str(e))
   
    
    return stations_podkarp
    
def merge_all_files(input_directory, stations):
    '''
        This function loads all source files, joins it with prefiltered stations,
        concat them into one big df and save in destination folder.
    '''
    try:
        files = os.listdir(input_directory)
        pattern = re.compile(r"o_d.+\.csv")

        matching_files = [element for element in files if pattern.match(element)]
        #file causing problems is skipped
        matching_files.remove('o_d_12_2023.csv')
        columns = ['Kod stacji','Nazwa stacji','Rok','Miesiąc','Dzień','Suma dobowa opadów [mm]','Status pomiaru SMDB','Rodzaj opadu [S/W/ ] ','Wysokość pokrywy śnieżnej [cm] ','Status pomiaru PKSN','Wysokość świeżospałego śniegu [cm] ','Status pomiaru HSS ','Gatunek śniegu[kod]','Status pomiaru GATS','Rodzaj pokrywy śnieżnej [kod]','Status pomiaru RPSN']
        df = pd.DataFrame(columns=columns + ['Rzeka','Wysokość n.p.m.','geometry','Województwo'])
        
        
        output_directory = os.path.join(os.path.dirname(__file__), '..','..','data','raw')
        for csv_file in matching_files:
            df_temp = pd.read_csv(os.path.join(input_directory, csv_file), encoding='cp1250', header=None, names=columns)
            df_temp = df_temp.merge(stations,left_on='Kod stacji',right_on='ID', how='inner')
            df_temp['Nazwa stacji'] = df_temp['Nazwa']
            del df_temp['ID']
            del df_temp['Nazwa']
            df = pd.concat([df,df_temp],axis=0)
            print(csv_file)

        #show unique station names
        print('Obszar analizy: Województwo Podkarpackie.\nLista stacji na obszarze analizy:\n')
        print(df['Nazwa stacji'].unique())
        
        #show min and max dates for each station
        df['date'] = pd.to_datetime(dict(year=df.Rok, month=df.Miesiąc, day=df.Dzień))
        print('\nZakresy pomiarów wg stacji:\n')
        print(df.groupby(by='Nazwa stacji')['date'].agg(['min','max']))
        
        #draw stations map
        stations_filt = stations[stations['Nazwa'].isin(df['Nazwa stacji'].unique())]
        draw_stations_map(input_directory,stations_filt)
        
        df.to_csv(os.path.join(output_directory,'merged_data.csv'), encoding='utf-8-sig', index=False)
        
    except Exception as e:
        raise Exception('Error caught while merging csv files (merge_to_df.py -> merge_all_files()):' + str(e))
        

def _change_col_order(row):
    pattern = r'^(\d\d ){2}.+$'
        
    if re.match(pattern,str(row['Rzeka'])):
        row['Wysokość n.p.m.'] = row['Długość geograficzna']
        row['Długość geograficzna'] = row['Szerokość geograficzna']
        row['Szerokość geograficzna'] = row['Rzeka']
        row['Rzeka'] = np.nan
    return row        
        
def _convert_to_lon_lat(coord):
    coord_tab = str(coord).split(' ')
    if len(coord_tab) == 2:
       res =float(coord_tab[0]) +  float(coord_tab[1])/60
    elif len(coord_tab) == 3:
       res = float(coord_tab[0]) +  float(coord_tab[1])/60 + float(coord_tab[2])/3600
    else:
        res = float(coord_tab[0])
    return res

def _get_regions(input_directory):
    path = os.path.join(input_directory, '..','..','data_to_upload','Wojewodztwa.shp')
    woj = gpd.read_file(path)
    return woj

def draw_stations_map(input_directory,stations):
    woj = _get_regions(input_directory)
    
    fig, ax = plt.subplots(figsize=(10, 10))

    woj[woj['JPT_NAZWA_'] == 'podkarpackie'].plot(ax=ax, color='blue', edgecolor='black')

    stations.plot(ax=ax, color='red', markersize=10)
    plt.title("Stations in Podkarpackie region map")
    plt.show()


    