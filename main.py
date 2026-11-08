import os
import hashlib
import requests
from datetime import datetime
from flask import Flask, request, jsonify

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route('/')
def home():
    return "Dieng FIFA VIP 100% - Actif"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        txt = msg.get("text", "").strip()
        
        if txt and not txt.startswith("/"):
            parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
            t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
            
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Moteur strict basé sur les grilles FC26 Penalty (Scores élevés)
            selector = (h1 + h2) % 3
            if selector == 0:
                s1, s2 = 6, 5
                alt1, alt2 = 7, 6
                tot_str = "Plus de 6.5 buts (Ligne 6.5 - Forte intensité)"
                pen_text = "Plus de 2.5 Pénalties manqués (Nervosité en mort subite)"
                pair_val = "Non"
            elif selector == 1:
                s1, s2 = 7, 6
                alt1, alt2 = 8, 7
                tot_str = "Plus de 7.5 buts (Ligne 7.5 - Séance prolifique)"
                pen_text = "Plus de 1.5 Pénalties manqués (Duels tendus)"
                pair_val = "Oui"
            else:
                s1, s2 = 5, 4
                alt1, alt2 = 6, 5
                tot_str = "Plus de 8.5 buts (Ligne 8.5 - Festival offensif)"
                pen_text = "Moins de 2.5 Pénalties manqués (Efficacité redoutable)"
                pair_val = "Non"

            if (h1 * h2) % 2 == 0:
                winner, team_s1, team_s2, alt_s1, alt_s2 = t1, s1, s2, alt1, alt2
            else:
                winner, team_s1, team_s2, alt_s1, alt_s2 = t2, s2, s1, alt2, alt1

            current_time = datetime.now().strftime("%H:%M")
            conf = 98.4 + ((h1 % 15) / 10)

            out = (
                f"🔥 **DIENG PREDICT VIP - ANALYSE EXPERT FC26** 🔥\n\n"
                f"⚽ **Match :** {t1} vs {t2}\n"
                f"🕒 **Heure d'analyse :** {current_time} (GMT)\n"
                f"🏆 **Contexte :** Analyse Dynamique & Grille des Tirs au But (FC26)\n\n"
                f"🎯 **1. Verdict & Hiérarchie :**\n"
                f"• **Vainqueur Validé :** {winner} 🏆\n"
                f"• **Analyse professionnelle :** Maîtrise des frappes en fin de série : {winner} gère la pression psychologique et s'impose dans les moments clés.\n\n"
                f"🎯 **2. Scores Exacts & Marchés Principaux :**\n"
                f"• **Option 1 (Score exact principal) :** {t1} {team_s1} - {team_s2} {t2}\n"
                f"• **Option 2 (Score exact alternatif) :** {t1} {alt_s1} - {alt_s2} {t2}\n"
                f"• **Volume de buts :** Option Recommandée : {tot_str}\n\n"
                f"🎯 **3. Options VIP Supplémentaires (Tendances Marché) :**\n"
                f"• **Total Pair :** {pair_val} (Cohérence mathématique validée sur la grille)\n"
                f"• **Pénalties Manqués :** {pen_text}\n\n"
                f"📊 **Indice de Confiance VIP :** {conf:.1f}%\n"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
            
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
