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
    return {"status": "Dieng FIFA VIP 100% Actif - Mode Penalty Pro & Nuls"}

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
            
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Détermination intelligente du scénario (Victoire T1, Victoire T2 ou Match Nul)
            scenario = (h1 + h2) % 5
            
            if scenario == 0:
                # Match Nul serré
                s_t1, s_t2 = 4, 4
                alt_t1, alt_t2 = 5, 5
                winner = "Match Nul (Équilibre parfait)"
                analysis = f"Neutralisation parfaite entre {t1} et {t2} qui se neutralisent dans l'exercice des tirs au but."
            elif scenario == 1:
                # Match Nul prolifique
                s_t1, s_t2 = 5, 5
                alt_t1, alt_t2 = 4, 4
                winner = "Match Nul (Partage des points)"
                analysis = f"Duel extrêmement accroché où {t1} et {t2} font preuve d'une efficacité strictement identique."
            elif scenario == 2:
                # Victoire T1
                s_t1, s_t2 = 5, 4
                alt_t1, alt_t2 = 4, 3
                winner = t1
                analysis = f"Supériorité technique et sang-froid supérieur de {t1} pour s'imposer face à {t2}."
            elif scenario == 3:
                # Victoire T1 large
                s_t1, s_t2 = 4, 2
                alt_t1, alt_t2 = 5, 3
                winner = t1
                analysis = f"Maîtrise tactique et solidité défensive de {t1} pour verrouiller l'écart face à {t2}."
            else:
                # Victoire T2
                s_t1, s_t2 = 3, 5
                alt_t1, alt_t2 = 4, 5
                winner = t2
                analysis = f"Renversement de situation et efficacité redoutable de {t2} pour surprendre {t1}."

            total_goals = s_t1 + s_t2
            
            if total_goals >= 10:
                tot_str = "Plus de 9.5 buts (Séance historique)"
            elif total_goals >= 9:
                tot_str = "Plus de 8.5 buts (Séance ultra-prolongée)"
            elif total_goals >= 8:
                tot_str = "Plus de 7.5 buts (Forte intensité en mort subite)"
            else:
                tot_str = "Plus de 6.5 buts (Standard tirs au but validé)"

            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            pen_text = f"Convertis avec précision (Plus de {(total_goals // 2) - 0.5} réussis)"
            confidence = round(94.0 + ((h1 + h2) % 50) / 10.0, 1)

            current_time = datetime.now().strftime("%H:%M")

            out = (
                f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                f"⚽ **Affiche :** {t1} vs {t2}\n"
                f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                f"📋 **Rapport d'expertise :**\n"
                f"• {analysis}\n\n"
                f"🎯 **1. Issue Validée :** {winner} 🏆\n\n"
                f"🎯 **2. Scores Exacts & Marchés :**\n"
                f"• **Option 1 (Principal) :** {t1} {s_t1} - {s_t2} {t2}\n"
                f"• **Option 2 (Alternatif) :** {t1} {alt_t1} - {alt_t2} {t2}\n"
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
