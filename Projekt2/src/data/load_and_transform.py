import numpy as np
import h3
import pandas as pd
import os
import geopandas as gpd
import re
import shapely.wkb as swkb
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import osmnx

def load_raw_files():  
    try:
        path = os.path.join(os.path.dirname(__file__),'..','..','data','external')
        files = os.listdir(path)
        pattern = '.+parquet'
        source_files = []
        for file in files:
            if re.match(pattern, file):
                df = pd.read_parquet(os.path.join(path,file))
                source_files.append(df)
        return source_files
    except Exception as e:
        raise Exception(f"Error in load_and_transform.load_raw_files: {e}")


def extract_features(series):
    try:
        dict_of_lists = {}
        for d in series:
            for key, value in d.items():
                dict_of_lists.setdefault(key, []).append(value)
            
        return pd.DataFrame(data=dict_of_lists)
    except Exception as e:
        raise Exception(f"Error in load_and_transform.extract_features: {e}")

def create_gdf(df,epsg):
    try:
        df['geometry'] = df['geometry'].apply(lambda x: swkb.loads(x, hex = True))
        gdf = gpd.GeoDataFrame(data=df, geometry='geometry')
        gdf = gdf.set_crs(epsg=epsg)
        return gdf
    except Exception as e:
        raise Exception(f"Error in load_and_transform.create_gdf: {e}")

def get_boundary_coord(row, func, which):
    x, y = zip(*row.coords)
    return func(x) if which == 'x' else func(y)


def create_h3_grid(df, epsg=4326):
    try:
        buffer = 0.01
        max_x = max(df['geometry'].apply(lambda row: get_boundary_coord(row, max, 'x'))) + buffer
        min_x = min(df['geometry'].apply(lambda row: get_boundary_coord(row, min, 'x'))) - buffer
        max_y = max(df['geometry'].apply(lambda row: get_boundary_coord(row, max, 'y'))) + buffer
        min_y = min(df['geometry'].apply(lambda row: get_boundary_coord(row, min, 'y'))) - buffer
        
        geo = {
            'type': 'Polygon',
            'coordinates': [
                [
                    [min_x, min_y],
                    [min_x, max_y],
                    [max_x, max_y],
                    [max_x, min_y]
                ]
            ]
        }

        hexes = h3.polyfill(geo, 8)
        hex_polygons = [Polygon(h3.h3_to_geo_boundary(h3_index)) for h3_index in hexes]

        gdf_pol = gpd.GeoDataFrame(geometry=hex_polygons)
        gdf_pol = gdf_pol.set_crs(epsg=epsg)
        return gdf_pol, (max_y, min_y,max_x, min_x)
    except Exception as e:
        raise Exception(f"Error in load_and_transform.create_h3_grid: {e}")


def crop_grid(hex_gdf, bikepath_gdf, area_gdf, epsg):
    try:
        bikepath_gdf_proj = bikepath_gdf.to_crs(epsg=epsg)
        old_epsg = hex_gdf.crs.to_epsg()
        hex_gdf = hex_gdf.to_crs(epsg=epsg)
        area_gdf_proj = area_gdf.to_crs(epsg=epsg)
        hex_gdf['bike_path_length'] = 0.0
        hex_gdf['within_city'] = False

        for i, polygon in hex_gdf.iterrows():
            clipped = bikepath_gdf_proj.clip(polygon.geometry)
            within_city = polygon.geometry.intersects(area_gdf_proj.geometry)
            hex_gdf.loc[i,'bike_path_length'] = clipped.length.sum()
            hex_gdf.loc[i,'within_city'] = within_city[0]

        hex_gdf = hex_gdf[(hex_gdf['within_city'] == True) | (hex_gdf['bike_path_length'] > 0)]
        hex_gdf = hex_gdf.to_crs(epsg=old_epsg)
        del hex_gdf['within_city']
        return hex_gdf
    except Exception as e:
        raise Exception(f"Error in load_and_transform.crop_grid: {e}")

