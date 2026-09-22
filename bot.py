def bac_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 CONSEILS BAC 2026 PHYSIQUE:\n\n"
        "1. Toujours écrire données + formule + application\n"
        "2. Unités obligatoires! Sans unité = 0 point\n"
        "3. Schéma = +1 point facile\n"
        "4. Chapitres qui tombent 90%: RC/RL, Chute, pH, Ondes\n\n"
        "Tu veux que je t'explique un chapitre en vocal? Dis-moi lequel!"
    )

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
def bot_run():
    b=ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("cours", cours_cmd))
    b.add_handler(CommandHandler("formule", formule_cmd))
    b.add_handler(CommandHandler("exo", exo_cmd))
    b.add_handler(CommandHandler("bac", bac_cmd))
    b.run_polling()

if __name__=="__main__":
    threading.Thread(target=flask_run, daemon=True).start()
    bot_run()

