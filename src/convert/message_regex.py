import regex as re


# Check if exists places in original message like: text digit, digit text, digit currency_symbol, float_digit text, etc.
def location_check(string):
    currency_symbols = r'\$₴£€₽'
    pattern = rf'(?<=^|\s+)\d+\.?,?\d*\s+?\w+(?=$|\s)|(?<=^|\s+)\w+\s+?\d+\.?,?\d*(?=$|\s)|(?<=^|\s+)\d+\.?,?\d*\s*[{currency_symbols}](?=$|\s+)|(?<=^|\s+)[{currency_symbols}]\s*\d+\.?,?\d*(?=$|\s+)'
    search_result = re.findall(pattern, string, overlapped=True)
    return search_result if len(search_result) > 0 else False


# Returns amount of original currency
def get_amount(string):
    pattern_amount = r'\d+\.?,?\d*'
    amount = re.search(pattern_amount, string).group()
    if ',' in amount:
        amount = re.sub(',', '.', amount)
    amount = float(amount)
    return amount


# Checks if in result of first checking exists symbol or pattern of currency
def currency_check(search_result):
    amount_and_currency = []
    pattern_dict = {
        'EUR': 'eur|EUR|Eur|€|евро|еуро|евра',
        'USD': r'usd|dollar|\$|доллар|даляр|бакс|бачей|вечнозел|долар',
        'GBP': '£|pound|фунт',
        'RUB': '₽|rub|рубл|руб|деревян',
        'UAH': '₴|гривн|грв|грн|uah|hrivn|гривен',
        'BYN': 'byn|byr|бел|зайч|зайц'
    }
    for string in search_result:
        pattern_word = r'[^\d\s\.,]+'
        word_regex = re.search(pattern_word, string)
        if word_regex is not None:
            word = word_regex.group().lower()
            for pattern in list(pattern_dict.items()):
                currency_string = re.search(pattern[1], word)
                if currency_string is not None and word.startswith(currency_string.group()):
                    currency_ = pattern[0]
                    amount = get_amount(string)
                    amount_and_currency.append([amount, currency_])
        else:
            return False
    return amount_and_currency if len(amount_and_currency) != 0 else False


# Start scanning text through 2 patterns and returns list of found pares amount-original_currency
# , if one of them don't find anything - returns False
def scan_text(message_text):
    first_check = location_check(message_text)
    if not first_check:
        return False
    amount_and_currency = currency_check(first_check)
    if not amount_and_currency:
        return False
    return amount_and_currency
