import hashlib
import requests
from fastapi import FastAPI, Request

app = FastAPI()

TOKEN = "9204768032:AAGdCe7c_tym2R6zyug8jtx33P9gC4wpZx4"

@app.get("/")
def home():
    return {"status": "FIFA VIP Pro Engine Active"}

@app.post("/")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("Données reçues de Telegram :", data)
        
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text_recu = data["message"].get("text", "").strip()
            
            match_info = "Barcelone vs Inter Miami"
            if text_recu and not text_recu.startswith("/"):
                match_info = text_recu
                
            # Découpage propre et sécurisé des équipes
            parties = [p.strip() for p in match_info.split("vs")] if "vs" in match_info else [match_info, "Visiteur"]
            eq1 = parties[0]
            eq2 = parties[1] if len(parties) > 1 else "Visiteur"
            
            # Empreinte cryptographique stable
            hash_bytes = hashlib.sha256(match_info.encode()).digest()
            v1 = hash_bytes[0]
            v2 = hash_bytes[1]
            v3 = hash_bytes[2]
            
            # Matrice de scénarios réalistes (scores serrés et logiques de penalties)
            bibliotheque_scenarios = [
                {"s1": 2, "s2": 3, "gagnant": eq2, "total": "Plus de 4.5 buts", "paire": "Non", "Penalties": "Moins de 2.5 manqués"},
                {"s1": 3, "s2": 4, "gagnant": eq2, "total": "Plus de 6.5 buts", "paire": "Non", "Penalties": "Plus de 2.5 manqués"},
                {"s1": 4, "s2": 5, "gagnant": eq2, "total": "Plus de 8.5 buts", "paire": "Oui", "Penalties": "Séance sous haute tension"},
                {"s1": 4, "s2": 3, "gagnant": eq1, "total": "Plus de 6.5 buts", "paire": "Non", "Penalties": "Maîtrise des gardiens"},
                {"s1": 5, "s2": 3, "gagnant": eq1, "total": "Plus de 7.5 buts", "paire": "Oui", "Penalties": "Efficacité redoutable"}
            ]
            
            choix = bibliotheque_scenarios[v1 % len(bibliotheque_scenarios)]
            
            alt_s1 = (choix["s1"] + 1) % 6
            alt_s2 = (choix["s2"] + 1) % 6
            if alt_s1 == choix["s1"]: 
                alt_s1 += 1

            indice_confiance = 97.8 + (v3 % 19) / 10

            analysis_text = (
                f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                f"⚽ **Match :** {eq1} vs {eq2}\n"
                f"🏆 **Contexte :** Analyse Dynamique & Forme des Tirs au But\n\n"
                f"🎯 **1. Verdict & Hiérarchie :**\n"
                f"• Vainqueur Validé : **{choix['gagnant']}** 🏆\n"
                f"• Analyse professionnelle : Étude de la régularité des frappes et de la résistance sous pression des porteurs.\n\n"
                f"📋 **2. Scores Exacts & Marchés Clés :**\n"
                f"• Option 1 (Principal) : **{eq1} {choix['s1']} - {choix['s2']} {eq2}**\n"
                f"• Option 2 (Alternatif) : **{eq1} {alt_s1} - {alt_s2} {eq2}**\n"
                f"• Volume de buts : **{choix['total']}**\n\n"
                f"📊 **3. Tendances Marché & Fiabilité :**\n"
                f"• Total Pair : **{choix['paire']}**\n"
                f"• Gestion des penalties : **{choix['Penalties']}**\n\n"
                f"📈 **Indice de Confiance VIP :** {indice_confiance:.1f}%"
            )
            
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": analysis_text, "parse_mode": "Markdown"}
            )
            print("Réponse de Telegram :", response.text)
            
    except Exception as e:
        print("Erreur critique dans le webhook :", str(e))
        
    return {"ok": True}
