import config
import time


# By giving dict with rates from Euro to others currencies returns a dict with cartesian product with end structure:
# {final_currency: rate_to_original_currency, ...: ..., ...}
def cartesian_structure(eur_dict):
    conversion_dict = {}
    for currency in config.CURRENCY_CODES:
        conversion_dict[currency] = {}
        if currency == 'EUR':
            conversion_dict[currency] = eur_dict
            continue
        for currency_nested in config.CURRENCY_CODES:
            if currency_nested == 'EUR':
                conversion_dict[currency][currency_nested] = round(1 / eur_dict[currency], config.ROUND_ACCURACY)
            elif currency_nested == currency:
                conversion_dict[currency][currency_nested] = 1.0
            else:
                conversion_dict[currency][currency_nested] = round(1 / eur_dict[currency] * eur_dict[currency_nested],
                                                                   config.ROUND_ACCURACY)
    conversion_dict['timestamp'] = int(time.time())
    return conversion_dict
