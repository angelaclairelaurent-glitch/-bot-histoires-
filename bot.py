import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

load_dotenv()

# C'ETAIT JETON AVANT, MAINTENANT C'EST TOKEN POUR RENDER
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN manquant ! Mets-le dans Render > Environment")

# --- Serveur obligatoire pour Render (règle le bug No open ports) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot en ligne !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Ton système anti-spam ---
MOTS_SPAM = ["+mo/", "rejoindre la con", "t.me/", "gagner de l'argent"]

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()
        for mot in MOTS_SPAM:
            if mot.lower() in text:
                try:
                    await update.message.delete()
                    await update.message.reply_text(f"🚫 Spam détecté et supprimé ! Mot: {mot}")
                    return
                except:
                    pass

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))
    print("Bot démarré !")
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
