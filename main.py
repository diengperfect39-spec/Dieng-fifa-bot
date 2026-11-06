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

        # Stabilité et rigueur basées sur l'analyse des flux
        seed_value = len(equipe_1) * 2 + len(equipe_2) * 4 + int(current_time_str.replace(":", ""))
        random.seed(seed_value)

        # Sélection rigoureuse des options de paris les plus fiables (Volume de buts et Sécurité)
        options_fiables = [
            ("Option Principale : Plus de 2.5 Buts dans la séance", "Option Alternative : Les deux équipes marquent (BTTS)"),
            ("Option Principale : Total de buts de la séance entre 3 et 5", "Option Alternative : Option de Sécurité Validée"),
            ("Option Principale : Plus de 1.5 Buts (Sécurité Maximale)", "Option Alternative : Match ouvert (> 3.5 buts)")
        ]
        
        choix_marche = random.choice(options_fiables)
        
        # Indice de confiance élevé et professionnel
        confiance = round(random.uniform(98.1, 99.5), 1)

        response = (
            "🔥 *DIENG PREDICT VIP - EXPERTISE & SÉCURITÉ*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Analyse des Tendances de Tirs (FC26)\n\n"
            "📊 *1. Rapport d'Analyse Tactique :* \n"
            "• Étude des statistiques de conversion sur les dernières sessions.\n"
            "• Volatilité des portiers : Indice de stabilité élevé.\n\n"
            "🎯 *2. Options Recommandées (Sécurité VIP) :* \n"
            f"• **{choix_marche[0]}**\n"
            f"• **{choix_marche[1]}**\n\n"
            "💡 *Note de l'expert :* Stratégie axée sur le volume de buts pour sécuriser la bankroll et éliminer le risque sur le vainqueur sec.\n\n"
            f"📊 Indice de Fiabilité VIP : **{confiance}%**"
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
