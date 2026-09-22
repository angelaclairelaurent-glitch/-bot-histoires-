import os, threading, random, textwrap
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edge_tts
from moviepy.editor import AudioFileClip, ColorClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK"

SUJETS = [
    """Tu ne vas jamais croire ce qui a ete decouvert a Puma Punku en Bolivie. En 1945, des archeologues trouvent des blocs de 131 tonnes. Le plus fou? Ils sont coupes au millimetre pres, avec des trous parfaits a l'interieur. Aujourd'hui meme avec nos machines laser, on aurait du mal a faire ca. Mais le plus mysterieux, c'est que ce site a 2000 ans. A l'epoque, ils n'avaient que des outils en pierre. Comment ont ils deplace 131 tonnes a 4000 metres d'altitude? Et pourquoi ce site a ete detruit en une seule nuit, comme par une explosion nucleaire? Les scientifiques n'ont toujours pas de reponse.""",
    """Au Japon, a 25 metres sous l'ocean, il y a une pyramide que personne ne peut expliquer. On l'appelle Yonaguni. Elle fait 25 metres de haut et 100 metres de long. Decouverte en 1986 par un plongeur, elle possede des escaliers, des terrasses, et meme une tete de tortue sculptee. Les geologues disent que c'est naturel. Mais les architectes disent que c'est impossible que la nature fasse des angles a 90 degres parfaits. Si c'est humain, elle a 10000 ans. Ca veut dire qu'une civilisation avancee existait avant l'Egypte. Une civilisation qui a ete engloutie par les eaux. Atlantide etait elle au Japon?""",
    """Gobekli Tepe en Turquie est le plus grand mystere de l'humanite. 11 000 ans. C'est 6000 ans plus vieux que les pyramides d'Egypte. C'est le premier temple jamais construit par l'homme. Mais le jour ou ils l'ont fini, ils l'ont enterre. Volontairement. Ils ont recouvert des piliers de 20 tonnes avec des tonnes de terre. Pourquoi construire pendant 1000 ans pour tout enterrer ensuite? Que cherchaient ils a cacher? Ou a proteger? Depuis sa decouverte en 1994, on a fouille seulement 5 pourcent du site. 95 pourcent est encore sous terre. Imagine ce qu'on va encore trouver."""
]

def make_text_image(text, size=(720,1280)):
    img = Image.new('RGB', size, color=(18,18,18))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
    except:
        font = ImageFont.load_default()
    wrapped = textwrap.fill(text, width=28)
    bbox = draw.multiline_textbbox((0,0), wrapped, font=font, align="center")
    w,h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.multiline_text((size[0]/2 - w/2, size[1]/2 - h/2), wrapped, font=font, fill="white", align="center", stroke_width=2, stroke_fill="black")
    img.save("txt.png")
    return "txt.png"

async def start(update, context):
    await update.message.reply_text("Bot VIRAL grave pret! Tape /2videos")

async def deux(update, context):
    await update.message.reply_text("Je fais tes 2 videos longues voix grave... 60 sec...")
    for i in range(2):
        txt = random.choice(SUJETS)
        comm = edge_tts.Communicate(txt, "fr-FR-HenriNeural", rate="-10%", pitch="-5Hz")
        await comm.save(f"v{i}.mp3")
        audio = AudioFileClip(f"v{i}.mp3")
        fond = ColorClip(size=(720,1280), color=(18,18,18), duration=audio.duration)
        txt_path = make_text_image(txt)
        txt_clip = ImageClip(txt_path).set_duration(audio.duration).set_pos("center")
        final = CompositeVideoClip([fond, txt_clip]).set_audio(audio)
        final.write_videofile(f"final{i}.mp4", fps=24, codec='libx264', audio_codec='aac', logger=None)
        await update.message.reply_video(video=open(f"final{i}.mp4",'rb'), caption=f"VIDEO {i+1} - {txt[:100]}... #mystere #fyp")
        audio.close()

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
def bot_run():
    b = ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("2videos", deux))
    b.run_polling()

if __name__ == "__main__":
    threading.Thread(target=flask_run, daemon=True).start()
    bot_run()
