import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

# Matrice analytique complète et rigoureuse des équipes
TEAM_METRICS = {
    "barcelone": {"pen_acc": 91, "gk_save": 84, "momentum": 89},
    "real madrid": {"pen_acc": 92, "gk_save": 85, "momentum": 90},
    "bayern munich": {"pen_acc": 90, "gk_save": 83, "momentum": 88},
    "manchester city": {"pen_acc": 93, "gk_save": 86, "momentum": 91},
    "paris saint-germain": {"pen_acc": 89, "gk_save": 82, "momentum": 87},
    "juventus": {"pen_acc": 87, "gk_save": 88, "momentum": 88},
    "arsenal": {"pen_acc": 88, "gk_save": 85, "momentum": 87},
    "al nassr": {"pen_acc": 85, "gk_save": 79, "momentum": 84},
    "inter miami": {"pen_acc": 84, "gk_save": 78, "momentum": 83}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Système Analytique Intégral Actif"}

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
                
                m1 = TEAM_METRICS.get(t1, {"pen_acc": 86, "gk_save": 83, "momentum": 85})
                m2 = TEAM_METRICS.get(t2, {"pen_acc": 86, "gk_save": 83, "momentum": 85})
                
                # Calcul mathématique strict de la performance
                score_1 = (m1["pen_acc"] * 0.5) + (m1["momentum"] * 0.3) - (m2["gk_save"] * 0.2)
                score_2 = (m2["pen_acc"] * 0.5) + (m2["momentum"] * 0.3) - (m1["gk_save"] * 0.2)
                
                if score_1 >= score_2:
                    winner = t1_raw
                    loser = t2_raw
                    diff = score_1 - score_2
                else:
                    winner = t2_raw
                    loser = t1_raw
                    diff = score_2 - score_1

                # Attribution des scores exacts selon l'écart analytique
                if diff > 3.0:
                    if winner == t1_raw:
                        s1, s2 = 5, 2
                        alt_1, alt_2 = 4, 2
                    else:
                        s1, s2 = 2, 5
                        alt_1, alt_2 = 2, 4
                elif diff > 1.2:
                    if winner == t1_raw:
                        s1, s2 = 4, 3
                        alt_1, alt_2 = 5, 3
                    else:
                        s1, s2 = 3, 4
                        alt_1, alt_2 = 3, 5
                else:
                    if winner == t1_raw:
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

                analysis_tone = f"Analyse de performance : {winner} surclasse {loser} grâce à un meilleur taux de conversion des penalties et une supériorité dans le duel des gardiens."

                # Sélection rigoureuse des lignes Over / Under officielles (6.5, 7.5, 8.5)
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts / Moins de 7.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts / Moins de 8.5 buts"
                else:
                    over_under_str = "Plus de 8.5 buts"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon l'indice d'efficacité (Volume global : {total_goals} buts)"
                
                confidence = round(83.0 + min(diff * 4.0, 14.0), 1)
                if confidence > 97.0: 
                    confidence = 96.2

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
