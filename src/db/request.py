import src.bot.config as config
import src.db.database_filler as database_filler
import src.stats.stats as stats
from src.exceptions import bot_exception
import json as js
import requests


def requesting():
    """ Making get-request for getting json with exchange rates for Euro"""
    response = requests.get(config.ENDPOINT, params=config.PAYLOAD_RATES)
    if response.status_code != 200:
        raise bot_exception.ApiException
    json = js.loads(response.text)
    conversion_dict = database_filler.cartesian_structure(json['rates'])
    stats.update_request_stats()
    return conversion_dict
