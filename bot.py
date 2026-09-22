import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN") or "8672527452:AAGjFUCJZYQki_hVoOQROlbtpkxpPv4gskA"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Ca marche bro ! Tape /histoire")

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
