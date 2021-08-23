import telebot
import config
import src.stats.stats as stats
import src.db.db as db
from src.convert.exchanging import get_reply_text
from src.convert.message_regex import scan_text


db.init()
TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)


# Starting interaction within /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello')


# Reaction to suitable message, what contain currency and her amount
@bot.message_handler(func=lambda message: False if not scan_text(message.text) else True)
def echo_all(message):
    amount_and_currency = scan_text(message.text)
    reply_text = get_reply_text(amount_and_currency)
    stats.update_user_stats(amount_and_currency, message.from_user.username)
    bot.reply_to(message, reply_text)


bot.polling()
