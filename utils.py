from pathlib import Path
import os
import requests

def create_directory(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)

def download_file(url, folder_name, file_name):
    folder_path = os.path.join("/Volumes/Untitled", folder_name)
    file_path = os.path.join(folder_path, file_name)
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
            print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download: {file_name} from {url}")

