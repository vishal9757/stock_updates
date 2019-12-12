import redis
import copy
import DOWNLOAD_CONFIG

REDIS_HOST = "localhost"#os.environ['REDIS_HOST']
REDIS_PORT = 6379#os.environ['REDIS_PORT']
REDIS_INDEX = 0#os.environ['REDIS_INDEX']
LIST_NAME = "company"#os.environ['LIST_NAME']


def get_company_suggestions(text):
    REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
    resp = REDIS_CLIENT.sscan(LIST_NAME, cursor=0, match=text+"*")
    result = []
    cursor = resp[0]
    result.extend(resp[1])
    while cursor != 0:
        resp = REDIS_CLIENT.sscan(LIST_NAME, cursor=cursor, match=text+"*")
        cursor = resp[0]
        result.extend(resp[1])
    result.sort()
    return result

def get_company_stats(text):
    REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
    response = REDIS_CLIENT.hmget(text, DOWNLOAD_CONFIG.EXTRACT_FIELDS)
    record = {}
    for _index in range(len(DOWNLOAD_CONFIG.EXTRACT_FIELDS)):
        record[DOWNLOAD_CONFIG.EXTRACT_FIELDS[_index]] = response[_index]
    return record

def get_sorted_company():
    REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
    key_list = DOWNLOAD_CONFIG.EXTRACT_FIELDS
    key_list = ['*->'+key for key in key_list]
    resp = REDIS_CLIENT.sort(LIST_NAME, desc=False, by="*->"+DOWNLOAD_CONFIG.SORT_KEY, get=key_list, start=0, num=10)
    sort_list = []
    count = 0
    record = {}
    for i in range(len(resp)):
        index = i%len(DOWNLOAD_CONFIG.EXTRACT_FIELDS)
        field = DOWNLOAD_CONFIG.EXTRACT_FIELDS[index]
        record[field] = resp[i]
        count += 1
        if count == len(DOWNLOAD_CONFIG.EXTRACT_FIELDS):
            count = 0
            print (record)
            sort_list.append(copy.deepcopy(record))
            record = {}

    return sort_list