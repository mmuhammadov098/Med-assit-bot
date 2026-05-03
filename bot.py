import urllib.request
import urllib.parse
import json
import time

# Ma'lumotlar bazasini import qilish
try:
    from dorilar import DORI_BAZASI
except ImportError:
    from newfile import DORI_BAZASI

# Bot sozlamalari
TOKEN = "8764111707:AAFzU3CuTSNlkhzB6Ah3rQaUKnDc41DE9Gw"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

def call_method(method, params=None):
    url = BASE_URL + method
    if params:
        query_string = urllib.parse.urlencode(params)
        url += "?" + query_string
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            return json.loads(response.read().decode())
    except:
        return None

def main():
    last_update_id = 0
    print("--- BOT ISHGA TUSHDI ---")
    print(f"Bazada {len(DORI_BAZASI)} ta dori mavjud.")
    
    while True:
        updates = call_method("getUpdates", {"offset": last_update_id + 1, "timeout": 30})
        
        if updates and updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"]
                
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    user_text = update["message"]["text"].lower().strip()
                    
                    if user_text == "/start":
                        reply = "Salom! Dori nomini yozing."
                    elif user_text in DORI_BAZASI:
                        info = DORI_BAZASI[user_text]
                        # Agar info lug'at bo'lsa uz qismini oladi, aks holda matnni o'zini
                        if isinstance(info, dict):
                            reply = info.get("uz", "Ma'lumot topilmadi")
                        else:
                            reply = info
                    else:
                        reply = "Bunday dori bazada yo'q"
                    
                    call_method("sendMessage", {"chat_id": chat_id, "text": reply})
        
        time.sleep(1)

if __name__ == "__main__":
    main()
