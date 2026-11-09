import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

# Matrice de performance réelle des équipes (Attaque / Défense FC26)
TEAM_STATS = {
    "barcelone": {"att": 88, "def": 84},
    "real madrid": {"att": 90, "def": 85},
    "bayern munich": {"att": 89, "def": 83},
    "manchester city": {"att": 91, "def": 86},
    "paris saint-germain": {"att": 88, "def": 82},
    "juventus": {"att": 86, "def": 86},
    "arsenal": {"att": 87, "def": 85},
    "al nassr": {"att": 84, "def": 78},
    "inter miami": {"att": 83, "def": 77}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Moteur de Performance FC26 Actif"}

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
                
                # Récupération des stats réelles ou attribution d'un standard équilibré
                stats1 = TEAM_STATS.get(t1, {"att": 85, "def": 83})
                stats2 = TEAM_STATS.get(t2, {"att": 85, "def": 83})
                
                # Calcul de performance pondéré
                power1 = stats1["att"] * 0.6 + stats1["def"] * 0.4
                power2 = stats2["att"] * 0.6 + stats2["def"] * 0.4
                
                # Détermination rigoureuse du vainqueur selon la performance pure
                if power1 >= power2:
                    winner = t1_raw
                    s1 = 4 if (power1 - power2) > 2 else 3
                    s2 = 2 if s1 == 4 else 1
                    alt_1, alt_2 = s1, s2 + 1
                    analysis_tone = f"Analyse de performance : {t1_raw} affiche un indice offensif supérieur et prend l'ascendance tactique sur {t2_raw}."
                else:
                    winner = t2_raw
                    s2 = 4 if (power2 - power1) > 2 else 3
                    s1 = 2 if s2 == 4 else 1
                    alt_1, alt_2 = s1 + 1, s2
                    analysis_tone = f"Analyse de performance : {t2_raw} démontre une meilleure solidité et surclasse {t1_raw} dans la décisive."

                # Règle absolue du mode Penalty : Zéro match nul (mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1

                total_goals = s1 + s2
                
                # Alignement strict sur tes lignes officielles (6.5, 7.5, 8.5)
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts"
                else:
                    over_under_str = "Plus de 8.5 buts"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon les stats de performance (Volume global : {total_goals} buts)"
                
                # Indice de confiance calculé selon l'écart de performance
                diff = abs(power1 - power2)
                confidence = round(85.0 + min(diff * 2.5, 12.5), 1)
                if confidence > 97.5: 
                    confidence = 96.8

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
