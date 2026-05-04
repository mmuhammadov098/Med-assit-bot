import os
import telebot
from flask import Flask
from threading import Thread

# 1. Render uchun Web-Server (Botni uyg'oq tutish uchun)
app = Flask('')

@app.route('/')
def home():
    return "MedAssist bot ishlamoqda!"

def run():
    # Render beradigan portni olamiz
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot sozlamalari (Siz bergan token joylandi)
TOKEN = "8764111707:AAFzU3CuTSNlkhzB6Ah3rQaUKnDc41DE9Gw"
bot = telebot.TeleBot(TOKEN)

# 3. Tibbiy lug'at (Dori bazasi)
dori_bazasi = {
    "furatsilin": "Tomoqni chayish va jarohatlarni yuvish uchun mikrobga qarshi vosita.",
    "mezim": "Ovqat hazm qilishni yaxshilovchi fermentlar majmuasi.",
    "diklofenak": "Bo'g'im va mushak og'riqlarida yallig'lanishga qarshi vosita.",
    "yodomarin": "Qalqonsimon bez kasalliklarining oldini olish va davolash uchun yod preparati.",
    "analgin": "Og'riq qoldiruvchi va isitma tushiruvchi dori vositasi.",
    "anaprilin": "Yurak urishini sekinlashtiruvchi va qon bosimini tushiruvchi vosita."
}

@bot.message_handler(commands=['start'])
def salom(message):
    bot.reply_to(message, "Salom! MedAssist Pro botiga xush kelibsiz. Dori nomini yozing, men u haqida ma'lumot beraman.")

@bot.message_handler(func=lambda message: True)
def dori_qidirish(message):
    nomi = message.text.lower().strip()
    javob = dori_bazasi.get(nomi, "Bunday dori bazada yo'q")
    
    if nomi in dori_bazasi:
        bot.reply_to(message, f"💊 {nomi.capitalize()}: {javob}")
    else:
        bot.reply_to(message, javob)

# 4. Asosiy ishga tushirish qismi
if __name__ == "__main__":
    keep_alive() # Flask serverni orqa fonda yoqish
    print("Bot Render serverida muvaffaqiyatli ishga tushdi!")
    bot.infinity_polling()
