import os, threading, random, requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edge_tts
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "OK"

SUJETS = {
"yonaguni": "Au Japon, a 25 metres sous l'ocean, il y a une pyramide que personne ne peut expliquer. On l'appelle Yonaguni. Elle fait 25 metres de haut et 100 metres de long. Decouverte en 1986, elle possede des escaliers parfaits et des terrasses immenses. Les geologues disent que c'est naturel. Mais les architectes disent que c'est impossible. La nature ne fait jamais des angles a 90 degres parfaits. Si c'est humain, elle a plus de 10000 ans. Atlantide etait elle au Japon?",
"pumapunku": "A Puma Punku en Bolivie, il y a des blocs de 131 tonnes, coupes au millimetre pres. Avec des trous parfaits de 5 millimetres, comme fait avec une perceuse laser. Sauf que ce site a 2000 ans. A 4000 metres d'altitude. Comment ont ils deplace 131 tonnes sans roues? Pourquoi tout le site est detruit comme si une arme surpuissante avait tout souffle? Les pierres sont fondues par endroit. Que nous cachent ils a Puma Punku?"
}

def make_alive_clip(image_path, duration):
    clip = ImageClip(image_path).set_duration(duration)
    clip = clip.resize(lambda t: 1 + 0.15 * (t / duration))
    clip = clip.set_position(('center','center'))
    return clip

def get_images(key):
    queries = ["underwater+pyramid", "japan+ocean+ruins", "ancient+stairs"] if key=="yonaguni" else ["puma+punku", "megalithic+stone+bolivia", "ancient+destruction"]
    files=[]
    for i,q in enumerate(queries):
        try:
            r=requests.get(f"https://source.unsplash.com/720x1280/?{q}", timeout=15)
            open(f"i{i}.jpg","wb").write(r.content)
        except:
            r=requests.get(f"https://picsum.photos/720/1280?random={random.randint(1,999)}", timeout=10)
            open(f"i{i}.jpg","wb").write(r.content)
        files.append(f"i{i}.jpg")
    return files

async def start(update, context):
    await update.message.reply_text("Bot V5.1 vivant pret! Tape /video")

async def video_long(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("V5 VIVANTE en cours... 2min30 patiente bro")
    try:
        key = random.choice(list(SUJETS.keys()))
        txt = SUJETS[key]
        ssml = f'<speak><prosody rate="-5%" pitch="-2Hz" volume="+10%">{txt.replace(".", ".<break time=\"500ms\"/>")}</prosody></speak>'
        await edge_tts.Communicate(ssml, "fr-FR-HenriNeural").save("v.mp3")
        audio = AudioFileClip("v.mp3")
        imgs = get_images(key)
        dur = audio.duration / len(imgs)
        base_clips = [make_alive_clip(f, dur) for f in imgs]
        video_base = concatenate_videoclips(base_clips, method="compose").set_audio(audio)
        video_base = video_base.set_position(('center','center')).resize((720,1280))
        phrases = [p.strip() for p in txt.split(".") if p.strip()]
        total_chars = sum(len(p) for p in phrases)
        subs = []
        t = 0
        for phrase in phrases:
            phrase_dur = audio.duration * (len(phrase) / total_chars)
            try:
                txt_clip = TextClip(phrase, fontsize=32, color='white', stroke_color='black', stroke_width=3, method='caption', size=(650, None), font='DejaVu-Sans-Bold')
                txt_clip = txt_clip.set_position(('center', 0.78), relative=True).set_duration(phrase_dur).set_start(t)
                subs.append(txt_clip)
            except:
                pass
            t += phrase_dur
        final = CompositeVideoClip([video_base] + subs, size=(720,1280))
        final.write_videofile("final.mp4", fps=20, codec='libx264', audio_codec='aac', preset='ultrafast', threads=1, logger=None)
        await update.message.reply_video(video=open("final.mp4",'rb'), caption=f"V5 VIVANTE {audio.duration:.0f}s")
        audio.close()
    except Exception as e:
        await update.message.reply_text(f"Erreur V5: {e}")

def flask_run(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
def bot_run():
    b=ApplicationBuilder().token(TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CommandHandler("video", video_long))
    b.add_handler(CommandHandler("videos", video_long))
    b.run_polling()

if __name__=="__main__":
    threading.Thread(target=flask_run, daemon=True).start()
    bot_run()
