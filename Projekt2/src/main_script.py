from data import load_and_transform as lt
from features import build_features as bf
from shapely.ops import unary_union
import time
import pandas as pd
import osmnx
import geopandas as gpd
from data import save_geodataframe as sg
from models import train_model as tm
from models import predict_model as pm
from models import visualize_results as vr

def main():
    try:
        if not lt.processed_data_exists():

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

            # CALCULATE BUILDING POINTS
            gdf_ams_pol = bf.calculate_building_points(gdf_ams_pol)
            gdf_krk_pol = bf.calculate_building_points(gdf_krk_pol)

            # CALCULATE GREEN SPACE AREA
            gdf_ams_pol = bf.get_green_space_by_hex(gdf_ams_pol, bbox_ams, AMS_PROJ_EPSG)
            gdf_krk_pol = bf.get_green_space_by_hex(gdf_krk_pol, bbox_krk, KRK_PROJ_EPSG)

            # CALCULATE SERVICE POINTS
            gdf_ams_pol = bf.get_service_points_by_hex(gdf_ams_pol, bbox_ams, hex_area_ams, AMS_PROJ_EPSG)
            gdf_krk_pol = bf.get_service_points_by_hex(gdf_krk_pol, bbox_krk, hex_area_krk, KRK_PROJ_EPSG)

            print(gdf_ams_pol)
            print(gdf_krk_pol)

            sg.save_gdf(gdf_ams_pol, 'gdf_ams.parquet')
            sg.save_gdf(gdf_krk_pol, 'gdf_krk.parquet')
        else:
            gdf_ams_pol = lt.load_processed_data('gdf_ams.parquet')
            gdf_krk_pol = lt.load_processed_data('gdf_krk.parquet')

        X_train, X_test, y_train, y_test = tm.prepare_scaled_data(gdf_ams_pol)
        model = tm.train_RF_model(X_train, y_train)
        y_pred = pm.predict_model(model, X_test)
        mse, rmse, mae, r2 = pm.calculate_metrics(y_test, y_pred)
        pm.print_metrics('Random Forest Regressor', mse, rmse, mae, r2)

        X_krk_test, y_krk_test = pm.prepare_data_to_predict(gdf_krk_pol)
        y_krk_pred = pm.predict_model(model, X_krk_test)
        mse, rmse, mae, r2 = pm.calculate_metrics(y_krk_test, y_krk_pred)
        pm.print_metrics('Random Forest Regressor for Krakow', mse, rmse, mae, r2)
        data_to_plot_krk = vr.prepare_data_to_plot(gdf_krk_pol, y_krk_pred)
        vr.plot_results(data_to_plot_krk, 'Kraków')

        
    except Exception as e:
        print('Error:' + str(e))


if __name__ == "__main__":
    main()