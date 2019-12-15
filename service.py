import redis
import copy
import config

REDIS_HOST = "localhost"#os.environ['REDIS_HOST']
REDIS_PORT = 6379#os.environ['REDIS_PORT']
REDIS_INDEX = 0#os.environ['REDIS_INDEX']
LIST_NAME = "company"#os.environ['LIST_NAME']


def get_company_suggestions(text):
    """Function to get company suggestions
    Arguments:
        text {[str]} -- starting text of company
    Returns:
        [list] -- [list of companies]
    """
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
    """Function to search company in redis and get its all parameters
    Arguments:
        text {[str]} -- company name
    Returns:
        [dict] -- company record
    """
    REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
    response = REDIS_CLIENT.hmget(text, config.OUTPUT_FIELDS)
    record = {}
    for _index in range(len(config.OUTPUT_FIELDS)):
        record[config.OUTPUT_FIELDS[_index]] = response[_index]
    return record

def get_sorted_company(key):
    """Function to get sorted company list based on given key
    Arguments:
        key {[str]} -- Sorting key
    Returns:
        [list] -- list of sorted record
    """
    REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_INDEX)
    key_list = config.OUTPUT_FIELDS
    key_list = ['*->'+key for key in key_list]
    if key == 'NAME':
        resp = REDIS_CLIENT.sort(LIST_NAME, desc=True, by="*->"+key, get=key_list, start=0, num=10, alpha=True)
    else:    
        resp = REDIS_CLIENT.sort(LIST_NAME, desc=True, by="*->"+key, get=key_list, start=0, num=10)
    sort_list = []
    count = 0
    record = {}
    for i in range(len(resp)):
        index = i%len(config.OUTPUT_FIELDS)
        field = config.OUTPUT_FIELDS[index]
        record[field] = resp[i]
        count += 1
        if count == len(config.OUTPUT_FIELDS):
            count = 0
            print (record)
            sort_list.append(copy.deepcopy(record))
            record = {}

    return sort_list