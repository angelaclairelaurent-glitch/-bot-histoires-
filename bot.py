import os, threading, random, requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edge_tts
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK"

SUJETS = [
{
"text": "Au Japon, a 25 metres sous l'ocean, il y a une pyramide que personne ne peut expliquer. On l'appelle Yonaguni. Elle fait 25 metres de haut et 100 metres de long. Decouverte en 1986 par un plongeur japonais qui cherchait des requins, elle possede des escaliers parfaits, des terrasses immenses, et meme une tete de tortue sculptee dans la roche. Les geologues officiels disent que c'est naturel, que l'ocean a sculpte la roche. Mais les architectes les plus connus au monde disent que c'est impossible. La nature ne fait jamais des angles a 90 degres parfaits sur 100 metres. Et elle ne sculpte pas une tete de tortue. Si c'est humain, cette pyramide a plus de 10000 ans. Ca veut dire qu'une civilisation extremement avancee existait avant l'Egypte, avant Sumer. Une civilisation qui maitrisait la pierre, qui a ete engloutie par les eaux lors du deluge. Alors la question est, Atlantide etait elle au Japon? Et si on avait retrouve la preuve que tout ce qu'on nous apprend a l'ecole est faux?",
"images": ["underwater pyramid", "yonaguni japan", "atlantis ruins"]
},
{
"text": "Ce que je vais te dire sur Puma Punku en Bolivie va te glacer le sang. Imagine des blocs de 131 tonnes, coupes au millimetre pres. Pas un centimetre d'erreur. Avec des trous parfaits de 5 millimetres a l'interieur, comme fait avec une perceuse laser. Sauf que ce site a 2000 ans. A 4000 metres d'altitude, dans les Andes. A l'epoque, ils n'avaient que des pierres et des cordes, selon les livres d'histoire. Comment ont ils deplace 131 tonnes sans roues, sans chevaux? Et surtout, pourquoi tout le site est detruit comme si une arme surpuissante avait tout souffle en une seconde? Les pierres sont fondues par endroit, comme apres une explosion nucleaire. L'ONU a meme interdit des fouilles supplementaires. Que nous cachent ils a Puma Punku? Et si ce n'etait pas des humains qui l'ont construit?",
"images": ["puma punku", "megalithic stone", "ancient alien ruins"]
}
]

def get_imgs(kws):
    paths=[]
    for i,kw in enumerate(kws):
        try:
            r=requests.get(f"https://source.unsplash.com/720x1280/?{kw.replace(' ','%20')}", timeout=10)
            open(f"img{i}.jpg","wb").write(r.content)
            paths.append(f"img{i}.jpg")
        except: pass
    return paths if paths else ["img0.jpg"]

async def start(update, context):
    await update.message.reply_text("Bot 2MIN pret! Tape /2videos")

async def deux(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Je fais 2 videos LONGUES 90sec voix grave + vraies images... 3 min...")
    for i in range(2):
        s=random.choice(SUJETS)
        # VOIX ULTRA GRAVE ET LENTE = VIDEO PLUS LONGUE
        comm = edge_tts.Communicate(s["text"], "fr-FR-HenriNeural", rate="-20%", pitch="-8Hz")
        await comm.save(f"v{i}.mp3")
        audio = AudioFileClip(f"v{i}.mp3")
        print(f"DUREE AUDIO: {audio.duration} sec")
        imgs = get_imgs(s["images"])
        clips=[ImageClip(p).set_duration(audio.duration/len(imgs)).resize((720,1280)) for p in imgs]
        final = concatenate_videoclips(clips).set_audio(audio)
        final.write_videofile(f"final{i}.mp4", fps=24, codec='libx264', audio_codec='aac', logger=None)
        await update.message.reply_video(video=open(f"final{i}.mp4",'rb'), caption=f"VIDEO {i+1} - {audio.duration:.0f} sec #mystere #fyp")
        audio.close()

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
def bot_run():
    b=ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start",start))
    b.add_handler(CommandHandler("2videos",deux))
    b.run_polling()
if __name__=="__main__":
    threading.Thread(target=flask_run,daemon=True).start()
    bot_run()
