import os, threading, random
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, TextClip, CompositeVideoClip

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK 2 VIDEOS SANS CLE"

SUJETS = [
    "A Puma Punku en Bolivie, des blocs de 131 tonnes taillés au millimètre. Comment ont-ils fait il y a 2000 ans sans outils modernes? Le mystère reste total.",
    "Au Japon, une pyramide sous l'océan. Yonaguni. 25 mètres de haut. Escaliers et terrasses parfaits. Naturel ou fait par l'homme il y a 10 000 ans?",
    "Gobekli Tepe en Turquie. 11 000 ans. Plus vieux que les pyramides. Construit par des chasseurs-cueilleurs. Pourquoi l'ont-ils enterré volontairement?",
]

async def start(update, context):
    await update.message.reply_text("✅ Bot prêt sans clé!\nTape /2videos")

async def deux(update, context):
    await update.message.reply_text("🎬 Création de tes 2 vidéos en cours... 40 secondes...")
    for i in range(2):
        txt = random.choice(SUJETS)
        gTTS(text=txt, lang='fr').save(f"v{i}.mp3")
        audio = AudioFileClip(f"v{i}.mp3")
        
        # Fond noir format TikTok
        fond = ColorClip(size=(1080, 1920), color=(0,0,0), duration=audio.duration)
        # Texte au centre
        try:
            texte = TextClip(txt, fontsize=45, color='white', size=(900, None), method='caption', font='DejaVu-Sans-Bold')
            texte = texte.set_position('center').set_duration(audio.duration)
            final = CompositeVideoClip([fond, texte]).set_audio(audio)
        except:
            final = fond.set_audio(audio)
        
        final.write_videofile(f"final{i}.mp4", fps=24, codec='libx264', audio_codec='aac', logger=None)
        await update.message.reply_video(video=open(f"final{i}.mp4",'rb'), caption=f"VIDÉO {i+1} PRÊTE À POSTER ✅\n\nCopie ce texte pour TikTok:\n{txt}\n\n#mystere #fyp")

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
def bot_run():
    b = ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("2videos", deux))
    b.run_polling()

if __name__ == "__main__":
    threading.Thread(target=flask_run, daemon=True).start()
    bot_run()
