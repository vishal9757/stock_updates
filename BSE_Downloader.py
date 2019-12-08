import requests, zipfile, StringIO
from datetime import datetime
import time
import pandas as pd
import DOWNLOAD_CONFIG

def get_date():
    ts = time.time()
    ts = ts - (24*60*60)
    date = datetime.utcfromtimestamp(ts).strftime('%d%m%y')
    return date

def download_file(url):
    response = requests.get(url, stream=True)
    zip = zipfile.ZipFile(StringIO.StringIO(response.content))
    zip.extractall()

def process_file(file_name):
    data_frame = pd.read_csv(file_name)
    return

def main():
    date = get_date()
    DOWNLOAD_URL = DOWNLOAD_CONFIG.BASE_URL+date+'_CSV.ZIP'
    download_file(DOWNLOAD_URL)
    FILE_NAME = 'EQ'+date+'.csv'
    process_file(FILE_NAME)
