from data import load_and_transform as lt
from features import build_features as bf
from shapely.ops import unary_union
import time
import pandas as pd
import osmnx
import geopandas as gpd

def main():
    try:
        EPSG = 4326
        AMS_PROJ_EPSG = 28992
        KRK_PROJ_EPSG = 2180
        
        # LOAD BIKEPATHS DATA AND CONVERT IT TO GDF
        data = lt.load_raw_files()
        df_ams = data[0]
        df_krk = data[1]

        gdf_ams = lt.create_gdf(df_ams,EPSG)
        gdf_krk = lt.create_gdf(df_krk,EPSG)
        
        # CREATE H3 GRID AND GET ITS MAX/MIN LON/LAT
        gdf_krk_pol, bbox_krk = lt.create_h3_grid(gdf_krk)
        gdf_ams_pol, bbox_ams = lt.create_h3_grid(gdf_ams)
        
        # GET GDF WITH POLYGON OF CITY AREA
        ams_area = osmnx.geocode_to_gdf("Amsterdam")
        krk_area = osmnx.geocode_to_gdf("Kraków")

        # CROP GRID TO CITY BOUNDARIES AND CALCULATE SUMMED LENGTH OF BIKEPATHS
        gdf_ams_pol = lt.crop_grid(gdf_ams_pol, gdf_ams, ams_area, AMS_PROJ_EPSG)
        gdf_krk_pol = lt.crop_grid(gdf_krk_pol, gdf_krk, krk_area, KRK_PROJ_EPSG)
        print('H3 grids cropped')
        

        ######################################################################################################
        #FEATURE ENGINEERING
        
        # GET POLYGON OF CROPPED HEX GRID
        hex_area_ams = unary_union(gdf_ams_pol.geometry) 
        hex_area_krk = unary_union(gdf_krk_pol.geometry)
        
        # GET SUMMED LENGTH OF MAIN ROADS AND WALKS
        gdf_ams_pol = bf.get_roads_and_walks_length_by_hex(gdf_ams_pol, bbox_ams, hex_area_ams, AMS_PROJ_EPSG)
        gdf_krk_pol = bf.get_roads_and_walks_length_by_hex(gdf_krk_pol, bbox_krk, hex_area_krk, KRK_PROJ_EPSG)
        print('Roads distance and walks distance features added')
        
        # GET GDF WITH CITY CENTER POINT
        gdf_center_ams = bf.get_city_center_gdf('Amsterdam')
        gdf_center_krk = bf.get_city_center_gdf('Krakow')
        
        # GET DISTANCE FROM HEX TO CITY CENTER
        gdf_ams_pol = bf.get_hex_dist_to_city_center(gdf_ams_pol, gdf_center_ams, AMS_PROJ_EPSG)
        gdf_krk_pol = bf.get_hex_dist_to_city_center(gdf_krk_pol, gdf_center_krk, KRK_PROJ_EPSG)
        print('Distance to city center feature added')
                                                  
        print(gdf_ams_pol)
        print(gdf_krk_pol)
        
    except Exception as e:
        print('Error:' + str(e))


if __name__ == "__main__":
    main()