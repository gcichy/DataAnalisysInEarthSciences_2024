from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from models.train_model import scale_data
def predict_model(model, test_data):
    return model.predict(test_data)

def calculate_metrics(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mse, rmse, mae, r2

def print_metrics(model_name, mse, rmse, mae, r2):
    print(f'{model_name} - Mean Squared Error (MSE): {mse}')
    print(f'{model_name} - Root Mean Squared Error (RMSE): {rmse}')
    print(f'{model_name} - Mean Absolute Error (MAE): {mae}')
    print(f'{model_name} - R^2 Score: {r2}')

def prepare_data_to_predict(gdf):
    X_cols = ['main_roads_length', 'walks_length', 'dist_to_city_center[m]', 'building_count', 'green_space_area',
              'service_point_count']
    y_col = 'bike_path_length'
    gdf_to_test = gdf[X_cols]

    return scale_data(gdf_to_test), gdf[y_col]



