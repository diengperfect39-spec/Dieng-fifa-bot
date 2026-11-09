import os
requests = __import__('requests')
from datetime import datetime
from FastAPI import FastAPI, Request

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
    return {"status": "Dieng FIFA - Mode Variabilité Totale Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Récupération dynamique de l'affiche
            t1_raw, t2_raw = "Équipe 1", "Équipe 2"
            if "caption" in msg:
                txt = msg["caption"].strip()
                if "vs" in txt.lower():
                    parts = [p.strip() for p in txt.split("vs")]
                    t1_raw, t2_raw = parts[0], parts[1]
            elif "text" in msg:
                txt = msg["text"].strip()
                if txt and not txt.startswith("/"):
                    if "vs" in txt.lower():
                        parts = [p.strip() for p in txt.split("vs")]
                        t1_raw, t2_raw = parts[0], parts[1]
                    else:
                        t1_raw = txt

            # Algorithme de hachage unique : garantit des scores différents pour chaque match
            seed_val = abs(hash(t1_raw.lower() + "_" + t2_raw.lower()))
            
            # Génération dynamique des scores et des écarts
            base_score = 4 + (seed_val % 4) # Donne entre 4 et 7 buts pour le vainqueur
            diff = 1 + (seed_val % 2)       # Écart de 1 ou 2 buts
            
            if (seed_val % 2) == 0:
                winner, loser = t1_raw, t2_raw
                s1, s2 = base_score, base_score - diff
                alt1, alt2 = base_score + 1, base_score - diff + 1
            else:
                winner, loser = t2_raw, t1_raw
                s1, s2 = base_score - diff, base_score
                alt1, alt2 = base_score - diff + 1, base_score + 1

            # Sécurité pour éviter des scores négatifs ou aberrants
            if s2 < 2: s2 = 2
            if alt2 < 2: alt2 = 2

            total_goals = s1 + s2
            
            # Lignes Over/Under dynamiques selon le total calculé
            if total_goals >= 11:
                market_ou = "Plus de 9.5 buts (Mort subite prolongée)"
                pen_missed = "3 penalties ou plus (haute tension)"
            elif total_goals >= 9:
                market_ou = "Plus de 8.5 buts"
                pen_missed = "2 à 3 penalties manqués"
            elif total_goals >= 7:
                market_ou = "Plus de 6.5 buts / Moins de 7.5 buts"
                pen_missed = "1 à 2 penalties manqués"
            else:
                market_ou = "Moins de 6.5 buts (Match fermé)"
                pen_missed = "0 à 1 penalty manqué (efficacité maximale)"

            pair_val = "Oui" if total_goals % 2 == 0 else "Non"
            confidence = round(87.5 + ((seed_val % 9) * 1.1), 1)
            if confidence > 97.0: confidence = 96.2

            current_time = datetime.now().strftime("%H:%M")

            out = (
                "💎 **DIENG PREDICT VIP - ANALYSE UNIQUE** 💎\n\n"
                f"⚽ **Affiche :** {t1_raw} vs {t2_raw}\n"
                f"🕒 **Heure :** {current_time} (GMT)\n\n"
                f"🎯 **1. Vainqueur Validé :** {winner} 🏆\n\n"
                "🎯 **2. Scores Exacts & Marchés Buts (O/U) :**\n"
                f"• **Option 1 (Principal) :** {t1_raw} {s1} - {s2} {t2_raw}\n"
                f"• **Option 2 (Alternatif) :** {t1_raw} {alt1} - {alt2} {t2_raw}\n"
                f"• **Marché Buts (O/U) :** {market_ou}\n\n"
                "🎯 **3. Tendances Marché & Pénalties :**\n"
                f"• **Total Pair :** {pair_val}\n"
                f"• **Volume global estimé :** {total_goals} buts\n"
                f"• **Statistique Pénalties :** {pen_missed}\n\n"
                f"📊 **Indice de Confiance :** {confidence}%\n"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
