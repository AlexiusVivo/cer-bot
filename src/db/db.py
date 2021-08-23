import pymongo as pm
import datetime
from pprint import pprint
import src.bot.config as config
import src.db.request as request


def get_cw_collection(collection_name):
    """ Return collection"""
    client = pm.MongoClient('localhost', 27017)
    db = client['rates']
    cw_collection = db[collection_name]
    return cw_collection


def find_document(collection, elements, multiple=False):
    """ Finding certain document in database"""
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def insert_document(collection, document):
    """ Adding one document to collection"""
    return collection.insert_one(document).inserted_id


def replace_rates(collection):
    """Updates rates document"""
    rates = request.requesting()
    new_values = {"$set": rates}
    collection.update_many({}, new_values)


def check_collection_exist(collection_name):
    """ Check if collection exist in database """
    client = pm.MongoClient('localhost', 27017)
    db = client['rates']
    collections_names = db.list_collection_names()
    return False if collection_name not in collections_names else True


def check_last_record_number(collection_name):
    """ Check last number of record"""
    coll = get_cw_collection(collection_name)
    if find_document(coll, {}) is None:
        return 0
    saved_record_number = int(find_document(coll, {})['record_saved'])
    return saved_record_number


def get_rate(original_currency):
    """ By giving original currency returns from database dict with rates of this currency to each other"""
    collection_name = 'currencies'
    coll = get_cw_collection(collection_name)
    return find_document(coll, {})[original_currency]


def init():
    """ When bot starts, checking existing of collections and vice versa creating them with one sample record"""
    coll = get_cw_collection('request_stats')
    if not check_collection_exist('request_stats') or coll.count_documents({}) == 0:
        current_date = datetime.datetime.utcnow()
        empty_record = {'total_request_id': config.INIT_REQUEST_ID, 'request_date': current_date, 'current_month_request_id': 0}
        pprint(empty_record)
        coll.insert_one(empty_record).inserted_id
    coll = get_cw_collection('user_stats')
    if not check_collection_exist('user_stats') or coll.count_documents({}) == 0:
        current_date = datetime.datetime.utcnow()
        empty_record = {'total_request_id': config.INIT_REQUEST_USER_ID, 'request_date': current_date, 'current_month_request_id': 0, 'username': 'test', 'currencies': ['USD']}
        pprint(empty_record)
        coll.insert_one(empty_record).inserted_id
    coll = get_cw_collection('currencies')
    if not check_collection_exist('currencies') or coll.count_documents({}) == 0:
        empty_record = {}
        coll.insert_one(empty_record).inserted_id
        replace_rates(coll)
