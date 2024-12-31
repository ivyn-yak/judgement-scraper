from pathlib import Path
import os
import requests
import re
from datetime import datetime

class CustomError(Exception):
    """Custom exception when the articles are more than a month old."""
    def __init__(self, message):
        super().__init__(message)

def get_date(text):
    index = text.find("Decision Date:")
    str_date = text[index+15:]
    date = datetime.strptime(str_date, "%d %b %Y").date()

    return date
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

