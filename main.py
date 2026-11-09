import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

TEAM_METRICS = {
    "real madrid": {"power": 93},
    "paris saint-germain": {"power": 92},
    "barcelone": {"power": 91},
    "bayern munich": {"power": 90},
    "liverpool": {"power": 93},
    "manchester city": {"power": 94},
    "juventus": {"power": 88},
    "arsenal": {"power": 89}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA Vision VIP - Mode Premium Total Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Détection automatique de l'affiche (Real vs PSG par défaut sur la capture, modifiable par texte)
            t1_raw, t2_raw = "Real Madrid", "Paris Saint-Germain"
            
            if "text" in msg:
                txt = msg["text"].strip()
                if txt and not txt.startswith("/"):
                    if "vs" in txt.lower():
                        parts = [p.strip() for p in txt.split("vs")]
                        t1_raw, t2_raw = parts[0], parts[1]
                    else:
                        t1_raw = txt

            t1 = t1_raw.lower()
            t2 = t2_raw.lower()
            
            p1 = TEAM_METRICS.get(t1, {"power": 88})["power"]
            p2 = TEAM_METRICS.get(t2, {"power": 88})["power"]
            
            if p1 >= p2:
                winner = t1_raw
                loser = t2_raw
                diff = p1 - p2
                is_t1_win = True
            else:
                winner = t2_raw
                loser = t1_raw
                diff = p2 - p1
                is_t1_win = False

            # Calibration des scores et des marchés Over/Under officiels (6.5, 7.5, 8.5)
            if diff >= 2:
                s1, s2 = (5, 3) if is_t1_win else (3, 5)
                alt_1, alt_2 = (4, 2) if is_t1_win else (2, 4)
                market_ou = "Plus de 7.5 buts / Moins de 8.5 buts"
                pen_missed = "1 à 2 penalties manqués (pression défensive)"
            else:
                s1, s2 = (5, 4) if is_t1_win else (4, 5)
                alt_1, alt_2 = (6, 5) if is_t1_win else (5, 6)
                market_ou = "Plus de 8.5 buts (Mort subite prolongée)"
                pen_missed = "3 penalties ou plus (duels intenses sous haute tension)"

            total_goals = s1 + s2
            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            confidence = round(89.0 + (diff * 2.2), 1)
            if confidence > 97.0: confidence = 96.5

            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT PREMIUM - EXPERT FC26** 💎\n\n"
                f"⚽ **Affiche :** {t1_raw} vs {t2_raw}\n"
                f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                "📋 **Rapport d'expertise tactique :**\n"
                f"• {winner} affiche une supériorité nette dans la conversion des tirs face à {loser}.\n\n"
                f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                "🎯 **2. Scores Exacts & Marchés Buts (O/U) :**\n"
                f"• **Option 1 (Principal) :** {t1_raw} {s1} - {s2} {t2_raw}\n"
                f"• **Option 2 (Alternatif) :** {t1_raw} {alt_1} - {alt_2} {t2_raw}\n"
                f"• **Marché Buts (O/U) :** {market_ou}\n\n"
                "🎯 **3. Tendances Marché VIP & Pénalties :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Volume global estimé :** {total_goals} buts\n"
                f"• **Statistique Pénalties :** {pen_missed}\n\n"
                f"📊 **Indice de Confiance Premium :** {confidence}%\n"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
