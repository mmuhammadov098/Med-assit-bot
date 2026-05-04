import os
import telebot
from flask import Flask
from threading import Thread

# 1. Render uchun kichik Web-Server (Bot o'chib qolmasligi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlamoqda!"

def run():
    # Render avtomatik ravishda PORT taqdim etadi
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot sozlamalari (Tokeningizni bu yerga qo'ying)
TOKEN = "SIZNING_BOT_TOKENINGIZ" # <-- O'z tokeningizni yozing
bot = telebot.TeleBot(TOKEN)

# 3. Tibbiy lug'at (Baza)
dori_bazasi = {
    "furatsilin": "Tomoqni chayish va jarohatlarni yuvish uchun mikrobga qarshi vosita.",
    "mezim": "Ovqat hazm qilishni yaxshilovchi fermentlar majmuasi.",
    "diklofenak": "Bo'g'im va mushak og'riqlarida yallig'lanishga qarshi vosita.",
    "yodomarin": "Qalqonsimon bez kasalliklarining oldini olish va davolash uchun yod preparati."
}

@bot.message_handler(commands=['start'])
def salom(message):
    bot.reply_to(message, "Salom! Dori nomini yozing, men u haqida ma'lumot beraman.")

@bot.message_handler(func=lambda message: True)
def dori_qidirish(message):
    nomi = message.text.lower().strip()
    javob = dori_bazasi.get(nomi, "Bunday dori bazada yo'q")
    if nomi in dori_bazasi:
        bot.reply_to(message, f"💊 {nomi.capitalize()}: {javob}")
    else:
        bot.reply_to(message, javob)

# 4. Serverni va Botni ishga tushirish
if __name__ == "__main__":
    keep_alive() # Avval serverni yoqamiz
    print("Bot Render-da ishga tushishga tayyor...")
    bot.infinity_polling() # Keyin botni yoqamiz
