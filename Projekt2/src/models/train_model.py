import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

def scale_data(data):
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def prepare_scaled_data(gdf):
    X_cols = ['main_roads_length', 'walks_length', 'dist_to_city_center[m]', 'building_count', 'green_space_area', 'service_point_count']
    y_col = 'bike_path_length'

    X = gdf[X_cols]
    y = gdf[y_col]

    X_train_, X_test_, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = scale_data(X_train_)
    X_test = scale_data(X_test_)

    return X_train, X_test, y_train, y_test

def train_RF_model(X_train, y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    return rf_model

def train_GBM_model(X_train, y_train):
    gbm_model = GradientBoostingRegressor(n_estimators=50, learning_rate=0.1, max_depth=3,
                                          min_samples_leaf=4, subsample=0.8, random_state=42)
    gbm_model.fit(X_train, y_train)

    return gbm_model