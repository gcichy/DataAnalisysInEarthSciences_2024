import numpy as np
import pandas as pd
import scipy as sp
import os
# from spi_calculations import get_processed_data as gpd

def spi_1(df):
    grouped_data = df.groupby(['Rok', 'Miesiąc']).agg({'Suma dobowa opadów [mm]': 'sum'})
    alpha, loc, beta = sp.stats.gamma.fit(grouped_data, floc = 0)
    cdf = sp.stats.gamma.cdf(grouped_data, alpha, loc = loc, scale = beta)
    spi_value_1 = sp.stats.norm.ppf(cdf)
    grouped_data['spi1'] = spi_value_1
    output_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
    grouped_data.reset_index().to_csv(os.path.join(output_directory, 'spi_value_1.csv'), encoding='utf-8-sig', index=False)

# df = gpd.get_processed_data()
# print(spi_1(df))

def spi_3(df):
    grouped_data = df.groupby(['Rok', 'Miesiąc']).agg({'Suma dobowa opadów [mm]': 'sum'})
    if(len(grouped_data) < 3):
        raise ValueError("Data is shorter than 3 months")
    three_months_sum = []
    for i in range(2, len(grouped_data)):
        three_months_sum.append(grouped_data.iloc[i-2:i+1].sum())
    alpha, loc, beta = sp.stats.gamma.fit(three_months_sum, floc = 0)
    cdf = sp.stats.gamma.cdf(three_months_sum, alpha, loc = loc, scale = beta)
    spi_value_3 = sp.stats.norm.ppf(cdf)
    spi_value_3 = np.insert(spi_value_3,0, [np.nan, np.nan]) #zrobione ze wzgledu na fakt, że dla pierwszego roku w danych nie można dla stycznia oraz lutego wziąć trzech poprzednich miesięcy
    grouped_data['spi3'] = spi_value_3
    output_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
    # draw_transformed_histogram(data['Suma dobowa opadów [mm]_boxcox'], lambda_)
    grouped_data.reset_index().to_csv(os.path.join(output_directory, 'spi_value_3.csv'), encoding='utf-8-sig', index=False)

# df = gpd.get_processed_data()
# print(spi_3(df))


def spi_12(df):
    grouped_data = df.groupby(['Rok', 'Miesiąc']).agg({'Suma dobowa opadów [mm]': 'sum'})
    if(len(grouped_data) < 12):
        raise ValueError("Data is shorter than 12 months")
    twelve_months_sum = []
    for i in range(11, len(grouped_data)):
        twelve_months_sum.append(grouped_data.iloc[i-11:i+1].sum())
    alpha, loc, beta = sp.stats.gamma.fit(twelve_months_sum, floc = 0)
    cdf = sp.stats.gamma.cdf(twelve_months_sum, alpha, loc = loc, scale = beta)
    spi_value_12 = sp.stats.norm.ppf(cdf)
    spi_value_12 = np.insert(spi_value_12,0, 11*[np.nan]) #zrobione ze wzgledu na fakt, że dla pierwszego roku w danych nie można dla miesięcy od stycznia do listopada wziąć 11 poprzednich miesięcy
    grouped_data['spi12'] = spi_value_12
    output_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
    # draw_transformed_histogram(data['Suma dobowa opadów [mm]_boxcox'], lambda_)
    grouped_data.reset_index().to_csv(os.path.join(output_directory, 'spi_value_12.csv'), encoding='utf-8-sig', index=False)
# df = gpd.get_processed_data()

