import os
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
    return {"status": "Dieng FIFA - Mode Analyse Réaliste Actif"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Récupération de l'affiche via le texte ou la légende
            match_name = "Match FC26 Penalty"
            if "caption" in msg:
                match_name = msg["caption"].strip()
            elif "text" in msg:
                txt = msg["text"].strip()
                if txt and not txt.startswith("/"):
                    match_name = txt

            current_time = datetime.now().strftime("%H:%M")

            # Rapport basé sur l'analyse lucide et la protection du capital (sans faux scores inventés)
            out = (
                "🛡️ **DIENG STRATÉGIE - ANALYSE & SÉCURITÉ** 🛡️\n\n"
                f"⚽ **Affiche :** {match_name}\n"
                f"🕒 **Heure :** {current_time} (GMT)\n\n"
                "📊 **1. Lecture des Cotes & Rapport de Force :**\n"
                "• Analyse comparative des cotes 1X2 et des lignes de buts en cours.\n"
                "• Identification des dynamiques de marché (repérage des favoris logiques ou des duels 50/50 à haut risque).\n\n"
                "🎯 **2. Pistes de Sécurité Capital :**\n"
                "• **Option Buts (O/U) :** Privilégier les lignes intermédiaires sécurisées (comme le *Plus de 6.5* ou le *Moins de 8.5*) selon la tendance des cotes affichées.\n"
                "• **Option Vainqueur :** Attention aux cotes trop serrées (équilibres parfaits). S'abstenir ou miser prudemment si le match est un piège statistique.\n\n"
                "⚠️ **Règle d'or :** Pas de score exact inventé. On protège la caisse en misant uniquement sur les tendances logiques du marché."
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
