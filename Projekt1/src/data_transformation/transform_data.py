import pandas as pd
import os
from scipy import stats
import matplotlib.pyplot as plt

def transform_data(raw_data_dir):
    try:
        csv_file = 'merged_data.csv'
        data = pd.read_csv(os.path.join(raw_data_dir, csv_file))

        data = data.drop(['Status pomiaru SMDB', 'Status pomiaru PKSN', 'Status pomiaru HSS ', 'Gatunek śniegu[kod]',
                          'Status pomiaru GATS', 'Rodzaj pokrywy śnieżnej [kod]', 'Status pomiaru RPSN', 'Rzeka'],
                         axis=1)
        data['Rodzaj opadu [S/W/ ] '].fillna('brak', inplace=True)
        data = pd.get_dummies(data, drop_first=True, columns=['Rodzaj opadu [S/W/ ] '])
        data['Suma dobowa opadów [mm]_boxcox'], lambda_ = stats.boxcox(data['Suma dobowa opadów [mm]'] + 1e-6)

        output_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
        draw_transformed_histogram(data['Suma dobowa opadów [mm]_boxcox'], lambda_)
        data.to_csv(os.path.join(output_directory, 'processed_data.csv'), encoding='utf-8-sig', index=False)
    except Exception as e:
        raise Exception('Error caught while transforming data (transform_data.py -> transform_data()):' + str(e))


def draw_transformed_histogram(data, lambda_):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.hist(data, bins=25, density=True, alpha=0.6, color='b', edgecolor='black')
    ax.set_title(f'Box-Cox transformed data, lambda = {lambda_}')
    ax.set_xlabel('Transformed value')
    ax.set_ylabel('Count')
    ax.grid()
    plt.show()
