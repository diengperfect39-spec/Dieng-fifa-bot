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

# Hiérarchie fixe et absolue des forces des clubs sur FC26 Penalty
COEFFS_BASE = {
    "real madrid": 95, "manchester city": 94, "bayern munich": 93,
    "arsenal": 91, "barcelone": 90, "liverpool": 90,
    "juventus": 88, "psg": 88, "milan": 86, "inter": 86,
    "chelsea": 85, "atletico": 84, "inter miami": 82, "al nassr": 78
}

def get_power(club):
    nom = club.lower().strip()
    for k, v in COEFFS_BASE.items():
        if k in nom:
            return v
    return 83

async def handle_message(update: Update, context=None):
    if update.message and update.message.text:
        text = update.message.text.replace('/match', '').replace('/', '').strip()
        
        dakar_time = datetime.now(timezone(timedelta(hours=0)))
        current_time_str = dakar_time.strftime("%H:%M")
        
        await update.message.chat.send_action(action="typing")
        
        if " vs " in text.lower():
            teams = text.split(" vs ")
            eq_a = teams[0].strip()
            eq_b = teams[1].strip()
        else:
            eq_a = "Équipe 1"
            eq_b = "Équipe 2"

        p_a = get_power(eq_a)
        p_b = get_power(eq_b)

        # Hiérarchie stricte et neutre (indépendante de l'ordre de saisie)
        if p_a > p_b:
            vainqueur = eq_a
            perdant = eq_b
            ecart = p_a - p_b
        elif p_b > p_a:
            vainqueur = eq_b
            perdant = eq_a
            ecart = p_b - p_a
        else:
            if eq_a.lower() <= eq_b.lower():
                vainqueur = eq_a
                perdant = eq_b
            else:
                vainqueur = eq_b
                perdant = eq_a
            ecart = 2

        # GRAINE ULTRA-STABLE : 
        # Tant qu'on est à la même minute et avec les mêmes équipes (peu importe l'ordre), 
        # le résultat exact et l'analyse restent rigoureusement identiques.
        noms_tries = sorted([eq_a.lower(), eq_b.lower()])
        seed_stabilité = sum(ord(c) for nom in noms_tries for c in nom) + int(current_time_str.replace(":", ""))
        random.seed(seed_stabilité)

        scores_possibles = [
            (4, 3), (5, 4), (5, 3), (6, 5), (4, 2)
        ]
        sc_1, sc_2 = random.choice(scores_possibles)
        
        score_v = max(sc_1, sc_2)
        score_p = min(sc_1, sc_2)

        opt_1 = f"{vainqueur} {score_v} - {score_p} {perdant}"
        opt_2 = f"{vainqueur} {score_v + 1} - {score_p + 1} {perdant}"

        total_buts = score_v + score_p
        if total_buts >= 8:
            marche_total = "Option Recommandée : Plus de 7.5 buts (Forte intensité en fin de séance)"
        else:
            marche_total = "Option Recommandée : Plus de 6.5 buts (Séance rythmée attendue)"

        confiance = round(98.0 + min(ecart * 0.1, 1.5), 1)

        analyses_pro = [
            f"Analyse de la dynamique récente : {vainqueur} démontre une supériorité constante dans l'impact de ses tireurs lors des dernières sessions.",
            f"Étude des métriques de performance : la solidité affichée par {vainqueur} sur ses derniers matchs virtuels fait la différence.",
            f"Lecture des tendances de la simulation : les indicateurs de conversion penchent nettement en faveur de {vainqueur}.",
            f"Indice de régularité tactique : {vainqueur} maîtrise mieux la pression psychologique des duels aux 11 mètres."
        ]
        analyse_retenue = random.choice(analyses_pro)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {eq_a} vs {eq_b}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Analyse Statique & Performance (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            f"• *Analyse professionnelle :* {analyse_retenue}\n\n"
            "🎯 *2. Scores Exacts & Marchés Recommandés :* \n"
            f"• Option 1 (Score exact principal) : **{opt_1}**\n"
            f"• Option 2 (Score exact alternatif) : **{opt_2}**\n"
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
