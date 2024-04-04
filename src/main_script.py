from data_preparation import get_external_data as ged
import time



def main():
    ged.get_external_data()
    
    input_dir = ged.get_input_dir()
    ged.break_to_remove_zip_files(input_dir)
    

if __name__ == "__main__":
    main()