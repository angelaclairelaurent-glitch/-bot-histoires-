import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "METS_TON_TOKEN_ICI"

# Mots interdits (spam)
SPAM_WORDS = ["t.me/", "joinchat", "crypto", "invest", "gagne de l'argent", "sexe", "@"]

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    
    # Vérifie si c'est du spam
    is_spam = any(word in text for word in SPAM_WORDS)
    
    # Vérifie si c'est un lien
    if "http" in text or "www." in text:
        is_spam = True

    if is_spam:
        try:
            await update.message.delete()
            print(f"Spam supprimé: {text}")
            # Optionnel: bannir l'utilisateur
            # await context.bot.ban_chat_member(update.effective_chat.id, update.effective_user.id)
        except Exception as e:
            print(f"Erreur: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))
    print("Bot anti-spam démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
