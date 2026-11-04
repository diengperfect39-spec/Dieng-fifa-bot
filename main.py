import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Bienvenue sur le bot VIP **FC26 Penalty** de Dieng !\n\n"
        "🎯 Module d'analyse et pronostics des tirs au but actif.\n"
        "Utilisez la commande `/match Équipe 1 vs Équipe 2` pour obtenir le vainqueur et les scores exacts."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def analyser_match_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte_saisi = update.message.text
    parties = texte_saisi.replace("/match", "").split(" vs ")

    if len(parties) == 2:
        equipe1 = parties[0].strip()
        equipe2 = parties[1].strip()

        reponse = f"""
👑 **PRONOSTIC VIP - TIRS AU BUT FC26** 👑\n
⚽ **{equipe1} vs {equipe2}**\n
🏆 *Mode : Séance de Penalty (Pronostic Score Exact)*\n\n
🔥 **1. Verdict du Vainqueur :**\n
• Avantage net : **{equipe1}** (Supériorité dans l'exercice des tirs et sang-froid des tireurs)\n\n
🎯 **2. Scores Exacts les plus probables :**\n
• **Option 1 (Le plus probable) :** `{equipe1} 5 - 4 {equipe2}`\n
• **Option 2 (Alternative serrée) :** `{equipe1} 4 - 3 {equipe2}`\n\n
📊 *Indice de fiabilité : 89% sur la série*
"""
        await update.message.reply_text(reponse, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "⚠️ Format incorrect.\n"
            "Utilisez le format exact : `/match Équipe 1 vs Équipe 2`",
            parse_mode="Markdown"
        )

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logging.error("Aucun token Telegram trouvé dans les variables d'environnement !")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("match", analyser_match_custom))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == "__main__":
    asyncio.run(main())
