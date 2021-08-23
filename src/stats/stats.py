import datetime
import src.db.db as db


def create_user_record(amount_and_currency, username, collection):
    """ Creating record of request successful to bot"""
    record = {}
    last_request = list(collection.find({}).sort('total_request_id', -1).limit(1))[0]
    current_date = datetime.datetime.utcnow()
    record['total_request_id'] = int(last_request['total_request_id']) + 1
    record['request_date'] = current_date
    record['username'] = username
    record['currencies'] = []
    for amount_with_currency in amount_and_currency:
        record['currencies'].append(amount_with_currency[1])
    return record


def create_request_record(collection):
    """ Creating record of request successful to API"""
    record = {}
    last_request = list(collection.find({}).sort('total_request_id', -1).limit(1))[0]
    current_date = datetime.datetime.utcnow()
    record['total_request_id'] = int(last_request['total_request_id']) + 1
    record['request_date'] = current_date
    record['current_month_request_id'] = 0
    return record


def update_user_stats(amount_and_currency, username):
    """ Updating user statistic by one new record about successful request to bot"""
    collection = db.get_cw_collection('user_stats')
    new_doc = create_user_record(amount_and_currency, username, collection)
    db.insert_document(collection, new_doc)


def update_request_stats():
    """ Updating user statistic by one new record about successful request to API"""
    collection = db.get_cw_collection('request_stats')
    new_doc = create_request_record(collection)
    db.insert_document(collection, new_doc)
