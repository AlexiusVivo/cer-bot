import src.bot.config as config
import src.db.database_filler as database_filler
import json as js
import requests


# Making get-request for getting json with exchange rates for Euro
def requesting():
    response = requests.get(config.ENDPOINT, params=config.PAYLOAD_RATES)
    json = js.loads(response.text)
    conversion_dict = database_filler.cartesian_structure(json['rates'])
    return conversion_dict