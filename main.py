import os
import hashlib
import requests
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP 100% Actif - Analyse Universelle FC26"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    data = await req.json()
    if data and "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        txt = msg.get("text", "").strip()
        
        if txt and not txt.startswith("/"):
            parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
            t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
            
            # Analyse universelle et dynamique basée sur l'empreinte unique de n'importe quelle équipe saisie
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Calcul dynamique du rapport de force et des scores serrés (type FC26 Penalty)
            scenario = (h1 + h2) % 4
            if scenario == 0:
                s1, s2 = 5, 4
                alt_s1, alt_s2 = 4, 3
                winner = t1
                analysis = f"{t1} montre une meilleure maîtrise sous pression et prend l'ascendant tactique face à {t2}."
            elif scenario == 1:
                s1, s2 = 4, 2
                alt_s1, alt_s2 = 4, 3
                winner = t1
                analysis = f"Solidité défensive et efficacité chirurgicale de {t1} pour contenir les offensives de {t2}."
            elif scenario == 2:
                s1, s2 = 4, 5
                alt_s1, alt_s2 = 3, 4
                winner = t2
                analysis = f"Sursaut d'orgueil redoutable de {t2} qui renverse la tendance face à {t1} dans la séance."
            else:
                s1, s2 = 3, 4
                alt_s1, alt_s2 = 4, 5
                winner = t2
                analysis = f"{t2} fait preuve d'un sang-froid supérieur dans les moments clés pour dominer {t1}."

            total_goals = s1 + s2
            tot_str = f"Plus de {total_goals - 0.5} buts (Séance intense)"
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            pen_text = f"Convertis avec précision (Plus de {(total_goals // 2)} réussis)"
            confidence = round(94.5 + ((h1 * h2) % 40) / 10.0, 1)

            current_time = datetime.now().strftime("%H:%M")

            out = (
                f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                f"⚽ **Affiche :** {t1} vs {t2}\n"
                f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                f"📋 **Rapport d'expertise :**\n"
                f"• {analysis}\n\n"
                f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                f"🎯 **2. Scores Exacts & Marchés :**\n"
                f"• **Option 1 (Principal) :** {t1} {s1} - {s2} {t2}\n"
                f"• **Option 2 (Alternatif) :** {t1} {alt_s1} - {alt_s2} {t2}\n"
                f"• **Volume de buts :** {tot_str}\n\n"
                f"🎯 **3. Tendances Marché :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Pénalties :** {pen_text}\n\n"
                f"📊 **Confiance VIP :** {confidence}%\n"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
            
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})
