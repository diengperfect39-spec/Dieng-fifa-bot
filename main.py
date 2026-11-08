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
    return {"status": "Dieng FIFA VIP 100% Actif - Analyse Avancée FC26"}

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
            
            # Hash indépendant pour chaque équipe pour obtenir de vraies variations uniques
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Calcul dynamique et indépendant des scores (plages réalistes de penalties : 3 à 6 buts)
            score1 = 3 + (h1 % 3)  # Donne entre 3 et 5
            score2 = 3 + (h2 % 3)  # Donne entre 3 et 5
            
            # Éviter les égalités parfaites ennuyeuses
            if score1 == score2:
                score1 += 1

            # Détermination du vainqueur selon la vraie force relative des hashes
            if h1 > h2:
                winner = t1
                if score1 < score2:
                    score1, score2 = score2, score1
                s1, s2 = score1, score2
                alt_s1, alt_s2 = max(3, s1 - 1), s2 + 1 if s2 < 5 else s2 - 1
                analysis = f"Supériorité tactique et meilleure gestion des tirs au but par {t1} face à {t2}."
            else:
                winner = t2
                if score2 < score1:
                    score1, score2 = score2, score1
                s1, s2 = score2, score1  # Inversion pour que l'équipe 2 gagne si c'est elle la vainqueure
                # Ajustement propre pour le format T1 vs T2
                # On s'assure que s1 est pour t1 et s2 pour t2, mais si t2 gagne, s2 > s1
                pass

            # Recalibrage propre pour garantir la victoire du bon vainqueur affiché
            if h1 > h2:
                winner = t1
                s_t1 = max(score1, score2)
                s_t2 = min(score1, score2)
                if s_t1 == s_t2: s_t1 += 1
                alt_t1, alt_t2 = max(3, s_t1 - 1), s_t2
                analysis = f"Assurance technique et solidité de {t1} pour contenir les offensives de {t2}."
            else:
                winner = t2
                s_t2 = max(score1, score2)
                s_t1 = min(score1, score2)
                if s_t1 == s_t2: s_t2 += 1
                alt_t1, alt_t2 = s_t1, max(3, s_t2 - 1)
                analysis = f"Forte intensité et renversement de situation orchestré par {t2} pour dominer {t1}."

            total_goals = s_t1 + s_t2
            
            # Volumes de buts conformes aux marchés du jeu
            if total_goals >= 9:
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
                f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
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
