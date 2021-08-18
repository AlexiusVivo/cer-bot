import config
import database_filler
import db
import requests
import json as js


# Making get-request for getting json with exchange rates for Euro
def requesting():
    response = requests.get(config.ENDPOINT, params=config.PAYLOAD_RATES)
    json = js.loads(response.text)
    conversion_dict = database_filler.cartesian_structure(json['rates'])
    return conversion_dict


# Converting dict with amount and currency to dict with structure {currency: {final_currency1: amount of original
# currency in final, final_currency2: ..., ...}}
def converter(amount_and_currency):
    converted_dict = {}
    for pare in amount_and_currency:
        converted_dict[pare[1]] = {}
        for rate in list(db.get_rate(pare[1]).items()):
            if rate[0] == pare[1]:
                converted_dict[pare[1]][rate[0]] = round(pare[0], config.ROUND_ACCURACY)
            else:
                converted_dict[pare[1]][rate[0]] = round(pare[0] * rate[1], config.ROUND_ACCURACY)
    return converted_dict


# Creating block of text for one of captured currencies
def currency_text_block(converted_currencies):
    emoji_dict = {'EUR': u'\U0001F1EA\U0001F1FA',
                  'USD': u'\U0001F1FA\U0001F1F8',
                  'GBP': u'\U0001F1EC\U0001F1E7',
                  'RUB': u'\U0001F1F7\U0001F1FA',
                  'UAH': u'\U0001F1FA\U0001F1E6',
                  'BYN': u'\U0001F1E7\U0001F1FE'}
    delimiter = '======\n'
    original_currency = converted_currencies[0]
    original_currency_with_amount = f'{emoji_dict[original_currency]}{converted_currencies[1][original_currency]} {original_currency}\n'
    text_block = f'{delimiter}{original_currency_with_amount}{delimiter}'
    for converted_currency in list(converted_currencies[1].items()):
        if converted_currency[0] == original_currency:
            continue
        else:
            text_converted_currency = f'{emoji_dict[converted_currency[0]]}{converted_currency[1]} {converted_currency[0]}\n'
            text_block += text_converted_currency
    return text_block


# Creating text of message
def get_reply_text(amount_and_currency):
    reply_text = ''
    converted_dict = converter(amount_and_currency)
    print(converted_dict)
    for converted_currencies in list(converted_dict.items()):
        reply_text += currency_text_block(converted_currencies)
    return reply_text
