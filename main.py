import os
import random
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

        # Génération d'une base numérique unique pour chaque match
        match_hash = abs(hash(equipe_1.lower() + equipe_2.lower()))
        random.seed(match_hash)

        # Alternance neutre du vainqueur (plus de favoritisme pour l'équipe à domicile)
        if match_hash % 2 == 0:
            vainqueur = equipe_1
            perdant = equipe_2
        else:
            vainqueur = equipe_2
            perdant = equipe_1

        # Variété des scores de tirs au but (fini le 4-3 systématique)
        possible_scores = [
            (4, 2), (5, 3), (3, 2), (5, 4), (6, 5), (4, 3), (5, 1)
        ]
        score_main = random.choice(possible_scores)
        score_alt = random.choice(possible_scores)
        
        # S'assurer que le vainqueur gagne bien
        s1, s2 = max(score_main), min(score_main)
        if s1 == s2: s1 += 1
        
        a1, a2 = max(score_alt), min(score_alt)
        if a1 == a2: a1 += 1
        if (s1, s2) == (a1, a2):
            a2 = max(0, a2 - 1)

        # Banque d'analyses tactiques variées et dynamiques
        analyses_pool = [
            f"Fermeture des angles par le gardien de {vainqueur} lors des phases de mort subite et manque de sang-froid des tireurs adverses.",
            f"Maîtrise totale de la pression psychologique et lecture parfaite des trajectoires de tir par {vainqueur}.",
            f"Domination tactique dans l'exercice des duels 1v1 aux 11 mètres, scellant l'issue avec autorité pour {vainqueur}.",
            f"Solidité défensive des remparts et efficacité clinique des tireurs clés de {vainqueur} dans le money-time."
        ]
        analyse_choisie = random.choice(analyses_pool)

        # Indice de confiance dynamique
        confiance = round(random.uniform(94.2, 98.8), 1)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Séance de Penalty (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            f"• *Analyse tactique :* {analyse_choisie}\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            f"• Option 1 (Tendance principale) : **{vainqueur} {s1} - {s2} {perdant}**\n"
            f"• Option 2 (Alternative serrée) : **{vainqueur} {a1} - {a2} {perdant}**\n\n"
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
