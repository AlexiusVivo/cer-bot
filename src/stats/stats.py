import datetime

import src.db.db as db
from pprint import pprint
import pymongo
import time


def current_time():
    time_ = time.gmtime()
    return time_


def create_user_record(amount_and_currency, username):
    record = {}
    saved_record_number = db.check_last_record_number('user_stats')
    current_record_number = saved_record_number + 1
    # USER_STATISTIC['record_saved'] = current_record_number
    record[current_record_number] = {}
    record[current_record_number]['username'] = username
    record[current_record_number]['currencies'] = []
    for amount_with_currency in amount_and_currency:
        record[current_record_number]['currencies'].append(amount_with_currency[1])
    time_ = current_time()
    record[current_record_number]['message_time'] = f'{time_[3]}.{time_[4]}.{time_[5]} {time_[2]}.{time_[1]}.{time_[0]}'
    print(record)
    # return USER_STATISTIC.update(record)
    return

def create_request_record(collection):
    record = {}
    collection = db.get_cw_collection('request_stats')
    last_request = list(collection.find({}).sort('total_request_id', -1).limit(1))[0]
    current_date = datetime.datetime.utcnow()
    record['total_request_id'] = int(last_request['total_request_id']) + 1
    record['request_date'] = current_date
    record['current_month_request_id'] = 0
    return record


if __name__ == '__main__':
    print(current_time())


def update_request_stats():
    collection = db.get_cw_collection('request_stats')
    new_doc = create_request_record(collection)
    db.insert_document(collection, new_doc)