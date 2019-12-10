import os
import redis
import requests, zipfile, StringIO
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import DOWNLOAD_CONFIG

REDIS_HOST = "localhost"#os.environ['REDIS_HOST']
REDIS_PORT = 6379#os.environ['REDIS_PORT']
REDIS_INDEX = 0#os.environ['REDIS_INDEX']
REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
LIST_NAME = "company"#os.environ['LIST_NAME']

def download_file(url):
    response = requests.get(url, stream=True)
    zip = zipfile.ZipFile(StringIO.StringIO(response.content))
    zip.extractall()

def process_record(doc):
    processed_record = {}
    for field in DOWNLOAD_CONFIG.EXTRACT_FIELDS:
        processed_record[field] = str(doc.get(field, '')).strip()
    processed_record["GAIN"] = ((float(processed_record["CLOSE"]) - float(processed_record['OPEN']))/float(processed_record['CLOSE']))*100
    return processed_record

def process_file(file_name):
    data_frame = pd.read_csv(file_name)
    REDIS_CLIENT.delete(LIST_NAME)
    for _index, row in data_frame.iterrows():
        row = row.to_dict()
        processed_record = process_record(row)
        name =row.get('SC_NAME', '').strip()
        REDIS_CLIENT.sadd(LIST_NAME, name)
        REDIS_CLIENT.hmset(name, processed_record)

def get_download_url():
    try:
        resp = requests.get(DOWNLOAD_CONFIG.BASE_URL).text
        soup = BeautifulSoup(resp, features="html.parser")
        file_url = soup.find('a', id="ContentPlaceHolder1_btnhylZip")
        file_url = file_url.get('href')
        return file_url
    except:
        return ""

def get_file_name(url):
    try:
        file_name = url.split('/')[-1].replace('.ZIP','').replace('_CSV', '.CSV')
        return file_name
    except:
        return ""

def main():
    url = get_download_url()
    if url:
        download_file(url)
        file_name = get_file_name(url)
        process_file(file_name)

if __name__ == '__main__':
    main()