import os
import threading
import telebot
from flask import Flask

# Get Token from Render Environment Variables, do NOT put token here
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Aviato Tracker Bot is online. Type /help")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "Type /start to begin")

def run_bot():
    bot.infinity_polling()

# Run Telegram Bot in background thread so Flask can also run
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
