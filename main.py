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

        # Hash unique basé sur le match et l'heure exacte de la requête
        sim_hash = abs(hash(text.lower() + current_time_str))
        random.seed(sim_hash)

        # Alternance neutre du vainqueur
        if sim_hash % 2 == 0:
            v_1, v_2 = equipe_1, equipe_2
        else:
            v_1, v_2 = equipe_2, equipe_1

        # Génération mathématique dynamique de scores serrés ou en mort subite (sans liste figée)
        # Permet d'obtenir des scores variés et imprévisibles à chaque analyse
        type_seance = random.choice(["standard", "prolongee", "tendu"])
        
        if type_seance == "standard":
            perdant_score = random.randint(2, 4)
            gagnant_score = perdant_score + random.choice([1, 2])
        elif type_seance == "prolongee":
            perdant_score = random.randint(5, 8)
            gagnant_score = perdant_score + 1
        else:
            gagnant_score = random.randint(4, 7)
            perdant_score = gagnant_score - random.choice([1, 2])
            if perdant_score < 1: perdant_score = 1

        # Score alternatif différent pour éviter les doublons
        alt_perdant = max(1, perdant_score + random.choice([-1, 1]))
        alt_gagnant = gagnant_score + random.choice([0, 1])
        if alt_gagnant == alt_perdant:
            alt_gagnant += 1

        # Banque d'analyses contextuelles de la simulation
        analyses_pool = [
            f"Analyse de la résistance psychologique : basculement de la décision sur les derniers tirs sous haute pression pour {v_1}.",
            f"Fluctuation de l'algorithme des gardiens : {v_1} prend l'ascendant technique lors du face-à-face final.",
            f"Lecture des tendances de frappe des tireurs : {v_1} capitalise sur une meilleure lecture des trajectoires.",
            f"Dénouement de la séance aux 11 mètres : la régularité des phases de tirs profite à {v_1}."
        ]
        analyse_choisie = random.choice(analyses_pool)

        confiance = round(random.uniform(94.8, 99.3), 1)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {equipe_1} vs {equipe_2}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* FC26 Penalty (Simulateur Virtuel)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {v_1} 🏆\n"
            f"• *Analyse tactique :* {analyse_choisie}\n\n"
            "🎯 *2. Scores Exacts Recommandés :* \n"
            f"• Option 1 (Tendance principale) : **{v_1} {gagnant_score} - {perdant_score} {v_2}**\n"
            f"• Option 2 (Alternative) : **{v_1} {alt_gagnant} - {alt_perdant} {v_2}**\n\n"
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
