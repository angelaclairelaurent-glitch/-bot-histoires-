import os, threading, random
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK"

SUJETS = [
    "A Puma Punku en Bolivie, des blocs de 131 tonnes tailles au millimetre. Comment ont-ils fait il y a 2000 ans?",
    "Au Japon, une pyramide sous l'ocean. Yonaguni. 25 metres de haut. Qui l'a construit il y a 10000 ans?",
    "Gobekli Tepe en Turquie. 11000 ans. Plus vieux que les pyramides. Pourquoi l'ont-ils enterre?",
]

async def start(update, context):
    await update.message.reply_text("✅ Bot prêt!\nTape /2videos")

async def deux(update, context):
    await update.message.reply_text("🎬 Je fais tes 2 videos... 20 sec...")
    for i in range(2):
        txt = random.choice(SUJETS)
        gTTS(text=txt, lang='fr').save(f"v{i}.mp3")
        audio = AudioFileClip(f"v{i}.mp3")
        fond = ColorClip(size=(720, 1280), color=(0,0,0), duration=audio.duration).set_audio(audio)
        fond.write_videofile(f"final{i}.mp4", fps=24, codec='libx264', audio_codec='aac', logger=None)
        await update.message.reply_video(video=open(f"final{i}.mp4",'rb'), caption=f"VIDEO {i+1} PRETE ✅\n{txt}\n\n#mystere #fyp")

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
def bot_run():
    b = ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("2videos", deux))
    b.run_polling()

if __name__ == "__main__":
    threading.Thread(target=flask_run, daemon=True).start()
    bot_run()
