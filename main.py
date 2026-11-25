# -*- coding: utf-8 -*-
import os
import threading
import telebot
from openai import OpenAI
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "ToshovGPT is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_ID = "agent_6b060cadc0b88191b4248dca2b0f3b43"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

user_histories = {}
MAX_HISTORY = 20

def get_history(user_id):
    if user_id not in user_histories:
        user_histories[user_id] = []
    return user_histories[user_id]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "Салом! 👋 Хуш омадед! Имрӯз ба шумо бо чӣ ёрӣ расонам?")

@bot.message_handler(commands=['new'])
def new_chat(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "Хуб! Сӯҳбати навро сар кардем. 👋 Чӣ ёрӣ расонам?")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer(message):
    try:
        if not message.text:
            return
        user_id = message.chat.id
        history = get_history(user_id)
        history.append({"role": "user", "content": message.text})
        if len(history) > MAX_HISTORY:
            history = history[-MAX_HISTORY:]
            user_histories[user_id] = history

        # Занг ба Агенти ToshovGPT
        response = client.responses.create(
            agent=AGENT_ID,
            input=history
        )
        text = response.output_text
        if not text:
            text = "Бубахшед, агент ҷавоб надод. Лутфан боз як бор нависед!"

        history.append({"role": "assistant", "content": text})
        for i in range(0, len(text), 4000):
            part = text[i:i+4000]
            if i == 0:
                bot.reply_to(message, part)
            else:
                bot.send_message(message.chat.id, part)
    except Exception as e:
        print(f"Хатогӣ: {e}")
        bot.reply_to(message, "Бубахшед, каме хатогӣ шуд. Лутфан боз як бор нависед!")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    print("ToshovGPT 24/7 кор мекунад...")
    bot.polling(none_stop=True, skip_pending=True)
# ToshovGPT - бо Агент
