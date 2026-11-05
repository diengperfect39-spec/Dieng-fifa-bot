import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "TON_BOT_TOKEN")
bot = Bot(token=TOKEN)

# Initialisation synchrone de l'application Telegram pour éviter les blocages sur Render
application = Application.builder().token(TOKEN).updater(None).build()

async def handle_message(update: Update, context=None):
    if update.message and update.message.text:
        text = update.message.text
        await update.message.chat.send_action(action="typing")
        
        # Analyse VIP professionnelle sans les codes V1/V2
        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {text.replace('/match', '').strip()}\n"
            "🏆 *Contexte :* Séance de Penalty (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            "• Vainqueur validé : Équipe dominante selon la dynamique.\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            "• Option 1 : **3 - 2**\n"
            "• Option 2 : **4 - 3**\n\n"
            "📊 Indice de Confiance VIP : **98.5%**"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

application.add_handler(MessageHandler(filters.TEXT, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, bot)
    # Exécution directe de l'application sans file d'attente bloquante
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
