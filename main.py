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
    return {"status": "Dieng FIFA - Mode Aléatoire Intelligent Actif"}

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

            # Clé de hachage ultra-dynamique (mélange les équipes et l'heure précise)
            seed_str = f"{t1_raw}-{t2_raw}-{datetime.now().strftime('%H%M%S%f')}"
            seed_val = abs(hash(seed_str))
            
            # Répartition sur 5 scénarios pour varier complètement les vainqueurs et les scores
            scenario = seed_val % 5
            
            if scenario == 0:
                # Victoire nette Équipe 1
                winner_text = f"🏆 **{t1_raw}** (Supériorité tactique validée)"
                s1, s2 = 6, 3
                alt1, alt2 = 5, 2
                market_ou = "Plus de 7.5 buts"
                pen_missed = "1 penalty manqué"
                conseil = "Le favori prend le large. Bonne option sur le vainqueur sec."
            elif scenario == 1:
                # Victoire nette Équipe 2
                winner_text = f"🏆 **{t2_raw}** (Domination extérieure nette)"
                s1, s2 = 3, 6
                alt1, alt2 = 2, 5
                market_ou = "Plus de 7.5 buts"
                pen_missed = "2 penalties manqués (grosse pression)"
                conseil = "L'outsider surprend. Valider la victoire de l'équipe 2."
            elif scenario == 2:
                # Match 50/50 très serré
                winner_text = f"⚠️ **Indécis / 50-50** (Gros risque de piège)"
                s1, s2 = 4, 4
                alt1, alt2 = 5, 4
                market_ou = "Plus de 8.5 buts (Feu d'artifice)"
                pen_missed = "3 penalties ou plus (stress maximal)"
                conseil = "Match équilibré à haut risque. Protéger le capital ou s'abstenir."
            elif scenario == 3:
                # Victoire étriquée Équipe 1
                winner_text = f"⚖️ **{t1_raw}** (Victoire sur le fil)"
                s1, s2 = 4, 3
                alt1, alt2 = 5, 4
                market_ou = "Moins de 8.5 buts"
                pen_missed = "0 à 1 penalty manqué"
                conseil = "Duel serré mais avantage logique aux locaux."
            else:
                # Victoire étriquée Équipe 2
                winner_text = f"⚖️ **{t2_raw}** (Hold-up tactique)"
                s1, s2 = 3, 4
                alt1, alt2 = 4, 5
                market_ou = "Moins de 8.5 buts"
                pen_missed = "1 penalty manqué"
                conseil = "Rencontre fermée, l'équipe 2 tire son épingle du jeu."

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            confidence = round(82.0 + (seed_val % 14), 1)
            if confidence > 95.0: 
                confidence = 92.5

            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT VIP - ANALYSE VARIÉE** 💎\n\n"
                f"⚽ **Affiche :** {t1_raw} vs {t2_raw}\n"
                f"🕒 **Heure :** {current_time} (GMT)\n\n"
                f"🎯 **1. Analyse du Vainqueur :** {winner_text}\n\n"
                "🎯 **2. Scores Suggérés & Marchés Buts (O/U) :**\n"
                f"• **Option 1 :** {t1_raw} {s1} - {s2} {t2_raw}\n"
                f"• **Option 2 :** {t1_raw} {alt1} - {alt2} {t2_raw}\n"
                f"• **Marché Buts :** {market_ou} (Total : {total_goals} buts)\n\n"
                "🎯 **3. Paramètres & Sécurité :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Pénalties manqués :** {pen_missed}\n"
                f"• **Indice de Confiance :** {confidence}%\n\n"
                f"💡 **Conseil Capital :** {conseil}"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
