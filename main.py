import telebot

TOKEN = "9086694940:AAHFD_3fyVWG_-pcU_v4SQCBGTEB7BNEuc4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом устод! Ман боти шумо Toshov2008_AI_bot хастам! Зур шуд! 😊")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Шумо навиштед: " + message.text)

bot.polling()
