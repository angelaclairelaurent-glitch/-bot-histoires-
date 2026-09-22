import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN manquant !")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot en ligne !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    # IMPORTANT: use_reloader=False sinon Render crash
    app.run(host="0.0.0.0", port=port, use_reloader=False)

MOTS_SPAM = ["+mo/", "rejoindre la con", "t.me/"]

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()
        for mot in MOTS_SPAM:
            if mot.lower() in text:
                try:
                    await update.message.delete()
                    print(f"Spam supprimé: {text}")
                    return
                except Exception as e:
                    print(f"Impossible de supprimer: {e}")

def main():
    print("=== Bot demarre ! ===", flush=True)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))
    # drop_pending_updates évite les conflits
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    # Lance Flask en arrière-plan
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    print("Flask lancé", flush=True)
    main()
