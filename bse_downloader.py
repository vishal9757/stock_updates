import os
import redis
import requests
import zipfile
from io import BytesIO
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import config

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_INDEX = int(os.environ['REDIS_INDEX'])
REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
LIST_NAME = os.environ['LIST_NAME']


def download_file(url):
    """
    Function to download file from given url
    Arguments:
        url {[str]} -- url from where file has to be downloaded
    """
    response = requests.get(url, stream=True)
    zip = zipfile.ZipFile(BytesIO(response.content))
    zip.extractall()

def get_date(file_name):
    """Function to extract date from file name
    Arguments:
        file_name {[str]} -- File name
    Returns:
        [str] -- Date
    """
    file_name = file_name.replace('EQ','').replace('.CSV','')
    date = "{0}/{1}/{2}".format(file_name[:2], file_name[2:4], file_name[4:])
    return date

def process_record(doc):
    """Function to process document get required fields and calculate gain
    Arguments:
        doc {[dict]} -- raw record of csv file
    Returns:
        [dict] -- processed document
    """
    processed_record = {}
    for field in config.EXTRACT_FIELDS:
        new_field = config.FIELD_MAP.get(field, field)
        processed_record[new_field] = str(doc.get(field, '')).strip()
    processed_record["GAIN"] = ((float(processed_record["CLOSE"]) - float(
        processed_record['OPEN'])) / float(processed_record['CLOSE'])) * 100
    return processed_record


def process_file(file_name):
    """Function to process file
    Arguments:
        file_name {[str]} -- File name that has to be processed
    """
    data_frame = pd.read_csv(file_name)
    REDIS_CLIENT.delete(LIST_NAME)
    for _index, row in data_frame.iterrows():
        row = row.to_dict()
        processed_record = process_record(row)
        name = row.get('SC_NAME', '').strip()
        print (name)
        REDIS_CLIENT.sadd(LIST_NAME, name)
        REDIS_CLIENT.hmset(name, processed_record)
    file_date = get_date(file_name)
    REDIS_CLIENT.set("last_updated_date", file_date)

def get_download_url():
    """Function to get download url from homepage
    Arguments:
        None
    Returns:
        [str] -- Downloadable url
    """
    resp = requests.get(config.BASE_URL).text
    soup = BeautifulSoup(resp, features="html.parser")
    file_url = soup.find('a', id="ContentPlaceHolder1_btnhylZip")
    file_url = file_url.get('href')
    return file_url


def get_file_name(url):
    """Function to get file name from url
    Arguments:
        url {[str]} -- Url from where file is downloaded
    Returns:
        [str] -- file name
    """
    file_name = url.split('/')[-1].replace('.ZIP', '').replace('_CSV', '.CSV')
    return file_name


def main():
    """Main Function
    Arguments:
        None
    """
    url = get_download_url()
    if url:
        download_file(url)
        file_name = get_file_name(url)
        process_file(file_name)


if __name__ == '__main__':
    main()
