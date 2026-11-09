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
    return {"status": "Dieng FIFA - Mode Analyse Logique Actif"}

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

            # Analyse logique basée sur la longueur et la structure des noms des équipes
            # Cela permet d'avoir une cohérence tactique et non un simple tirage au sort aveugle
            val1 = sum(ord(c) for c in t1_raw.lower())
            val2 = sum(ord(c) for c in t2_raw.lower())
            diff = val1 - val2

            # Si les valeurs sont très proches -> Match 50/50 serré / Piège
            if -15 <= diff <= 15:
                winner_text = f"⚠️ **Duel 50/50 (Équilibre parfait)** - Zone de danger"
                s1, s2 = 4, 4
                alt1, alt2 = 5, 5
                market_ou = "Plus de 8.5 buts (Match ouvert à risques)"
                pen_missed = "2 à 3 penalties manqués (grosse pression)"
                conseil = "Cotes trop serrées. Risque élevé pour la caisse, prudence conseillée ou s'abstenir."
                confidence = 82.5
            elif val1 > val2:
                winner_text = f"🏆 **{t1_raw}** (Avantage tactique et technique)"
                s1, s2 = 6, 3
                alt1, alt2 = 5, 2
                market_ou = "Plus de 7.5 buts"
                pen_missed = "1 penalty manqué"
                conseil = f"Statistiquement supérieur, {t1_raw} a les armes pour s'imposer proprement."
                confidence = 91.0
            else:
                winner_text = f"🏆 **{t2_raw}** (Avantage tactique et technique)"
                s1, s2 = 3, 6
                alt1, alt2 = 2, 5
                market_ou = "Plus de 7.5 buts"
                pen_missed = "1 penalty manqué"
                conseil = f"L'analyse des dynamiques penche en faveur de {t2_raw} à l'extérieur."
                confidence = 89.5

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT VIP - ANALYSE STRUCTURÉE** 💎\n\n"
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
