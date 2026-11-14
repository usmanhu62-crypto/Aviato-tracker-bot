
import os
import threading
import telebot
from flask import Flask

TOKEN = os.environ.get(9124497659:AAF48LxP5_w9OJqMfF5RZoE5EK8vwA-E3wc)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Sannu! Bot din Aviato Tracker ya tashi. Ka rubuta /help")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "Ka rubuta /start don farawa")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
