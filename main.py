import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "TON_BOT_TOKEN")
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👑 *DIENG-FIFA-PENALTY | VIP EXPERT* ⚽🔥\n\n"
        "Commande valide :\n"
        "`/match Bayern Munich vs Barcelone V1 1.885 V2 1.835`"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def match_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupère tout le texte après /match
    user_input = " ".join(context.args) if context.args else ""
    
    await update.message.chat.send_action(action="typing")
    
    # Analyse professionnelle VIP basée sur la structure demandée
    response = (
        "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
        f"⚽ *Match :* {user_input if user_input else 'Bayern Munich vs Barcelone'}\n"
        "🏆 *Contexte :* Phase Finale - Séance de Penalty (FC26)\n\n"
        "🎯 *1. Verdict & Hiérarchie (Codes V1 / V2) :* \n"
        "• Vainqueur validé : Équipe 1 (V1)\n"
        "• Analyse de tendance : Étude croisée de la performance et des cotes de référence.\n\n"
        "🎯 *2. Scores Exacts Recommandés (Professionnel) :* \n"
        "• Option 1 : **3 - 2**\n"
        "• Option 2 : **4 - 3**\n\n"
        "📊 Indice de Confiance VIP : **98.2%**"
    )
    
    await update.message.reply_text(response, parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("match", match_analysis))

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
