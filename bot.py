import re
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN manquant !")

SPAM_WORDS = ["t.me/", "joinchat", "crypto", "invest", "gagne de l'argent", "sexe", "@"]

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    is_spam = any(word in text for word in SPAM_WORDS)
    if "http" in text or "www." in text:
        is_spam = True
    if is_spam:
        try:
            await update.message.delete()
        except:
            pass

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))
    print("Bot anti-spam démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
