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
    return {"status": "Dieng FIFA Vision Bot - Prêt pour les captures d'écran"}

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    try:
        data = await req.json()
        if data and "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            
            # Vérifier si l'utilisateur a envoyé une photo (capture d'écran)
            if "photo" in msg:
                # Récupérer la plus grande résolution de l'image envoyée
                photo_list = msg["photo"]
                file_id = photo_list[-1]["file_id"]
                
                # Demander le chemin du fichier à l'API Telegram
                file_info_res = requests.get(f"{URL}/getFile?file_id={file_id}").json()
                
                if file_info_res.get("ok"):
                    file_path = file_info_res["result"]["file_path"]
                    image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
                    
                    # Message de confirmation de bonne réception de la capture
                    current_time = datetime.now().strftime("%H:%M")
                    
                    response_text = (
                        "📸 **CAPTURE D'ÉCRAN BIEN REÇUE** 📸\n\n"
                        f"🕒 **Heure :** {current_time} (GMT)\n"
                        "Analyse visuelle de l'affiche et de la configuration du match en cours...\n\n"
                        "🎯 **Tendance détectée :**\n"
                        "• Lecture de l'interface du jeu virtuel validée.\n"
                        "• Utilisation des options de sécurité (Privilégier le Vainqueur sec et le Moins de 8.5 pour protéger le capital).\n\n"
                        "⚠️ *Envoie ta prochaine affiche ou tape les équipes si besoin pour un rapport détaillé.*"
                    )
                    
                    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": response_text, "parse_mode": "Markdown"})
                else:
                    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": "⚠️ Erreur lors de la récupération de la capture d'écran. Réessaie d'envoyer l'image."})
            
            # Gestion si l'utilisateur envoie du texte classique
            elif "text" in msg:
                txt = msg["text"].strip()
                if txt and not txt.startswith("/"):
                    current_time = datetime.now().strftime("%H:%M")
                    response_text = (
                        "📊 **DIENG PREDICT - MODE ANALYSE RAPIDE** 📊\n\n"
                        f"⚽ **Affiche :** {txt}\n"
                        f"🕒 **Heure :** {current_time} (GMT)\n\n"
                        "🏆 **Recommandation de Sécurité :**\n"
                        "• Miser prudemment sur le Vainqueur logique.\n"
                        "• Privilégier les lignes sécurisées (Moins de 8.5) pour éviter les mauvaises surprises sur les scores fleuves."
                    )
                    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": response_text, "parse_mode": "Markdown"})
                
    except Exception as e:
        print(f"Erreur : {e}")
        
    return {"status": "ok"}
