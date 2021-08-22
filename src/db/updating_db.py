import src.db.db as db
import src.stats.stats as stats


def update_rates():
    collection_name = 'currencies'
    coll = db.get_cw_collection(collection_name)
    db.replace_rates(coll)


if __name__ == '__main__':
    update_rates()