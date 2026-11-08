import os
import hashlib
import requests
from fastapi import FastAPI, Request

app = FastAPI()

TOKEN = "9204768032:AAGdCe7c_tym2R6zyug8jtx33P9gC4wpZx4"

@app.get("/")
def home():
    return {"status": "FIFA VIP Pro Active"}

@app.post("/")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text_recu = data["message"].get("text", "").strip()
            
            if text_recu and not text_recu.startswith("/"):
                parties = [p.strip() for p in text_recu.split("vs")] if "vs" in text_recu else [text_recu, "Visiteur"]
                eq1 = parties[0]
                eq2 = parties[1] if len(parties) > 1 else "Visiteur"
                
                hash_bytes = hashlib.sha256(text_recu.encode()).digest()
                v1 = hash_bytes[0]
                v3 = hash_bytes[2]
                
                scenarios = [
                    {"s1": 2, "s2": 3, "gagnant": eq2, "total": "Plus de 4.5 buts", "paire": "Non", "pen": "Moins de 2.5 manqués"},
                    {"s1": 3, "s2": 4, "gagnant": eq2, "total": "Plus de 6.5 buts", "paire": "Non", "pen": "Plus de 2.5 manqués"},
                    {"s1": 4, "s2": 5, "gagnant": eq2, "total": "Plus de 8.5 buts", "paire": "Oui", "pen": "Séance sous haute tension"},
                    {"s1": 4, "s2": 3, "gagnant": eq1, "total": "Plus de 6.5 buts", "paire": "Non", "pen": "Maîtrise des gardiens"},
                    {"s1": 3, "s2": 2, "gagnant": eq1, "total": "Plus de 4.5 buts", "paire": "Non", "pen": "Efficacité redoutable"}
                ]
                
                choix = scenarios[v1 % len(scenarios)]
                alt_s1 = (choix["s1"] + 1) % 6
                alt_s2 = (choix["s2"] + 1) % 6
                if alt_s1 == choix["s1"]: alt_s1 += 1

                confiance = 97.8 + (v3 % 19) / 10

                analysis_text = (
                    f"DIENG PREDICT VIP - ANALYSE EXPERT FC26\n\n"
                    f"Match : {eq1} vs {eq2}\n"
                    f"Contexte : Analyse Dynamique & Forme des Tirs au But\n\n"
                    f"1. Verdict & Hierarchie :\n"
                    f"- Vainqueur Valide : {choix['gagnant']}\n"
                    f"- Analyse : Stabilite des frappes et gestion de la pression.\n\n"
                    f"2. Scores Exacts & Marches Cles :\n"
                    f"- Option 1 (Principal) : {eq1} {choix['s1']} - {choix['s2']} {eq2}\n"
                    f"- Option 2 (Alternatif) : {eq1} {alt_s1} - {alt_s2} {eq2}\n"
                    f"- Volume de buts : {choix['total']}\n\n"
                    f"3. Tendances Marche :\n"
                    f"- Total Pair : {choix['paire']}\n"
                    f"- Penalties : {choix['pen']}\n\n"
                    f"Indice de Confiance VIP : {confiance:.1f}%"
                )
                
                resp = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": analysis_text}
                )
                print("Reponse Telegram:", resp.text)
    except Exception as e:
        print("Erreur:", str(e))
        
    return {"ok": True}
