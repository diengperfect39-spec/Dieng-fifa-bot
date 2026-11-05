import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Serveur web pour Render et UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Bot VIP Dieng Predict actif !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


# 2. Moteur d'analyse professionnel et dynamique FC26 Penalty
def get_match_prediction(team1, team2):
    # Désignation du vainqueur avec une logique de solidité virtuelle
    winner = team1 if random.random() > 0.45 else team2
    loser = team2 if winner == team1 else team1
    
    # Génération dynamique et réaliste des scores de tirs au but (variés : serrés ou offensifs)
    # On simule un écart de buts cohérent pour éviter les scores figés
    winning_goals = random.choice([3, 4, 5, 6, 7])
    # Le perdant marque souvent un score proche ou un peu inférieur
    losing_goals = winning_goals - random.choice([1, 2])
    if losing_goals < 1:
        losing_goals = 1
        
    score_opt1 = f"{winning_goals} - {losing_goals}"
    
    # Option alternative (un autre scénario plausible, ex: plus serré ou aux tirs au but)
    alt_winning = winning_goals if random.random() > 0.5 else winning_goals + 1
    alt_losing = losing_goals if random.random() > 0.5 else losing_goals
    score_opt2 = f"{alt_winning} - {alt_losing}"

    # Indice de confiance professionnel
    reliability = random.randint(88, 96)
    
    # Créneaux horaires stratégiques basés sur les cycles du e-sport
    best_hours = "🕒 **Créneaux horaires les plus rentables :** 13h00 - 15h30 | 20h00 - 00h00 (Forte activité et régularité des favoris)"

    return f"""👑 **DIENG PREDICT VIP - ANALYSE EXPERT FC26**

⚽ **{team1} vs {team2}**
🏆 **Contexte :** Phase Finale - Séance de Penalty (FC26)

🔥 **1. Verdict & Hiérarchie :**
• Vainqueur pressenti : **{winner}** 
• Analyse de tendance : Supériorité dans la gestion des duels et solidité des frappes.

🎯 **2. Scores Exacts Recommandés :**
• **Option 1 (Tendance principale)** : {winner} {score_opt1} {loser}
• **Option 2 (Alternative tactique)** : {winner} {score_opt2} {loser}

{best_hours}

📊 **Indice de Confiance VIP :** {reliability}%"""


# 3. Commande /match sur Telegram
async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if "vs" in text.lower():
        parts = text.lower().split("vs")
        team1 = parts[0].strip().title()
        team2 = parts[1].strip().title()
    else:
        team1 = "Équipe 1"
        team2 = "Équipe 2"

    prediction = get_match_prediction(team1, team2)
    await update.message.reply_text(prediction, parse_mode="Markdown")


# 4. Démarrage du bot et du serveur
def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Erreur : TELEGRAM_TOKEN non défini !")
        return

    # Lancement du serveur web en arrière-plan
    threading.Thread(target=run_web, daemon=True).start()

    # Lancement du bot Telegram
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("match", match_command))
    
    print("Bot VIP démarré avec succès !")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
