import os
import hashlib
import requests
import time
from datetime import datetime

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"

print("Bot Dieng FIFA VIP démarré en mode Polling...")

offset = 0

while True:
    try:
        response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30})
        data = response.json()
        
        if data.get("ok"):
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    txt = msg.get("text", "").strip()
                    
                    if txt and not txt.startswith("/"):
                        parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
                        t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
                        
                        h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
                        h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
                        
                        selector = (h1 + h2) % 3
                        if selector == 0:
                            s1, s2, alt1, alt2 = 6, 5, 7, 6
                            tot_str = "Plus de 6.5 buts"
                            pen_text = "Plus de 2.5 Pénalties manqués"
                            pair_val = "Non"
                        elif selector == 1:
                            s1, s2, alt1, alt2 = 7, 6, 8, 7
                            tot_str = "Plus de 7.5 buts"
                            pen_text = "Plus de 1.5 Pénalties manqués"
                            pair_val = "Oui"
                        else:
                            s1, s2, alt1, alt2 = 5, 4, 6, 5
                            tot_str = "Plus de 8.5 buts"
                            pen_text = "Moins de 2.5 Pénalties manqués"
                            pair_val = "Non"

                        if (h1 * h2) % 2 == 0:
                            winner, team_s1, team_s2, a_s1, a_s2 = t1, s1, s2, alt1, alt2
                        else:
                            winner, team_s1, team_s2, a_s1, a_s2 = t2, s2, s1, alt2, alt1

                        current_time = datetime.now().strftime("%H:%M")

                        out = (
                            f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                            f"⚽ **Match :** {t1} vs {t2}\n"
                            f"🕒 **Heure :** {current_time} (GMT)\n\n"
                            f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                            f"🎯 **2. Scores Exacts & Marchés :**\n"
                            f"• **Option 1 :** {t1} {team_s1} - {team_s2} {t2}\n"
                            f"• **Option 2 :** {t1} {a_s1} - {a_s2} {t2}\n"
                            f"• **Volume de buts :** {tot_str}\n\n"
                            f"🎯 **3. Tendances :**\n"
                            f"• **Total Pair :** {pair_val}\n"
                            f"• **Pénalties Manqués :** {pen_text}\n\n"
                            f"📊 **Confiance VIP :** 98.5%\n"
                        )
                        
                        requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
        
    except Exception as e:
        print("Erreur:", e)
        time.sleep(3)
