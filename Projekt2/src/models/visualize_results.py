import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

def prepare_data_to_plot(gdf, predicted_data):
    data_to_plot = gdf[['geometry', 'bike_path_length']]
    data_to_plot.loc[:, 'predicted_bike_path_length'] = predicted_data

    return data_to_plot
def plot_results(gdf_to_plot, city_name):
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    gdf_to_plot.plot(column='bike_path_length', legend=True, ax=axes[0])
    axes[0].set_title(f'Bike path length in {city_name}')

    gdf_to_plot.plot(column='predicted_bike_path_length', legend=True, ax=axes[1])
    axes[1].set_title(f'Predicted bike path length in {city_name}')

    plt.show()