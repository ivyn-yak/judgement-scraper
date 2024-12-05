from pathlib import Path
import os
import requests
import re

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip().strip('.')
    return filename[:251] + ".pdf"

def create_directory(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)

def download_file(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
            print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download: {file_path} from {url}")

