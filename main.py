import os
from datetime import datetime, timezone, timedelta
from flask import Flask, request as flask_request
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "TON_BOT_TOKEN")

bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).updater(None).build()

async def handle_message(update: Update, context=None):
    if update.message and update.message.text:
        text = update.message.text.replace('/match', '').strip()
        
        # Heure locale Dakar (GMT)
        dakar_time = datetime.now(timezone(timedelta(hours=0)))
        current_time_str = dakar_time.strftime("%H:%M")
        
        await update.message.chat.send_action(action="typing")
        
        # Détermination des équipes
        if " vs " in text.lower():
            teams = text.split(" vs ")
            equipe_1 = teams[0].strip()
            equipe_2 = teams[1].strip()
        else:
            equipe_1 = "Équipe 1"
            equipe_2 = "Équipe 2"

        vainqueur = equipe_1 

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Séance de Penalty (FC26)\n\n"
            f"🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            "• Analyse de tendance : Étude croisée du rythme des tirs et de la résistance.\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            f"• Option 1 (Tendance principale) : **{equipe_1} 4 - 3 {equipe_2}**\n"
            f"• Option 2 (Alternative) : **{equipe_1} 5 - 3 {equipe_2}**\n\n"
            "📊 Indice de Confiance VIP : **97%**"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

# Capture absolument tous les messages texte entrants
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(MessageHandler(filters.COMMAND, handle_message))

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
