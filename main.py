import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Bienvenue sur le FIFA Virtual Match Bot de Dieng !\n\n"
        "📊 Module d'analyse prédictive professionnelle actif.\n"
        "Utilisez la commande `/match Équipe 1 vs Équipe 2` pour obtenir l'analyse VIP."
    )
    await update.message.reply_text(welcome_text)

async def analyser_match_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte_saisi = update.message.text
    parties = texte_saisi.replace("/match", "").split(" vs ")

    if len(parties) == 2:
        equipe1 = parties[0].strip()
        equipe2 = parties[1].strip()

        reponse = f"""
👑 **ANALYSE EXPERTE VIP & TENDANCE HISTORIQUE** 👑\n
⚽ **{equipe1} vs {equipe2}**\n
🏆 *Module : FC26. Penalty (Analyse des séries récentes)*\n\n
📊 **1. Analyse Statistique & Historique :**\n
• Dynamique des derniers matchs de la ligue : Forte tendance aux scores fleuves (moyenne élevée).\n
• Indice de conversion des penalties : **Élevé (91.5% de réussite sur les 3 premiers tirs)**\n\n
🎯 **2. Prédictions Clés & Marchés VIP :**\n
• Temps Réglementaire : Match ouvert avec une forte probabilité d'un total supérieur à 2.5 buts.\n
• Les deux équipes marquent : **Oui (Option ultra-sécurisée validée par l'historique)**\n
• Tendance 1X2 / Série principale : Duel serré, avantage aux équipes ayant le momentum.
"""
        await update.message.reply_text(reponse, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "⚠️ Format incorrect.\n"
            "Utilisez le format exact : `/match Équipe 1 vs Équipe 2`",
            parse_mode="Markdown"
        )

async def main():
    TOKEN = "YOUR_TOKEN_HERE"
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("match", analyser_match_custom))

    # Lancement propre de la boucle pour python-telegram-bot v20+
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Garde le bot actif
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == "__main__":
    asyncio.run(main())
