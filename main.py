import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

TEAM_METRICS = {
    "barcelone": {"att": 91, "def": 85},
    "real madrid": {"att": 93, "def": 86},
    "bayern munich": {"att": 90, "def": 84},
    "manchester city": {"att": 94, "def": 87},
    "paris saint-germain": {"att": 92, "def": 83},
    "juventus": {"att": 87, "def": 88},
    "arsenal": {"att": 88, "def": 85},
    "al nassr": {"att": 85, "def": 80},
    "inter miami": {"att": 84, "def": 78}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Moteur Équilibré Petits/Gros Scores Actif"}

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
                
                m1 = TEAM_METRICS.get(t1, {"att": 86, "def": 83})
                m2 = TEAM_METRICS.get(t2, {"att": 86, "def": 83})
                
                power1 = m1["att"] * 0.7 + m1["def"] * 0.3
                power2 = m2["att"] * 0.7 + m2["def"] * 0.3
                
                # Signature unique pour varier dynamiquement entre match fermé, moyen ou ouvert
                match_profile = abs(hash(t1_raw + t2_raw + datetime.now().strftime("%H:%M"))) % 3
                
                if power1 >= power2:
                    winner = t1_raw
                    loser = t2_raw
                    diff = power1 - power2
                    is_t1_win = True
                else:
                    winner = t2_raw
                    loser = t1_raw
                    diff = power2 - power1
                    is_t1_win = False

                # Attribution des scores selon le profil du match (fermé, moyen ou ouvert)
                if match_profile == 0:
                    # Match fermé / score court (ex: 4-1 ou 4-2 -> Total 5 à 6 buts -> Moins de 6.5)
                    if diff > 2.5:
                        s1, s2 = (4, 1) if is_t1_win else (1, 4)
                        alt_1, alt_2 = (4, 2) if is_t1_win else (2, 4)
                    else:
                        s1, s2 = (4, 2) if is_t1_win else (2, 4)
                        alt_1, alt_2 = (3, 2) if is_t1_win else (2, 3)
                    analysis_tone = f"Analyse de performance : {winner} maîtrise son sujet et verrouille la rencontre pour s'imposer face à {loser}."
                elif match_profile == 1:
                    # Match disputé / score intermédiaire (ex: 4-3 ou 5-3 -> Total 7 à 8 buts)
                    if is_t1_win:
                        s1, s2 = 4, 3
                        alt_1, alt_2 = 5, 3
                    else:
                        s1, s2 = 3, 4
                        alt_1, alt_2 = 3, 5
                    analysis_tone = f"Analyse de performance : Duel tactique serré, {winner} fait la différence dans les derniers tirs face à {loser}."
                else:
                    # Match ouvert / score fleuve en mort subite (ex: 5-4 ou 6-5 -> Total 9 à 11 buts)
                    if is_t1_win:
                        s1, s2 = 5, 4
                        alt_1, alt_2 = 6, 5
                    else:
                        s1, s2 = 4, 5
                        alt_1, alt_2 = 5, 6
                    analysis_tone = f"Analyse de performance : Choc très offensif entre {winner} et {loser}, la décision se fait au bout du suspense en mort subite."

                # Règle absolue : Zéro match nul (mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1
                total_goals = s1 + s2

                # Marché O/U strict aligné sur le total réel
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts (Séance fermée & contrôlée)"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts"
                else:
                    over_under_str = "Plus de 8.5 buts (Séance ultra-prolifique)"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon l'analyse tactique (Volume global : {total_goals} buts)"
                
                confidence = round(84.0 + min(diff * 3.0, 12.0), 1)
                if confidence > 97.0: 
                    confidence = 95.5

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
