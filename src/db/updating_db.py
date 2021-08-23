import src.db.db as db


def update_rates():
    """ Updates exchange rates by certain time interval by CRON"""
    collection_name = 'currencies'
    coll = db.get_cw_collection(collection_name)
    db.replace_rates(coll)


if __name__ == '__main__':
    update_rates()