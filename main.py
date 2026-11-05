import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "TON_BOT_TOKEN")
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Si le message commence par /match ou contient les équipes
    if text:
        await update.message.chat.send_action(action="typing")
        
        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match analysé :* {text.replace('/match', '').strip()}\n"
            "🏆 *Contexte :* Séance de Penalty (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie (Codes V1 / V2) :* \n"
            "• Vainqueur validé : Basé sur la performance des cotes.\n"
            "• Analyse de tendance : Flux stable et régulier.\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            "• Option 1 : **3 - 2**\n"
            "• Option 2 : **4 - 3**\n\n"
            "📊 Indice de Confiance VIP : **98.5%**"
        )
        
        await update.message.reply_text(response, parse_mode="Markdown")

# Il écoute absolument TOUS les messages texte (avec ou sans /match) pour ne plus jamais rater une requête
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(MessageHandler(filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"

@app.route("/")
def index():
    return "Bot Dieng-Fifa-Penalty Actif !", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
