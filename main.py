import os
import requests
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA - Mode Analyse Intelligente Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Récupération dynamique de l'affiche
            t1_raw, t2_raw = "Équipe 1", "Équipe 2"
            if "caption" in msg:
                txt = msg["caption"].strip()
                if "vs" in txt.lower():
                    parts = [p.strip() for p in txt.split("vs")]
                    t1_raw, t2_raw = parts[0], parts[1]
            elif "text" in msg:
                txt = msg["text"].strip()
                if txt and not txt.startswith("/"):
                    if "vs" in txt.lower():
                        parts = [p.strip() for p in txt.split("vs")]
                        t1_raw, t2_raw = parts[0], parts[1]
                    else:
                        t1_raw = txt

            # Hachage unique pour la variabilité des affiches
            seed_val = abs(hash(t1_raw.lower() + "_" + t2_raw.lower()))
            
            # Logique pour identifier un match serré (50/50) ou un match avec favori
            is_balanced = (seed_val % 3 == 0) # Simule l'équilibre des cotes 1X2 serrées
            
            if is_balanced:
                winner_text = "⚠️ Match Équilibré (50/50) - Piège potentiel !"
                s1, s2 = 3, 2
                alt1, alt2 = 4, 3
                market_ou = "Moins de 7.5 buts ou Sécurité"
                pen_missed = "1 à 2 penalties (pression maximale)"
                conseil = "Match fermé ou serré. Il est plus sage de passer son tour ou de jouer prudent."
            else:
                # S'il y a un ascendant logique
                if (seed_val % 2) == 0:
                    winner_text = f"{t1_raw} (Léger Avantage)"
                    s1, s2 = 4, 2
                    alt1, alt2 = 5, 3
                else:
                    winner_text = f"{t2_raw} (Léger Avantage)"
                    s1, s2 = 2, 4
                    alt1, alt2 = 3, 5
                market_ou = "Plus de 6.5 buts"
                pen_missed = "0 à 1 penalty manqué"
                conseil = "Tendance plus ouverte, opportunité sur les buts intermédiaires."

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            current_time = datetime.now().strftime("%H:%M")

            out = (
                "🛡️ **DIENG SMART ANALYSE VIP** 🛡️\n\n"
                f"⚽ **Affiche :** {t1_raw} vs {t2_raw}\n"
                f"🕒 **Heure :** {current_time} (GMT)\n\n"
                f"🎯 **1. Analyse du Vainqueur :** {winner_text}\n\n"
                "🎯 **2. Scores Suggérés & Buts (O/U) :**\n"
                f"• **Option 1 :** {t1_raw} {s1} - {s2} {t2_raw}\n"
                f"• **Option 2 :** {t1_raw} {alt1} - {alt2} {t2_raw}\n"
                f"• **Marché Buts :** {market_ou} (Total estimé : {total_goals} buts)\n\n"
                "🎯 **3. Paramètres & Sécurité :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Pénalties manqués :** {pen_missed}\n\n"
                f"💡 **Conseil Capital :** {conseil}"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
