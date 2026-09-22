import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Physique-Chimie OK"

COURS = {
"meca": "🔹 MECANIQUE - Terminale\n\n1. 2e loi Newton: ΣF = m.a\n2. Chute libre: a=g=9.8 m/s², v=g.t, y=0.5.g.t²\n3. Energie: Ec=0.5.m.v², Ep=m.g.h, Em=Ec+Ep constant\n4. Satellite: v=√(g0.R²/r), T=2π√(r³/g0R²)\n\nASTUCE BAC: Toujours faire bilan des forces avant!",
"chimie": "🔹 CHIMIE - pH et acide/base\n\npH = -log[H3O+]\nAcide fort: [H3O+]=C => pH=-logC\nBase forte: [OH-]=C => pH=14+logC\nHenderson: pH=pKa+log([base]/[acide])\nEquivalence: n_acide = n_base\n\nASTUCE: A l'équivalence acide fort/base forte pH=7",
"optique": "🔹 ONDES\n\nλ = c.T = c/f\nE = h.f (photon)\nInterférences: Δ = kλ -> brillant, Δ=(k+0.5)λ -> sombre\nEffet Doppler: f_recue = f_émise * (v/(v±vs))",
"elec": "🔹 ELECTRICITE\n\nLoi d'Ohm: U=R.I\nRC: Uc=E(1-exp(-t/RC)), τ=RC\nRL: I=E/R(1-exp(-tR/L)), τ=L/R\nEnergie bobine: E=0.5.L.I², condo: E=0.5.C.U²"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 BOT BAC PHYSIQUE-CHIMIE TERMINALE\n\n"
        "/cours - Liste des chapitres\n"
        "/cours meca - Cours mécanique\n"
        "/formule - Toutes les formules BAC\n"
        "/exo meca - Exercice corrigé\n"
        "/bac - Conseils BAC\n\n"
        "Tape /cours pour commencer!"
    )

async def cours_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📚 CHAPITRES DISPO:\n"
            "- meca (Mécanique Newton)\n"
            "- chimie (pH, acide/base)\n"
            "- optique (Ondes, photon)\n"
            "- elec (RC, RL)\n\n"
            "Ex: /cours meca"
        )
        return
    chap = context.args[0].lower()
    if chap in COURS:
        await update.message.reply_text(COURS[chap])
    else:
        await update.message.reply_text("Chapitre pas trouvé. Tape /cours")

async def formule_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 FORMULES BAC A RETENIR PAR COEUR:\n\n"
        "ΣF=m.a | P=m.g | Ec=½mv² | Ep=mgh\n"
        "pH=-log[H3O+] | n=C.V | m=n.M\n"
        "U=R.I | P=U.I | E=½CU² | τ=RC\n"
        "λ=c/f | E=h.f | v=d/t\n\n"
        "Tape /cours [chapitre] pour les détails"
    )

async def exo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 EXO TYPE BAC - MECANIQUE:\n\n"
        "Un corps de 2kg tombe de 10m sans vitesse initiale.\n"
        "1. Calcule Ec et Ep en haut?\n"
        "2. Vitesse en bas?\n\n"
        "✅ CORRIGÉ:\n"
        "1. En haut: Ec=0, Ep=mgh=2*9.8*10=196J\n"
        "2. En bas: Em conserve => Ec=196J\n"
        "=> 0.5*2*v²=196 => v=14 m/s\n\n"
        "Tape /exo chimie pour un exo chimie"
    )

async def bac_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
