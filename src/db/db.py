import pymongo as pm
import time
import src.bot.config as config
import src.convert.exchanging as exchanging


# Return collection
def get_cw_collection():
    client = pm.MongoClient('localhost', 27017)
    db = client['rates']
    cw_collection = db['currencies']
    return cw_collection


# Finding certain document in database
def find_document(collection, elements, multiple=False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


# Updates rates document
def replace_rates(collection):
    rates = exchanging.request.requesting()
    collection.delete_many({})
    return collection.insert_one(rates).inserted_id


# Checking how a long database was updated, 86400 - one day in seconds, 43200 - 12 hours, 3600 - 1 hour
def check_timestamp(collection):
    return True if int(time.time()) - config.UPDATE_DB_TIMEOUT >= int(find_document(collection, {})['timestamp']) else False


# By giving original currency returns from database dict with rates of this currency to each other
def get_rate(original_currency):
    coll = get_cw_collection()
    if check_timestamp(coll):
        replace_rates(coll)
        coll = get_cw_collection()
    return find_document(coll, {})[original_currency]
