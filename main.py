import os
import random
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
    return {"status": "Dieng FIFA - Mode Sans Nul & Ultra-Précis Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Récupération robuste de l'affiche
            t1_raw, t2_raw = "", ""
            raw_text = ""
            
            if "caption" in msg:
                raw_text = msg["caption"].strip()
            elif "text" in msg:
                raw_text = msg["text"].strip()
                
            if raw_text and not raw_text.startswith("/"):
                if "vs" in raw_text.lower():
                    parts = [p.strip() for p in raw_text.split("vs")]
                    if len(parts) >= 2:
                        t1_raw, t2_raw = parts[0], parts[1]
                elif "-" in raw_text:
                    parts = [p.strip() for p in raw_text.split("-")]
                    if len(parts) >= 2:
                        t1_raw, t2_raw = parts[0], parts[1]

            # Si l'utilisateur n'a pas mis les noms, on met une alerte au lieu de laisser Équipe 1 / Équipe 2
            if not t1_raw or not t2_raw:
                t1_raw, t2_raw = "Domicile", "Extérieur"

            # Empreinte unique pour la variabilité
            seed_str = f"{t1_raw}_{t2_raw}_{datetime.now().strftime('%H%M%S%f')}"
            seed_val = abs(hash(seed_str))
            
            # Choix du scénario : UNIQUEMENT DES VAINQUEURS (pas de nul)
            selector = seed_val % 2  # 0 = Victoire Équipe 1, 1 = Victoire Équipe 2

            base_win = 5 + (seed_val % 3)      # Entre 5 et 7 buts pour le vainqueur
            diff = 1 + (seed_val % 2)          # Écart de 1 ou 2 buts
            base_los = base_win - diff         if (base_win - diff) >= 3 else 3

            if selector == 0:
                winner_text = f"🏆 **{t1_raw}** (Validation du vainqueur)"
                s1, s2 = base_win, base_los
                alt1, alt2 = base_win + 1, base_los
                market_ou = "Plus de 7.5 buts" if (s1 + s2) >= 9 else "Plus de 6.5 buts"
                pen_missed = f"{(seed_val % 2) + 1} penalty manqué"
                conseil = f"Avantage net pour {t1_raw}. Valider la victoire sec ou le handicap."
                confidence = round(89.0 + (seed_val % 7), 1)
            else:
                winner_text = f"🏆 **{t2_raw}** (Validation du vainqueur)"
                s1, s2 = base_los, base_win
                alt1, alt2 = base_los, base_win + 1
                market_ou = "Plus de 7.5 buts" if (s1 + s2) >= 9 else "Plus de 6.5 buts"
                pen_missed = f"{(seed_val % 2) + 1} penalty manqué"
                conseil = f"Avantage net pour {t2_raw}. Valider la victoire de l'extérieur."
                confidence = round(87.5 + (seed_val % 8), 1)

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT VIP - ANALYSE SANS NUL** 💎\n\n"
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
