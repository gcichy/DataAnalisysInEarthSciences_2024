import geopandas as gpd
import os


def save_gdf(gdf, file_name):
    try:
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
        full_path = os.path.join(path, file_name)

        gdf.to_parquet(full_path)
    except Exception as e:
        raise Exception(f"Error in save_geodataframe.save_gdf: {e}")
