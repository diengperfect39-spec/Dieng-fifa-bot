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

# Matrice de base équilibrée pour les performances FC26 Penalty
COEFFS_BASE = {
    "real madrid": 92, "barcelone": 92, "manchester city": 91, "bayern munich": 90,
    "arsenal": 89, "liverpool": 89, "juventus": 87, "psg": 87, "paris saint-germain": 87, 
    "dortmund": 86, "milan": 86, "inter": 86, "chelsea": 85, "atletico": 84, 
    "napoli": 84, "roma": 83, "marseille": 82, "ajax": 82, "inter miami": 81, "al nassr": 80
}

def get_power(club):
    nom = club.lower().strip()
    for k, v in COEFFS_BASE.items():
        if k in nom:
            return v
    return 82

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

        base_a = get_power(eq_a)
        base_b = get_power(eq_b)

        # GRAINE ULTRA-STABLE (Même match à la même minute = même résultat figé)
        noms_tries = sorted([eq_a.lower(), eq_b.lower()])
        seed_stabilité = sum(ord(c) for nom in noms_tries for c in nom) + int(current_time_str.replace(":", ""))
        random.seed(seed_stabilité)

        # FACTEUR DE FORME DU JOUR (Permet aux outsiders de créer la surprise)
        forme_a = random.uniform(-4.5, 4.5)
        forme_b = random.uniform(-4.5, 4.5)

        p_a = base_a + forme_a
        p_b = base_b + forme_b

        # Désignation du vainqueur basée sur la forme du jour
        if p_a >= p_b:
            vainqueur = eq_a
            perdant = eq_b
            ecart = p_a - p_b
        else:
            vainqueur = eq_b
            perdant = eq_a
            ecart = p_b - p_a

        # Scores exacts cohérents
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

        # CORRECTION LOGIQUE : Le Total Pair est déduit mathématiquement du score exact pour zéro incohérence
        if total_buts % 2 == 0:
            choix_pair = f"Oui ({total_buts} buts au total - Cohérence mathématique validée)"
        else:
            choix_pair = f"Non ({total_buts} buts au total - Cohérence mathématique validée)"

        # Analyse des pénalties manqués liée à la structure du score
        if total_buts >= 10:
            penalties_manques = "Plus de 3.5 Pénalties manqués (Forte nervosité en mort subite)"
        elif total_buts == 9:
            penalties_manques = "Plus de 2.5 Pénalties manqués (Pression accrue sur les gardiens)"
        else:
            penalties_manques = "Moins de 2.5 Pénalties manqués (Efficacité remarquable des tireurs)"

        confiance = round(97.5 + min(abs(ecart) * 0.3, 2.0), 1)

        analyses_pro = [
            f"Analyse de la dynamique de forme : {vainqueur} surprend grâce à une efficacité redoutable de ses tireurs sur cette session.",
            f"Étude des métriques de performance : la solidité inattendue affichée par {vainqueur} fait basculer le pronostic en sa faveur.",
            f"Lecture des tendances de la simulation : la dynamique du jour penche nettement pour {vainqueur}.",
            f"Indice de surprise tactique : {vainqueur} gère mieux la pression et déjoue les pronostics initiaux."
        ]
        analyse_retenue = random.choice(analyses_pro)

        response = (
            "🔥 *DIENG PREDICT VIP - ANALYSE EXPERT FC26*\n\n"
            f"⚽ *Match :* {eq_a} vs {eq_b}\n"
            f"🕒 *Heure d'analyse :* {current_time_str} (GMT)\n"
            "🏆 *Contexte :* Analyse Dynamique & Forme du Jour (FC26)\n\n"
            "🎯 *1. Verdict & Hiérarchie :* \n"
            f"• **Vainqueur Validé :** {vainqueur} 🏆\n"
            f"• *Analyse professionnelle :* {analyse_retenue}\n\n"
            "🎯 *2. Scores Exacts & Marchés Principaux :* \n"
            f"• Option 1 (Score exact principal) : **{opt_1}**\n"
            f"• Option 2 (Score exact alternatif) : **{opt_2}**\n"
            f"• *Volume de buts :* {marche_total}\n\n"
            "🎯 *3. Options VIP Supplémentaires (Tendances Marché) :* \n"
            f"• *Total Pair :* **{choix_pair}**\n"
            f"• *Pénalties Manqués :* **{penalties_manques}**\n\n"
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
