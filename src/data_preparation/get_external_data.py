import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random as rand
import re
import os
import time
import zipfile

def get_input_dir():
    directory_path = input('Choose input path for source files:')
 
    if not os.path.exists(directory_path):
        raise Exception("Error loading exgternal data: Provided path doesn't exist")
    
    os.chmod(directory_path, 0o700)
    
    return directory_path
    
    
def get_links(url, pattern):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    links = bs.find_all('a', href=True)
    
    return  [urljoin(url, link['href']) for link in links if re.match(pattern, link.text)]


def process_file(file_url, input_directory):
    file_name = extract_file_name(file_url)
    
    input_file_path = input_directory + '/' + file_name
    save_file(file_url, input_file_path)
    
    unzip_and_delete_folder(input_file_path, input_directory)
    
    time.sleep(0.5)   


def extract_file_name(url):
    file_name = url.split('/')
    return file_name[-1]


def save_file(url, save_path):
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
    
def unzip_and_delete_folder(input_file_path, input_directory):
    try:
        with zipfile.ZipFile(input_file_path, 'r') as zip_ref:
            zip_ref.extractall(input_directory)
        
        os.remove(input_file_path)
    except Exception as e:
        print(f'Failed to uznip or remove file {input_file_path}\nError: {e}')



    

def main():
    try:
        input_directory = get_input_dir()

        url = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/'
        pattern = r'(199.+/|20.+/)'
        links = get_links(url, pattern)
        for link in links:
            pattern = r'.*\.zip'
            zip_files = get_links(link, pattern)
            print(zip_files)
            for file_url in zip_files:
                process_file(file_url, input_directory)              
        
        stations_url = 'https://danepubliczne.imgw.pl/pl/datastore/getfiledown/Arch/Telemetria/Meteo/kody_stacji.csv'
        save_path = input_directory + '/' + 'kody_stacji.csv'
        save_file(stations_url, save_path)
    except Exception as e:
        print(f'Error caught: {e}')
        
          
if __name__ == "__main__":
 main()