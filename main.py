import telebot
import config
import exchanging
import message_regex

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)


# Starting interaction within /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello')


# Reaction to suitable message, what contain currency and her amount
@bot.message_handler(func=lambda message: False if not message_regex.scan_text(message.text) else True)
def echo_all(message):
    amount_and_currency = message_regex.scan_text(message.text)
    reply_text = exchanging.get_reply_text(amount_and_currency)
    bot.reply_to(message, reply_text)


bot.polling()
