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
    return {"status": "Dieng FIFA - Mode Variabilité Totale des Scores Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Récupération dynamique propre de l'affiche
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

            # Empreinte unique basée sur les noms et l'heure exacte pour générer des scores totalement variables
            seed_str = f"{t1_raw}_{t2_raw}_{datetime.now().strftime('%H%M%S%f')}"
            seed_val = abs(hash(seed_str))
            
            # Choix dynamique et neutre du scénario de match
            selector = seed_val % 3  # 0 = Avantage Équipe 1, 1 = Avantage Équipe 2, 2 = Duel serré 50/50

            # Génération de scores aléatoires mais logiques (entre 3 et 7 buts pour le vainqueur, écart de 1 à 3 buts)
            base_win = 4 + (seed_val % 3)      # Donne entre 4 et 6
            diff = 1 + ((seed_val // 7) % 2)   # Écart de 1 ou 2 buts
            base_los = max(2, base_win - diff)

            if selector == 0:
                winner_text = f"🏆 **{t1_raw}** (Ascendant tactique local)"
                s1, s2 = base_win, base_los
                alt1, alt2 = base_win + 1, max(2, base_los - 1)
                market_ou = "Plus de 6.5 buts" if (s1 + s2) < 9 else "Plus de 8.5 buts"
                pen_missed = f"{(seed_val % 2) + 1} penalty manqué"
                conseil = f"L'analyse des dynamiques penche en faveur de {t1_raw} à domicile."
                confidence = round(88.0 + (seed_val % 7), 1)
            elif selector == 1:
                winner_text = f"🏆 **{t2_raw}** (Ascendant tactique extérieur)"
                s1, s2 = base_los, base_win
                alt1, alt2 = max(2, base_los - 1), base_win + 1
                market_ou = "Plus de 6.5 buts" if (s1 + s2) < 9 else "Plus de 8.5 buts"
                pen_missed = f"{(seed_val % 2)} à {(seed_val % 2) + 1} penalties manqués"
                conseil = f"L'analyse des dynamiques penche en faveur de {t2_raw} à l'extérieur."
                confidence = round(86.5 + (seed_val % 8), 1)
            else:
                winner_text = f"⚠️ **Duel 50/50 (Équilibre parfait)** - Zone de danger"
                s1, s2 = 4, 4 if (seed_val % 2 == 0) else (5, 5)
                alt1, alt2 = s1 + 1, s2 + 1
                market_ou = "Plus de 8.5 buts (Match ouvert à risques)"
                pen_missed = "2 à 3 penalties manqués (grosse pression)"
                conseil = "Cotes trop serrées. Risque élevé pour la caisse, prudence conseillée ou s'abstenir."
                confidence = 82.0

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT VIP - ANALYSE UNIQUE & VARIÉE** 💎\n\n"
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
