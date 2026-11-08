import time
import requests

TOKEN = "9204768032:AAGdCe7c_tym2R6zyug8jtx33P9gC4wpZx4"

print("Bot démarré en mode Polling direct...")

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1&timeout=30"
        response = requests.get(url).json()
        
        if "result" in response and response["result"]:
            for update in response["result"]:
                chat_id = update["message"]["chat"]["id"]
                text_recu = update["message"].get("text", "").strip()
                
                if text_recu and not text_recu.startswith("/"):
                    analysis_text = f"🔥 Analyse VIP : {text_recu} -> Match validé et sécurisé !"
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": analysis_text}
                    )
        time.sleep(1)
    except Exception as e:
        print("Erreur:", e)
        time.sleep(5)
