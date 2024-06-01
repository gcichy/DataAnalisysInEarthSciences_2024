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
from geopy.geocoders import Nominatim
import geopy
from shapely.geometry import Point
from geopy.distance import geodesic


def get_city_center_gdf(city_name):
    try:
         
        geolocator = Nominatim(user_agent="my-app")
        location = geolocator.geocode(city_name)
        if isinstance(location, geopy.location.Location):
            center_gdf = gpd.GeoDataFrame(geometry=[Point(location.longitude, location.latitude)],crs=4326) 
            return center_gdf
        
        print(f"Failed to get {city_name} center.")
        return None
        
    except Exception as e:
        print(f"Error in build_fetures.get_city_center_gdf: Failed to get {city_name} center: {e}")
        return None

def get_hex_dist_to_city_center(hex_gdf, center_gdf, epsg):
    try:
        old_epsg = hex_gdf.crs.to_epsg()
        center_gdf_proj = center_gdf.to_crs(epsg=epsg)
        hex_gdf = hex_gdf.to_crs(epsg=epsg)

        hex_gdf['dist_to_city_center[m]'] = hex_gdf.geometry.centroid.distance(center_gdf_proj.iloc[0,0])
        hex_gdf = hex_gdf.to_crs(epsg=old_epsg)
        return hex_gdf
    except Exception as e:
        raise Exception(f"Error in build_fetures.get_hex_dist_to_city_center: {e}")
    
def get_roads_and_walks_length_by_hex(hex_gdf, bbox, hex_area, epsg):
    try:
        G_roads = osmnx.graph_from_bbox(bbox=bbox, network_type='drive')
        G_walks = osmnx.graph_from_bbox(bbox=bbox, network_type='walk')

        # Convert the road network to a GeoDataFrame of edges
        gdf_walks = osmnx.graph_to_gdfs(G_walks, nodes=False)
        gdf_roads = osmnx.graph_to_gdfs(G_roads, nodes=False)
        
        gdf_roads['highway'].apply(lambda x: x[0] if isinstance(x, list) else x).unique()
        gdf_roads_main = gdf_roads[gdf_roads['highway'].isin(['secondary', 'primary', 'tertiary', 'busway',
            'motorway_link', 'motorway'])]
        
        gdf_roads_main_clipped = gdf_roads_main.geometry.clip(hex_area)
        gdf_walks_clipped = gdf_walks.geometry.clip(hex_area)
        
        old_epsg = hex_gdf.crs.to_epsg()
        hex_gdf = hex_gdf.to_crs(epsg=epsg)
        gdf_roads_main_clipped_proj = gdf_roads_main_clipped.to_crs(epsg=epsg)
        gdf_walks_clipped_proj = gdf_walks_clipped.to_crs(epsg=epsg)
        hex_gdf['main_roads_length'] = 0.0
        hex_gdf['walks_length'] = 0.0
        
        for i, polygon in hex_gdf.iterrows():
            clipped_r = gdf_roads_main_clipped_proj.clip(polygon.geometry)
            clipped_w = gdf_walks_clipped_proj.clip(polygon.geometry)
            hex_gdf.loc[i,'main_roads_length'] = clipped_r.length.sum()
            hex_gdf.loc[i,'walks_length'] = clipped_w.length.sum()

        hex_gdf = hex_gdf.to_crs(epsg=old_epsg)
        return hex_gdf
    except Exception as e:
        raise Exception(f"Error in build_fetures.get_roads_and_walks_length_by_hex: {e}")

    