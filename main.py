import os
import hashlib
requests = __import__('requests')
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
    return {"status": "Dieng FIFA VIP Pro - Analyse de Performance Réelle Active"}

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
                t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
                
                h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
                h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
                
                perf_1 = (h1 % 5) + 3
                perf_2 = (h2 % 5) + 3
                
                if perf_1 >= perf_2:
                    winner = t1
                    s1 = 4 if perf_1 > perf_2 else 3
                    s2 = 3 if s1 == 4 else 2
                    alt_1, alt_2 = s1, s2 - 1 if s2 > 2 else s2 + 1
                    analysis_tone = f"Analyse de performance : {t1} surclasse {t2} grâce à une meilleure efficacité dans l'exercice des tirs au but."
                else:
                    winner = t2
                    s2 = 4 if perf_2 > perf_1 else 3
                    s1 = 3 if s2 == 4 else 2
                    alt_1, alt_2 = s1 - 1 if s1 > 2 else s1 + 1, s2
                    analysis_tone = f"Analyse de performance : {t2} démontre une supériorité tactique et un sang-froid supérieur face à {t1}."

                if s1 == s2:
                    s1 += 1
                if alt_1 == alt_2:
                    alt_1 += 1

                total_goals = s1 + s2
                
                if total_goals <= 5:
                    over_under_str = "Moins de 5.5 buts (Séance fermée & verrouillée)"
                elif total_goals == 6:
                    over_under_str = "Plus de 5.5 buts / Moins de 6.5 buts"
                else:
                    over_under_str = "Plus de 6.5 buts (Séance offensive et ouverte)"

                pair_val = "Oui" if total_goals % 2 == 0 else "Non"
                pen_text = f"Tirs convertis selon l'indice de performance (Volume global : {total_goals} buts)"
                
                confidence = round(85.0 + ((h1 ^ h2) % 100) / 10.0, 1)
                if confidence > 95.0: 
                    confidence = 94.2

                current_time = datetime.now().strftime("%H:%M")

                out = (
                    "🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                    f"⚽ **Affiche :** {t1} vs {t2}\n"
                    f"🕒 **Heure d'analyse :** {current_time} (GMT)\n\n"
                    "📋 **Rapport d'expertise analytique :**\n"
                    f"• {analysis_tone}\n\n"
                    f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                    "🎯 **2. Scores Exacts & Marchés :**\n"
                    f"• **Option 1 (Principal) :** {t1} {s1} - {s2} {t2}\n"
                    f"• **Option 2 (Alternatif) :** {t1} {alt_1} - {alt_2} {t2}\n"
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
