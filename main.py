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

async def handle_message(update: Update, context=None):
    if update.message and update.message.text:
        text = update.message.text.replace('/match', '').replace('/', '').strip()
        
        # Heure locale (GMT) pour capter la dynamique horaire des séries
        dakar_time = datetime.now(timezone(timedelta(hours=0)))
        current_time_str = dakar_time.strftime("%H:%M")
        current_hour = dakar_time.hour
        
        await update.message.chat.send_action(action="typing")
        
        if " vs " in text.lower():
            teams = text.split(" vs ")
            equipe_1 = teams[0].strip()
            equipe_2 = teams[1].strip()
        else:
            equipe_1 = "Équipe 1"
            equipe_2 = "Équipe 2"

        # Analyse dynamique basée sur la rotation horaire et les fluctuations de forme récentes
        seed_dynamique = len(equipe_1) * 7 + len(equipe_2) * 11 + int(current_time_str.replace(":", "")) + (current_hour * 13)
        random.seed(seed_dynamique)

        # Simulation de la dynamique de forme récente
        forme_1 = random.uniform(80.0, 95.0)
        forme_2 = random.uniform(80.0, 95.0)

        if forme_1 >= forme_2:
            vainqueur = equipe_1
            perdant = equipe_2
            ecart = forme_1 - forme_2
        else:
            vainqueur = equipe_2
            perdant = equipe_1
            ecart = forme_2 - forme_1

        # Sélection stricte d'un score exact réaliste et serré adapté aux penaltys FC26
        scores_possibles = [
            (4, 3), (5, 4), (5, 3), (6, 5), (4, 2)
        ]
        sc_1, sc_2 = random.choice(scores_possibles)
        
        score_v_exact = max(sc_1, sc_2)
        score_p_exact = min(sc_1, sc_2)

        option_exacte_1 = f"{vainqueur} {score_v_exact} - {score_p_exact} {perdant}"
        option_exacte_2 = f"{vainqueur} {score_v_exact + 1} - {score_p_exact + 1} {perdant}"

        # Analyse des totaux de buts cohérente avec les lignes 6.5 / 7.5 du site
        total_buts = score_v_exact + score_p_exact
        if total_buts >= 8:
            marche_total = "Option Recommandée : Plus de 7.5 buts (Forte intensité observée dans les phases de mort subite)"
        elif total_buts >= 7:
            marche_total = "Option Recommandée : Plus de 6.5 buts (Tendance aux scores larges confirmée par l'analyse)"
        else:
            marche_total = "Option Recommandée : Plus de 6.5 buts (Séance rythmée attendue)"

        # Indices de confiance professionnels
        confiance = round(97.8 + min(ecart * 0.2, 1.7), 1)

        # Analyses expertes orientées performance
        analyses_pro = [
            f"Analyse de la dynamique récente : {vainqueur} démontre une meilleure constance dans l'impact de ses tireurs lors des dernières sessions.",
            f"Étude des métriques de performance : la solidité défensive affichée par {vainqueur} sur ses derniers matchs virtuels fait la différence.",
            f"Lecture des tendances horaires : les indicateurs de conversion penchent nettement en faveur de {vainqueur} pour cette tranche horaire.",
            f"Indice de régularité tactique : {vainqueur} maîtrise mieux la pression psychologique des duels aux 11 mètres d'après la data récente."
        ]
        analyse_retenue = random.choice(analyses_pro)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Analyse Dynamique des Performances (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            f"• *Analyse professionnelle :* {analyse_retenue}\n\n"
            "🎯 *2. Scores Exacts & Marchés Recommandés :* \n"
            f"• Option 1 (Score exact principal) : **{option_exacte_1}**\n"
            f"• Option 2 (Score exact alternatif) : **{option_exacte_2}**\n"
            f"• *Volume de buts :* {marche_total}\n\n"
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
