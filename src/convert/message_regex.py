import regex as re
import src.bot.config as config


def get_modifiers(position, lenght):
    """ This function check what distance of search doesn't go beyond the index range"""
    modifiers = {'0': 0, '-1': -1, '-2': -2, '+1': 1, '+2': 2}
    outlimit_before = position - config.MAX_DISTANCE if position - config.MAX_DISTANCE < 0 else 0
    outlimit_after = position + config.MAX_DISTANCE - (lenght - 1) if position + config.MAX_DISTANCE > (
            lenght - 1) else 0
    if outlimit_before < 0:
        modifiers.pop('-2')
        if outlimit_before == -2:
            modifiers.pop('-1')
    elif outlimit_after > 0:
        modifiers.pop('+2')
        if outlimit_after == 2:
            modifiers.pop('+1')
    return modifiers


def kilo_search(modifiers, position, splited_string):
    """ Search around found amount multiplier of 1000 (k-symbol)"""
    kilo_result = 0
    for modifier in list(modifiers.values()):
        pattern_kilo = r'(?<=\d+\.?\d+?)?[kKкК]+$|^[kKкК]+$'
        if position + modifier not in range(len(splited_string)):
            continue
        substring = splited_string[position + modifier]
        kilo = re.search(pattern_kilo, substring)
        # print(substring)
        if kilo is None:
            continue
        kilo = kilo.group()
        kilo_count = len(kilo)
        if kilo_count > 4:
            kilo_count = 4
        kilo_result = 1000 ** kilo_count
    return kilo_result if kilo_result != 0 else False


def splitting_string(string):
    """ Divide the text of message to 'tokens' """
    splited_string = list(filter(lambda empty_element: empty_element != '', re.split(r'\s+', string)))
    return splited_string if len(splited_string) != 0 else False


def currency_check(splited_string):
    """ Checks if in splited regex by space symbols exists symbol or pattern of currency"""
    success = []
    currencies = []
    pattern_dict = {
        'EUR': u'\u20AC|€|eur|EUR|Eur|евро|еуро|евра',
        'USD': r'usd|dollar|\$|доллар|даляр|бакс|бачей|вечнозел',
        'GBP': u'£|\u00A3|pound|фунт',
        'RUB': u'₽|\u20BD|rub|рубл|руб|деревян|^р$|^р\.$',
        'UAH': u'₴|\u20B4|гривен|грн|uah|hrivn',
        'BYN': 'byn|byr|бел|зайч|зайц'
    }
    for index in range(len(splited_string)):
        result = re.search(r'(?<=\d+[,\.]?\d+?[kKкК]+?)?([^,\.0-9]+)', splited_string[index])
        if result is None:
            continue
        result = result.group()
        success.append(result)
        substring = result.lower()
        for pattern in list(pattern_dict.items()):
            currency_string = re.match(pattern[1], substring)
            if currency_string is not None:
                currencies.append((index, pattern[0]))
    return currencies if len(currencies) != 0 else False


def amount_check(currencies, splited_string):
    """Returns amount of original currency"""
    amount_and_currencies = []
    pattern_digit_amount = r'\d+[,\.]?\d*?'
    for currency in currencies:
        modifiers = get_modifiers(currency[0], len(splited_string))
        for modifier in list(modifiers.values()):
            if currency[0] + modifier not in range(len(splited_string)):
                continue
            substring = splited_string[currency[0] + modifier]
            result = re.search(pattern_digit_amount, substring)
            if result is None:
                continue
            result = result.group()
            if ',' in result:
                result = re.sub(',', '.', result)
            result = float(result)
            kilo = kilo_search(modifiers, currency[0], splited_string)
            if kilo:
                result = result * kilo
            amount_and_currencies.append((result, currency[1]))
            break
    return amount_and_currencies if len(amount_and_currencies) != 0 else False


def scan_text(string):
    """ Start scanning text through 2 patterns and returns list of found pares amount-original_currency,
    if one of them don't find anything - returns False"""
    splited_string = splitting_string(string)
    if not splited_string:
        return False
    currencies = currency_check(splited_string)
    if not currencies:
        return False
    amount_and_currencies = amount_check(currencies, splited_string)
    if not amount_and_currencies:
        return False
    return amount_and_currencies
