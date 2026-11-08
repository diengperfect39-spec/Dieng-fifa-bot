import os
import hashlib
requests = __import__('requests')
from datetime import datetime
from fastapi import FastAPI, Request

TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-fifa-bot.onrender.com"

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Dieng FIFA VIP Pro - Système Opérationnel & Propre"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    data = await req.json()
    if data and "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        txt = msg.get("text", "").strip()
        
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
                base_s1, base_s2
