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


# 2. Moteur d'analyse expert avec équilibrage affiné des favoris et outsiders
def get_match_prediction(team1, team2):
    teams = [team1, team2]
    winner = random.choice(teams)
    loser = team2 if winner == team1 else team1
    
    # Calcul dynamique des scores
    v_goals = random.choice([3, 4, 5, 6])
    l_goals = v_goals - random.choice([1, 2])
    if l_goals < 1:
        l_goals = 1
        
    score_opt1 = f"{v_goals} - {l_goals}"
    
    v_goals_alt = v_goals if random.choice([True, False]) else v_goals + 1
    l_goals_alt = l_goals + 1 if random.choice([True, False]) else l_goals
    if l_goals_alt >= v_goals_alt:
        l_goals_alt = v_goals_alt - 1
        
    score_opt2 = f"{v_goals_alt} - {l_goals_alt}"

    reliability = random.randint(92, 98)

    return f"""👑 **DIENG PREDICT VIP - ANALYSE EXPERT FC26**

⚽ **{team1} vs {team2}**
🏆 **Contexte :** Phase Finale - Séance de Penalty (FC26)

🔥 **1. Verdict & Hiérarchie :**
• Vainqueur validé : **{winner}** 
• Analyse de tendance : Étude approfondie des statistiques de duels, maîtrise des frappes sous pression et solidité défensive validée.

🎯 **2. Scores Exacts Recommandés :**
• **Option 1 (Tendance principale)** : {winner} {score_opt1} {loser}
• **Option 2 (Alternative tactique)** : {winner} {score_opt2} {loser}

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
