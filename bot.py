import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
TOKEN=os.getenv("TOKEN")
app=Flask(__name__)
@app.route('/')
def home(): return "Bot D OK"
async def start(update,context):
    await update.message.reply_text("🎓 BOT BAC D\n/cours - liste\n/cours ph - pH dosage\n/cours meca - mecanique\n/formule - formules\n/exo - exo\n/bac - conseils")
async def cours_cmd(update,context):
    if not context.args:
        await update.message.reply_text("/cours meca\n/cours ph\n/cours cinetique")
        return
    c=context.args[0].lower()
    if c=="meca": t="MECA D: F=m.a, chute v=g.t, h=0.5gt2, Ec=0.5mv2 Ep=mgh Em=cte"
    elif c=="ph": t="pH D: pH=-log[H3O+], fort pH=-logC, eq CaVa=CbVb pH=7"
    elif c=="cinetique": t="CINETIQUE: v=-dC/dt, ester lente reversible, saponif totale rapide"
    else: t="Chapitre: meca, ph, cinetique"
    await update.message.reply_text(t)
async def formule_cmd(update,context):
    await update.message.reply_text("FORMULES: F=m.a, Ec=0.5mv2, pH=-logC, CaVa=CbVb, τ=RC")
async def exo_cmd(update,context):
    await update.message.reply_text("EXO: 10mL acide 0.1M + NaOH 0.1M => Veq=10mL pH=7")
async def bac_cmd(update,context):
    await update.message.reply_text("BAC D: pH + meca + cinetique = 19/20")
def flask_run():
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
def bot_run():
    b=ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start",start))
    b.add_handler(CommandHandler("cours",cours_cmd))
    b.add_handler(CommandHandler("formule",formule_cmd))
    b.add_handler(CommandHandler("exo",exo_cmd))
    b.add_handler(CommandHandler("bac",bac_cmd))
    b.run_polling()
if __name__=="__main__":
    threading.Thread(target=flask_run,daemon=True).start()
    bot_run()
