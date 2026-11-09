import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

# Matrice de performance officielle (Attaque / Défense / Forme FC26)
TEAM_METRICS = {
    "barcelone": {"power": 91},
    "real madrid": {"power": 93},
    "bayern munich": {"power": 90},
    "manchester city": {"power": 94},
    "paris saint-germain": {"power": 92},
    "juventus": {"power": 88},
    "arsenal": {"power": 89},
    "al nassr": {"power": 85},
    "inter miami": {"power": 84}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Correctif Vainqueur Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            txt = msg.get("text", "").strip()
            
            if txt and not txt.startswith("/"):
                parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
                t1_raw, t2_raw = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
                
                t1 = t1_raw.lower()
                t2 = t2_raw.lower()
                
                # Récupération directe de la puissance réelle de chaque équipe
                p1 = TEAM_METRICS.get(t1, {"power": 86})["power"]
                p2 = TEAM_METRICS.get(t2, {"power": 86})["power"]
                
                # Comparaison directe et sans ambiguïté pour désigner le vrai vainqueur
                if p1 >= p2:
                    winner = t1_raw
                    loser = t2_raw
                    diff = p1 - p2
                    is_team1_winner = True
                else:
                    winner = t2_raw
                    loser = t1_raw
                    diff = p2 - p1
                    is_team1_winner = False

                # Attribution des scores exacts selon le vainqueur réel
                if diff >= 3:
                    if is_team1_winner:
                        s1, s2 = 5, 2
                        alt_1, alt_2 = 4, 2
                    else:
                        s1, s2 = 2, 5
                        alt_1, alt_2 = 2, 4
                elif diff >= 1:
                    if is_team1_winner:
                        s1, s2 = 4, 3
                        alt_1, alt_2 = 5, 3
                    else:
                        s1, s2 = 3, 4
                        alt_1, alt_2 = 3, 5
                else:
                    # Séance très serrée en mort subite (ex: 4-5 ou 5-4)
                    if is_team1_winner:
                        s1, s2 = 5, 4
                        alt_1, alt_2 = 6, 5
                    else:
                        s1, s2 = 4, 5
                        alt_1, alt_2 = 5, 6

                # Règle absolue : Zéro match nul (mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1
                total_goals = s1 + s2

                analysis_tone = f"Analyse de performance : {winner} prend l'ascendant tactique et s'impose face à {loser} grâce à une meilleure efficacité globale."

                # Sélection rigoureuse des lignes Over / Under (6.5, 7.5, 8.5)
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts / Moins de 7.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts / Moins de 8.5 buts"
                else:
                    over_under_str = "Plus de 8.5 buts"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon l'analyse (Volume global : {total_goals} buts)"
                
                confidence = round(85.0 + min(diff * 3.0, 12.0), 1)
                if confidence > 97.0: 
                    confidence = 95.8

                current_time = datetime.now().strftime("%H:%M")

                out = (
                    "🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                    f"⚽ **Affiche :** {t1_raw} vs {t2_raw}\n"
                    f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                    "📋 **Rapport d'expertise analytique :**\n"
                    f"• {analysis_tone}\n\n"
                    f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                    "🎯 **2. Scores Exacts & Marchés :**\n"
                    f"• **Option 1 (Principal) :** {t1_raw} {s1} - {s2} {t2_raw}\n"
                    f"• **Option 2 (Alternatif) :** {t1_raw} {alt_1} - {alt_2} {t2_raw}\n"
                    f"• **Marché Buts (O/U) :** {over_under_str}\n\n"
                    "🎯 **3. Tendances Marché VIP :**\n"
                    f"• **Total Pair :** {pair_val}\n"
                    f"• **Pénalties :** {pen_text}\n\n"
                    f"📊 **Indice de Confiance Analytique :** {confidence}%\n"
                )
                
                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
