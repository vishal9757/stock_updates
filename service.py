import redis
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
