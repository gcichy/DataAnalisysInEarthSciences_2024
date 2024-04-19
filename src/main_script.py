from data_preparation import get_external_data as ged
from data_preparation import merge_to_df as mrg
from data_transformation import get_raw_data as grd
from data_transformation import transform_data as td
from spi_calculations import get_processed_data as gpd
from spi_calculations import spi
import time


def main():
    try:
        # ged.get_external_data()

        input_dir = ged.get_input_dir()
        # ged.break_to_remove_zip_files(input_dir)

        #stations = mrg.subset_stations(input_dir)
        #mrg.merge_all_files(input_dir,stations)

        #raw_data_dir = grd.get_raw_data_dir()
        #td.transform_data(raw_data_dir)
        data = gpd.get_processed_data()
        spi_1 = spi.spi_1(data)
        spi_3 = spi.spi_3(data)
        spi_12 = spi.spi_12(data)



    except Exception as e:
        print('Error:' + str(e))


if __name__ == "__main__":
    main()
