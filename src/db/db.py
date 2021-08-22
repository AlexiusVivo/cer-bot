import pymongo as pm
import datetime
from pprint import pprint
import src.bot.config as config
import src.db.request as request


# Return collection
def get_cw_collection(collection_name):
    client = pm.MongoClient('localhost', 27017)
    db = client['rates']
    cw_collection = db[collection_name]
    return cw_collection


# Finding certain document in database
def find_document(collection, elements, multiple=False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def insert_document(collection, document):
    return collection.insert_one(document).inserted_id


def replace_rates(collection):
    """Updates rates document"""
    rates = request.requesting()
    new_values = {"$set": rates}
    collection.update_many({}, new_values)


def check_collection_exist(collection_name):
    client = pm.MongoClient('localhost', 27017)
    db = client['rates']
    collections_names = db.list_collection_names()
    return False if collection_name not in collections_names else True


def check_last_record_number(collection_name):
    coll = get_cw_collection(collection_name)
    if find_document(coll, {}) is None:
        return 0
    saved_record_number = int(find_document(coll, {})['record_saved'])
    return saved_record_number

def write_user_records(user_stats):
    collection_name = 'user_stats'
    coll = get_cw_collection(collection_name)
    coll.delete_one({'record_saved'})
    coll.insert_one(user_stats).inserted_id
    return


def get_current_month_and_requests(collection_name):
    coll = get_cw_collection(collection_name)
    if find_document(coll, {}) is None:
        return (0, 0)
    current_month = find_document(coll, {})['current_month']
    if current_month is None:
        current_month = 0
    month_requests_amount = find_document(coll, {})['records_in_this_months']
    if month_requests_amount is None:
        month_requests_amount = 0
    return (current_month, month_requests_amount)


# By giving original currency returns from database dict with rates of this currency to each other
def get_rate(original_currency):
    collection_name = 'currencies'
    coll = get_cw_collection(collection_name)
    return find_document(coll, {})[original_currency]


def init():
    coll = get_cw_collection('request_stats')
    if not check_collection_exist('request_stats') or coll.count_documents({}) == 0:
        current_date = datetime.datetime.utcnow()
        empty_record = {'total_request_id': config.INIT_REQUEST_ID, 'request_date': current_date, 'current_month_request_id': 0}
        pprint(empty_record)
        coll.insert_one(empty_record).inserted_id
    coll = get_cw_collection('currencies')
    if not check_collection_exist('currencies') or coll.count_documents({}) == 0:
        empty_record = {}
        coll.insert_one(empty_record).inserted_id
        replace_rates(coll)
