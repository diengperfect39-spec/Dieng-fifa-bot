import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. Petit serveur web pour satisfaire Render
app = Flask('')

@app.route('/')
def home():
    return "Bot Telegram actif !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Fonction de génération des pronostics (avec de l'aléa)
def get_match_prediction(team1, team2):
    scenarios = [
        ("5 - 4", "4 - 3", 87),
        ("4 - 2", "3 - 1", 82),
        ("5 - 3", "4 - 3", 91),
        ("6 - 5", "5 - 4", 78),
        ("4 - 3", "2 - 1", 85),
        ("3 - 2", "4 - 3", 89)
    ]
    score_opt1, score_opt2, reliability = random.choice(scenarios)
    
    winner = team1 if random.random() > 0.35 else team2
    loser = team2 if winner == team1 else team1
    
    return f"""👑 **PRONOSTIC VIP - TIRS AU BUT FC26** 👑

⚽ **{team1} vs {team2}**

🏆 **Mode : Séance de Penalty (Pronostic Score Exact)**

🔥 **1. Verdict du Vainqueur :**
• Avantage net : **{winner}** (Supériorité dans l'exercice des tirs et sang-froid des tireurs)

🎯 **2. Scores Exacts les plus probables :**
• **Option 1 (Le plus probable)** : {winner} {score_opt1} {loser}
• **Option 2 (Alternative serrée)** : {winner} {score_opt2} {loser}

📊 **Indice de fiabilité :** {reliability}% sur la série"""

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

# 4. Démarrage principal du bot et du serveur
def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Erreur : TELEGRAM_TOKEN non défini !")
        return

    # Lancement du serveur web Flask en arrière-plan (pour Render)
    threading.Thread(target=run_web).daemon = True

    # Lancement du bot Telegram en mode polling
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("match", match_command))
    
    print("Bot démarré avec succès !")
    application.run_polling()

if __name__ == '__main__':
    main()
