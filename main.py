import os
import hashlib
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Analyseur Expert Dynamique Actif"}

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
            
            # Analyse cryptographique croisée unique pour chaque confrontation
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Calcul de la dynamique de tirs au but (garantit des scores serrés de type 4-3, 5-4, 6-5...)
            raw_s1 = (h1 % 4) + 3
            raw_s2 = (h2 % 4) + 3
            
            # Règle absolue : INTERDICTION FORMELLE DE NUL (Mort subite obligatoire)
            if raw_s1 == raw_s2:
                if (h1 % 2) == 0:
                    raw_s1 += 1
                else:
                    raw_s2 += 1

            # Détermination rigoureuse du vainqueur et des options alternatives
            if raw_s1 > raw_s2:
                winner = t1
                s1, s2 = raw_s1, raw_s2
                alt_s1 = s1 if s1 > 4 else s1 + 1
                alt_s2 = s2 if s2 > 3 else s2 + 1
                if alt_s1 == alt_s2: alt_s1 += 1
                analysis = f"Analyse tactique : {t1} impose un rythme asphyxiant et démontre une maîtrise supérieure des duels psychologiques face à {t2}."
            else:
                winner = t2
                s1, s2 = raw_s1, raw_s2 # s1 pour t1, s2 pour t2 (où s2 > s1)
                alt_s1 = s1 if s1 > 3 else s1 + 1
                alt_s2 = s2 if s2 > 4 else s2 + 1
                if alt_s1 == alt_s2: alt_s2 += 1
                analysis = f"Analyse tactique : Efficacité chirurgicale et renversement de situation orchestré par {t2} pour crucifier {t1} en mort subite."

            total_goals = s1 + s2
            
            # Marchés de buts professionnels (lignes 6.5, 7.5, 8.5+)
            if total_goals >= 11:
                tot_str = "Plus de 9.5 buts (Séance historique en mort subite)"
            elif total_goals >= 9:
                tot_str = "Plus de 8.5 buts (Forte intensité prolongée)"
            elif total_goals >= 8:
                tot_str = "Plus de 7.5 buts (Animation offensive élevée)"
            else:
                tot_str = "Plus de 6.5 buts (Standard tirs au but validé)"

            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            pen_text = f"Convertis sous pression (Plus de {(total_goals // 2) - 0.5} réussis)"
            
            # Indice de confiance dynamique non figé (s'adapte au profil de l'affiche, de 86.5% à 97.8%)
            dynamic_confidence = round(86.5 + ((h1 ^ h2) % 114) / 10.0, 1)

            current_time = datetime.now().strftime("%H:%M")

            out = (
                f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                f"⚽ **Affiche :** {t1} vs {t2}\n"
                f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                f"📋 **Rapport d'expertise pro :**\n"
                f"• {analysis}\n\n"
                f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                f"🎯 **2. Scores Exacts & Marchés :**\n"
                f"• **Option 1 (Principal) :** {t1} {s1} - {s2} {t2}\n"
                f"• **Option 2 (Alternatif) :** {t1} {alt_s1} - {alt_s2} {t2}\n"
                f"• **Volume de buts :** {tot_str}\n\n"
                f"🎯 **3. Tendances Marché VIP :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Pénalties :** {pen_text}\n\n"
                f"📊 **Indice de Confiance :** {dynamic_confidence}%\n"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
            
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})
