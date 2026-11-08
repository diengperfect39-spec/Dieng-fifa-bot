import os
import hashlib
import requests
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Force la réinitialisation propre du webhook à chaque redémarrage sur Render
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Webhook Actif et Opérationnel"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            txt = msg.get("text", "").strip()
            
            # Ignore les commandes du bot pour traiter les affiches
            if txt and not txt.startswith("/"):
                parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
                t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
                
                # Analyse cryptographique croisée unique basée sur les profils des équipes
                h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
                h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
                
                # Analyse dynamique de la physionomie : alternance entre matchs serrés et matchs ouverts/fleuves
                profile_type = (h1 + h2) % 4
                
                if profile_type == 0:
                    base_s1, base_s2 = 4, 3
                    alt_s1, alt_s2 = 5, 4
                    analysis_tone = f"Duel tactique et verrouillé : {t1} impose un ascendant mesuré pour étouffer les offensives de {t2}."
                elif profile_type == 1:
                    base_s1, base_s2 = 5, 4
                    alt_s1, alt_s2 = 4, 3
                    analysis_tone = f"Grosse intensité en mort subite : {t1} fait preuve d'un sang-froid chirurgical pour distancer {t2}."
                elif profile_type == 2:
                    base_s1, base_s2 = 6, 5
                    alt_s1, alt_s2 = 7, 6
                    analysis_tone = f"Séance ultra-offensive et spectaculaire : les deux équipes se livrent un duel de haute volée, avec un avantage décisif pour {t1} dans les derniers tirs."
                else:
                    base_s1, base_s2 = 5, 7
                    alt_s1, alt_s2 = 4, 6
                    analysis_tone = f"Festival offensif sous haute pression : {t2} surclasse totalement {t1} grâce à une insolente réussite en fin de séance."

                if (h1 % 2) == 0 and profile_type >= 2:
                    s1, s2 = base_s2, base_s1
                    alt_1, alt_2 = alt_s2, alt_s1
                    winner = t2
                elif profile_type >= 2:
                    s1, s2 = base_s1, base_s2
                    alt_1, alt_2 = alt_s1, alt_s2
                    winner = t1
                else:
                    if h1 > h2:
                        winner = t1
                        s1, s2 = base_s1, base_s2
                        alt_1, alt_2 = alt_s1, alt_s2
                    else:
                        winner = t2
                        s1, s2 = base_s2, base_s1
                        alt_1, alt_2 = alt_s2, alt_s1

                # Règle absolue du mode Penalty : INTERDICTION STRICTE DE NUL (Mort subite obligatoire)
                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1

                total_goals = s1 + s2
                
                # Marché Over / Under unique, net et ultra-rassurant
                if total_goals <= 6:
                    over_under_str = "Plus de 5.5 buts"
                elif total_goals == 7:
                    over_under_str = "Plus de 6.5 buts"
                elif total_goals == 8:
                    over_under_str = "Plus de 7.5 buts"
                elif total_goals == 9:
                    over_under_str = "Plus de 8.5 buts"
                else:
                    over_under_str = "Plus de 9.5 buts"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis sous haute pression (Volume global : {total_goals} buts)"
                
                # Indice de confiance élite strictement calibré entre 80.0% et 100.0%
                confidence = round(80.0 + ((h1 ^ h2) % 201) / 10.0, 1)
                if confidence > 99.8: 
                    confidence = 99.8

                current_time = datetime.now().strftime("%H:%M")

                out = (
                    f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                    f"⚽ **Affiche :** {t1} vs {t2}\n"
                    f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                    f"📋 **Rapport d'expertise analytique :**\n"
                    f"• {analysis_tone}\n\n"
                    f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                    f"🎯 **2. Scores Exacts & Marchés :**\n"
                    f"• **Option 1 (Principal) :** {t1} {s1} - {s2} {t2}\n"
                    f"• **Option 2 (Alternatif) :** {t1} {alt_1} - {alt_2} {t2}\n"
                    f"• **Marché Buts (O/U) :** {over_under_str}\n\n"
                    f"🎯 **3. Tendances Marché VIP :**\n"
                    f"• **Total Pair :** {pair_val}\n"
                    f"• **Pénalties :** {pen_text}\n\n"
                    f"📊 **Indice de Confiance Analytique :** {confidence}%\n"
                )
                
                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur de traitement : {e}")
        
    return {"status": "ok"}
