import os
import random
from datetime import datetime, timezone, timedelta
from flask import Flask, request as flask_request
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU")

bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).updater(None).build()

# Dictionnaire des forces des clubs sur FC26 Penalty
COEFFS_CLUBS = {
    "real madrid": 92, "manchester city": 91, "bayern munich": 90,
    "arsenal": 89, "barcelone": 88, "liverpool": 88,
    "juventus": 87, "psg": 87, "milan": 86, "inter": 86,
    "chelsea": 85, "atletico": 84, "dortmund": 84, "al nassr": 82
}

def get_club_score(nom_club):
    nom_net = nom_club.lower().strip()
    for cle, val in COEFFS_CLUBS.items():
        if cle in nom_net:
            return val
    return 83

async def handle_message(update: Update, context=None):
    if update.message and update.message.text:
        text = update.message.text.replace('/match', '').replace('/', '').strip()
        
        # Heure locale (GMT)
        dakar_time = datetime.now(timezone(timedelta(hours=0)))
        current_time_str = dakar_time.strftime("%H:%M")
        
        await update.message.chat.send_action(action="typing")
        
        if " vs " in text.lower():
            teams = text.split(" vs ")
            equipe_1 = teams[0].strip()
            equipe_2 = teams[1].strip()
        else:
            equipe_1 = "Équipe 1"
            equipe_2 = "Équipe 2"

        # Récupération des forces
        score_1 = get_club_score(equipe_1)
        score_2 = get_club_score(equipe_2)

        # Génération d'une graine neutre basée sur les noms pour casser tout biais de position
        seed_neutre = sum(ord(c) for c in equipe_1) + sum(ord(c) for c in equipe_2) + int(current_time_str.replace(":", ""))
        random.seed(seed_neutre)

        # Calcul pondéré mais neutre
puissance_1 = score_1 + random.uniform(-2.0, 2.0)
        puissance_2 = score_2 + random.uniform(-2.0, 2.0)

        # Attribution stricte : l'équipe avec la plus forte puissance gagne, peu importe sa position
        if puissance_1 >= puissance_2:
            vainqueur = equipe_1
            perdant = equipe_2
        else:
            vainqueur = equipe_2
            perdant = equipe_1

        # Matrice ultra-sélective des scores exacts (Le vainqueur est TOUJOURS placé en premier avec le plus grand score)
        matrice_scores = [
            (3, 2),
            (4, 2),
            (4, 3),
            (5, 3)
        ]
        sc_1, sc_2 = random.choice(matrice_scores)

        opt_1 = f"{vainqueur} {sc_1} - {sc_2} {perdant}"
        opt_2 = f"{vainqueur} {sc_1 + 1} - {sc_2 + 1} {perdant}"

        # Analyses expertes et professionnelles
        analyses_vip = [
            f"Analyse des métriques de tirs FC26 : {vainqueur} surclasse son adversaire grâce à une meilleure conversion des duels sous haute pression.",
            f"Lecture des données algorithmiques : {vainqueur} sécurise l'ascendant grâce à une supériorité validée de son portier sur les phases de tirs au but.",
            f"Étude comparative des performances : la régularité affichée par {vainqueur} dans la gestion des 11 mètres fait pencher la balance.",
            f"Indice de solidité tactique : {vainqueur} présente un profil technique supérieur pour verrouiller l'issue de la séance."
        ]
        analyse_retenue = random.choice(analyses_vip)

        confiance = round(random.uniform(98.1, 99.4), 1)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Analyse de Performance & Tirs au But (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            f"• *Analyse professionnelle :* {analyse_retenue}\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            f"• Option 1 (Tendance principale) : **{opt_1}**\n"
            f"• Option 2 (Alternative) : **{opt_2}**\n\n"
            f"📊 Indice de Confiance VIP : **{confiance}%**"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

application.add_handler(MessageHandler(filters.TEXT, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_data = flask_request.get_json(force=True)
    update = Update.de_json(json_data, bot)
    import asyncio
    asyncio.run(application.initialize())
    asyncio.run(application.process_update(update))
    return "OK"

@app.route("/")
def index():
    return "Bot Dieng-Fifa-Penalty Actif !", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
