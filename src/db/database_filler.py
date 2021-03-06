import src.bot.config as config


def cartesian_structure(eur_dict):
    """ By giving dict with rates from Euro to others currencies returns a dict with cartesian product with
     end structure: {final_currency: rate_to_original_currency, ...: ..., ...}"""
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
    return conversion_dict
