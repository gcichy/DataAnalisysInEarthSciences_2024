from data_preparation import get_external_data as ged
from data_preparation import merge_to_df as mrg
import time



def main():
    try:
        #ged.get_external_data()
        
        input_dir = ged.get_input_dir()
        #ged.break_to_remove_zip_files(input_dir)
        
        stations = mrg.subset_stations(input_dir)
        mrg.merge_all_files(input_dir,stations)
        
    except Exception as e:
        print('Error:' + str(e))
        
if __name__ == "__main__":
    main()