import os
import threading
import random
import telebot
from flask import Flask
from collections import deque

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store last 100 rounds
history = deque(maxlen=100)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🎮 *Aviato Tracker Bot is Online!*\n\n"
        "Commands:\n"
        "/add 2.5 - Add a round result (e.g. /add 2.5)\n"
        "/history - See last 10 rounds\n"
        "/stats - See statistics\n"
        "/signal - Get signal based on history\n"
        "/clear - Clear history\n"
        "/help - Help",
        parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    start(message)

@bot.message_handler(commands=['add'])
def add_round(message):
    try:
        parts = message.text.split()
        crash = float(parts[1])
        history.append(crash)
        bot.reply_to(message, f"✅ Added: {crash}x\nTotal rounds: {len(history)}")
    except:
        bot.reply_to(message, "❌ Wrong format. Use: /add 2.5")

@bot.message_handler(commands=['history'])
def show_history(message):
    if not history:
        bot.reply_to(message, "No history yet. Use /add 2.5 to add rounds")
        return
    last = list(history)[-10:]
    text = "📋 *Last 10 Rounds:*\n" + "\n".join([f"{i+1}. {x}x" for i, x in enumerate(last)])
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats(message):
    if not history:
        bot.reply_to(message, "No data yet. Add rounds with /add")
        return
    data = list(history)
    avg = sum(data) / len(data)
    over_2 = sum(1 for x in data if x >= 2) / len(data) * 100
    over_5 = sum(1 for x in data if x >= 5) / len(data) * 100
    max_crash = max(data)
    bot.reply_to(message,
        f"📊 *Stats ({len(data)} rounds)*\n\n"
        f"Average: {avg:.2f}x\n"
        f"Over 2x: {over_2:.1f}%\n"
        f"Over 5x: {over_5:.1f}%\n"
        f"Highest: {max_crash}x",
        parse_mode="Markdown")

@bot.message_handler(commands=['signal'])
def signal(message):
    if len(history) < 5:
        bot.reply_to(message, "⚠️ Add at least 5 rounds first with /add. Example: /add 1.2")
        return
    data = list(history)[-10:]
    low_count = sum(1 for x in data if x < 2)
    
    if low_count >= 7:
        advice = "🔥 *HIGH CHANCE SIGNAL*\nLast 10 rounds mostly low (<2x).\nMany players wait for a higher round now.\n\nSuggested: Wait for 2x - 3x\nRisk: HIGH - Never bet what you can't lose"
    elif low_count >= 4:
        advice = "⚖️ *MEDIUM SIGNAL*\nMixed rounds.\nSuggested: Play safe 1.5x - 2x"
    else:
        advice = "❄️ *LOW SIGNAL*\nRecent rounds were high.\nSuggested: Wait / Play very low 1.2x - 1.5x"
    
    bot.reply_to(message, advice + "\n\n⚠️ Aviato is random. This is analysis, not a guarantee.", parse_mode="Markdown")

@bot.message_handler(commands=['clear'])
def clear(message):
    history.clear()
    bot.reply_to(message, "🗑️ History cleared!")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
