import os, threading, random, requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edge_tts
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK - 1 video 90sec"

SUJETS = [
"Au Japon, a 25 metres sous l'ocean, il y a une pyramide que personne ne peut expliquer. On l'appelle Yonaguni. Elle fait 25 metres de haut et 100 metres de long. Decouverte en 1986 par un plongeur japonais qui cherchait des requins, elle possede des escaliers parfaits, des terrasses immenses, et meme une tete de tortue sculptee dans la roche. Les geologues officiels disent que c'est naturel, que l'ocean a sculpte la roche. Mais les architectes les plus connus au monde disent que c'est impossible. La nature ne fait jamais des angles a 90 degres parfaits sur 100 metres. Et elle ne sculpte pas une tete de tortue. Si c'est humain, cette pyramide a plus de 10000 ans. Ca veut dire qu'une civilisation extremement avancee existait avant l'Egypte, avant Sumer. Une civilisation qui maitrisait la pierre, qui a ete engloutie par les eaux lors du deluge. Alors la question est, Atlantide etait elle au Japon? Et si on avait retrouve la preuve que tout ce qu'on nous apprend a l'ecole est faux?",
"Ce que je vais te dire sur Puma Punku en Bolivie va te glacer le sang. Imagine des blocs de 131 tonnes, coupes au millimetre pres. Pas un centimetre d'erreur. Avec des trous parfaits de 5 millimetres a l'interieur, comme fait avec une perceuse laser. Sauf que ce site a 2000 ans. A 4000 metres d'altitude, dans les Andes. A l'epoque, ils n'avaient que des pierres et des cordes, selon les livres d'histoire. Comment ont ils deplace 131 tonnes sans roues, sans chevaux? Et surtout, pourquoi tout le site est detruit comme si une arme surpuissante avait tout souffle en une seconde? Les pierres sont fondues par endroit, comme apres une explosion nucleaire. L'ONU a meme interdit des fouilles supplementaires. Que nous cachent ils a Puma Punku? Et si ce n'etait pas des humains qui l'ont construit?"
]

async def start(update, context):
    await update.message.reply_text("Bot 90sec OK! Tape /video")

async def video_long(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Je genere 1 video 90sec voix grave... 2 min...")
    try:
        txt = random.choice(SUJETS)
        # VOIX LENTE = VIDEO LONGUE
        comm = edge_tts.Communicate(txt, "fr-FR-HenriNeural", rate="-25%", pitch="-6Hz")
        await comm.save("v.mp3")
        audio = AudioFileClip("v.mp3")
        
        # 3 images stables (pas de unsplash qui plante)
        imgs = []
        for i, kw in enumerate(["pyramid underwater", "ancient ruins", "mystery"]):
            try:
                r = requests.get(f"https://picsum.photos/720/1280?random={random.randint(1,1000)}", timeout=15)
                open(f"i{i}.jpg","wb").write(r.content)
                imgs.append(f"i{i}.jpg")
            except: pass
        
        if not imgs:
            await update.message.reply_text("Erreur images, reessaie")
            return

        clips = [ImageClip(p).set_duration(audio.duration/len(imgs)) for p in imgs]
        final = concatenate_videoclips(clips).set_audio(audio)
        final.write_videofile("final.mp4", fps=20, codec='libx264', audio_codec='aac', logger=None, threads=1)
        
        await update.message.reply_video(video=open("final.mp4",'rb'), caption=f"VIDEO 90sec {audio.duration:.0f}s #mystere #fyp")
        audio.close()
    except Exception as e:
        await update.message.reply_text(f"Erreur: {e}")

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
def bot_run():
    b=ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start",start))
    b.add_handler(CommandHandler("video",video_long))
    b.add_handler(CommandHandler("2videos",video_long)) # ancien nom marche aussi
    b.run_polling()

if __name__=="__main__":
    threading.Thread(target=flask_run,daemon=True).start()
    bot_run()
