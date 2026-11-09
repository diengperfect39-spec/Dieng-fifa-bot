import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

# Matrice complète avec profils tactiques réels (Attaque, Défense, Tendance de score)
TEAM_PROFILES = {
    "barcelone": {"att": 91, "def": 85, "style": "ouvert"},
    "real madrid": {"att": 93, "def": 86, "style": "prolifique"},
    "bayern munich": {"att": 90, "def": 84, "style": "ouvert"},
    "manchester city": {"att": 94, "def": 87, "style": "prolifique"},
    "paris saint-germain": {"att": 92, "def": 83, "style": "prolifique"},
    "juventus": {"att": 87, "def": 88, "style": "ferme"},
    "arsenal": {"att": 88, "def": 85, "style": "equilibre"},
    "al nassr": {"att": 85, "def": 80, "style": "ouvert"},
    "inter miami": {"att": 84, "def": 78, "style": "ferme"}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Profils Dynamiques Adaptatifs Actifs"}

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
                
                p1 = TEAM_PROFILES.get(t1, {"att": 86, "def": 83, "style": "equilibre"})
                p2 = TEAM_PROFILES.get(t2, {"att": 86, "def": 83, "style": "equilibre"})
                
                # Calcul de la puissance globale
                power1 = p1["att"] * 0.6 + p1["def"] * 0.4
                power2 = p2["att"] * 0.6 + p2["def"] * 0.4
                
                if power1 >= power2:
                    winner = t1_raw
                    loser = t2_raw
                    diff = power1 - power2
                    is_team1_winner = True
                else:
                    winner = t2_raw
                    loser = t1_raw
                    diff = power2 - power1
                    is_team1_winner = False

                # Adaptation fine du score selon le style combiné des équipes
                combined_style = p1["style"] + "_" + p2["style"]
                
                if "ferme" in combined_style or diff > 4:
                    # Match plus fermé ou domination tactique contrôlée
                    if is_team1_winner:
                        s1, s2 = 4, 2
                        alt_1, alt_2 = 3, 2
                    else:
                        s1, s2 = 2, 4
                        alt_1, alt_2 = 2, 3
                    analysis_tone = f"Analyse de performance : {winner} impose une assise défensive rigoureuse et contrôle les débats face à {loser}."
                elif "prolifique" in combined_style or diff < 1.0:
                    # Match très ouvert, intense et poussé en mort subite (gros scores)
                    if is_team1_winner:
                        s1, s2 = 6, 5
                        alt_1, alt_2 = 5, 4
                    else:
                        s1, s2 = 5, 6
                        alt_1, alt_2 = 4, 5
                    analysis_tone = f"Analyse de performance : Choc très ouvert entre {winner} et {loser}, la décision se fait au bout du suspense en mort subite."
                else:
                    # Match équilibré standard mais animé
                    if is_team1_winner:
                        s1, s2 = 4, 3
                        alt_1, alt_2 = 5, 4
                    else:
                        s1, s2 = 3, 4
                        alt_1, alt_2 = 4, 5
                    analysis_tone = f"Analyse de performance : Duel serré où {winner} fait parler sa fraîcheur tactique pour dominer {loser}."

                # Règle absolue : Zéro match nul (mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1
                total_goals = s1 + s2

                # Attribution précise et flexible du marché O/U selon le total réel du match
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts (Séance fermée)"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts / Moins de 7.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts / Moins de 8.5 buts"
                else:
                    over_under_str = "Plus de 8.5 buts (Séance ultra-prolifique)"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon le profil tactique (Volume global : {total_goals} buts)"
                
                confidence = round(84.0 + min(diff * 3.5, 12.0), 1)
                if confidence > 97.0: 
                    confidence = 96.0

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
