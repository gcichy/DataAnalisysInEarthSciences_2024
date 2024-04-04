import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import time
import zipfile
import sys
import select

def get_input_dir():
    """
    Function gets location for external data to be stored in
    """
    return os.path.join(os.path.dirname(__file__), '..','..','data','external')

    
    
def _get_links(url, pattern):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    links = bs.find_all('a', href=True)
    
    return  [urljoin(url, link['href']) for link in links if re.match(pattern, link.text)]


def _process_file(file_url, input_directory):
    file_name = _extract_file_name(file_url)
    
    input_file_path = os.path.join(input_directory, file_name)
    _save_file(file_url, input_file_path)
    
    
    _unzip_and_delete_folder(input_file_path, input_directory)
    
    time.sleep(0.5)   


def _extract_file_name(url):
    file_name = url.split('/')
    return file_name[-1]


def _save_file(url, save_path):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Open a file at the specified path in binary write mode
            with open(save_path, "wb") as f:
                # Write the contents of the response to the file
                f.write(response.content)
                print(f'File {url} saved!')

        else:
            raise Exception(f"Failed to download file: {response.status_code}")
    except Exception as e:
        print(f'Failed to save file {url}\nError: {e}')
    
def _unzip_and_delete_folder(input_file_path, input_directory):
    try:
        with zipfile.ZipFile(input_file_path, 'r') as zip_ref:
            zip_ref.extractall(input_directory)
        
        os.remove(input_file_path)
    except Exception as e:
        print(f'Failed to uznip or remove file {input_file_path}\nError: {e}')



    
def get_external_data():
    """
    Function downloading prcipitation data from https://danepubliczne.imgw.pl.
    It utilizes all other functions created in this package.
    """
    try:
        input_directory = get_input_dir()

        url = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/'
        pattern = r'(199.+/|20.+/)'
        links = _get_links(url, pattern)
        for link in links:
            pattern = r'.*\.zip'
            zip_files = _get_links(link, pattern)
            print(zip_files)
            for file_url in zip_files:
                _process_file(file_url, input_directory)              
        
        stations_url = 'https://danepubliczne.imgw.pl/pl/datastore/getfiledown/Arch/Telemetria/Meteo/kody_stacji.csv'
        save_path =  os.path.join(input_directory, 'kody_stacji.csv')
        _save_file(stations_url, save_path)
    except Exception as e:
        print(f'Error caught in get_external_data package: {e}')   
        
        
def break_to_remove_zip_files(input_directory):
    
    has_zip_files = True
    regex = re.compile(r'.+\.zip')
    while has_zip_files:
        input(f'\nAby kontynuować rozpakuj (lub usuń jeśli rozpakowane) wszystkie pliki z rozszerzeniem .zip w folderze:\n{input_directory}\ni wciśnij enter\n')
        files = os.listdir(input_directory)
        
        if sum([1 if regex.search(f) else 0 for f in files]) == 0:
            has_zip_files = False
        
