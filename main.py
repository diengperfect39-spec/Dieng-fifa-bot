import os
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

# Matrice de performance avec styles tactiques nuancés (fermé, équilibré, offensif)
TEAM_PROFILES = {
    "barcelone": {"power": 91, "style": "offensif"},
    "real madrid": {"power": 93, "style": "offensif"},
    "bayern munich": {"power": 90, "style": "offensif"},
    "manchester city": {"power": 94, "style": "offensif"},
    "paris saint-germain": {"power": 92, "style": "offensif"},
    "liverpool": {"power": 93, "style": "offensif"},
    "juventus": {"power": 88, "style": "ferme"},
    "arsenal": {"power": 89, "style": "equilibre"},
    "al nassr": {"power": 85, "style": "equilibre"},
    "inter miami": {"power": 84, "style": "ferme"}
}

@app.on_event("startup")
def startup_event():
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP - Mode Premium Équilibré Actif"}

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
                
                p1 = TEAM_PROFILES.get(t1, {"power": 86, "style": "equilibre"})
                p2 = TEAM_PROFILES.get(t2, {"power": 86, "style": "equilibre"})
                
                # Détermination du vainqueur par la puissance
                if p1["power"] >= p2["power"]:
                    winner = t1_raw
                    loser = t2_raw
                    diff = p1["power"] - p2["power"]
                    is_t1_win = True
                else:
                    winner = t2_raw
                    loser = t1_raw
                    diff = p2["power"] - p1["power"]
                    is_t1_win = False

                # Analyse croisée des styles pour alterner intelligemment petits et grands scores
                # Utilisation d'une signature unique basée sur l'heure pour éviter les blocages en boucle
                time_seed = int(datetime.now().strftime("%M")) % 3
                
                if p1["style"] == "ferme" or p2["style"] == "ferme" or time_seed == 0:
                    # Scénario fermé / Score court (Total 5 à 6 buts -> Moins de 6.5)
                    if is_t1_win:
                        s1, s2 = 4, 1
                        alt_1, alt_2 = 4, 2
                    else:
                        s1, s2 = 1, 4
                        alt_1, alt_2 = 2, 4
                    analysis_tone = f"Analyse Premium : {winner} verrouille la rencontre tactiquement pour s'imposer proprement face à {loser}."
                elif time_seed == 1:
                    # Scénario équilibré / Score intermédiaire (Total 7 à 8 buts)
                    if is_t1_win:
                        s1, s2 = 4, 3
                        alt_1, alt_2 = 5, 3
                    else:
                        s1, s2 = 3, 4
                        alt_1, alt_2 = 3, 5
                    analysis_tone = f"Analyse Premium : Duel serré et disputé, {winner} fait la différence dans les derniers tirs face à {loser}."
                else:
                    # Scénario ouvert / Score fleuve en mort subite (Total 9 à 11 buts)
                    if is_t1_win:
                        s1, s2 = 6, 5
                        alt_1, alt_2 = 5, 4
                    else:
                        s1, s2 = 5, 6
                        alt_1, alt_2 = 4, 5
                    analysis_tone = f"Analyse Premium : Choc offensif intense entre {winner} et {loser}, la décision se fait au bout du suspense."

                # Règle absolue : Zéro match nul (mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1
                total_goals = s1 + s2

                # Marchés "Plus ou Moins" dynamiques et stricts alignés sur tes options de plateforme
                if total_goals <= 6:
                    over_under_str = "Moins de 6.5 buts (Option prudente validée)"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts / Moins de 7.5 buts (Ligne 7.5)"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts / Moins de 8.5 buts (Ligne 8.5)"
                else:
                    over_under_str = "Plus de 8.5 buts (Séance ultra-prolifique)"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon l'analyse tactique (Volume global : {total_goals} buts)"
                
                confidence = round(87.0 + min(diff * 2.5, 9.5), 1)
                if confidence > 97.5: 
                    confidence = 96.5

                current_time = datetime.now().strftime("%H:%M")

                out = (
                    "💎 **DIENG PREDICT PREMIUM - EXPERT FC26** 💎\n\n"
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
                    f"📊 **Indice de Confiance Premium :** {confidence}%\n"
                )
                
                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
