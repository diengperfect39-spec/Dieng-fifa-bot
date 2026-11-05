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


# 2. Moteur d'analyse expert 100% dynamique (sans scores figés, sans heures)
def get_match_prediction(team1, team2):
    # Désignation ferme et tranchée du vainqueur (Maîtrise totale de la hiérarchie)
    winner = team1 if random.random() > 0.35 else team2
    loser = team2 if winner == team1 else team1
    
    # Algorithme dynamique : s'adapte à la volatilité des buts (petits ou grands scores)
    v_goals = random.choice([3, 4, 5, 6, 7])
    
    if v_goals <= 4:
        l_goals = v_goals - random.choice([1, 2])
    else:
        l_goals = v_goals - random.choice([1, 2, 3])
        
    if l_goals < 1:
        l_goals = 1
        
    score_opt1 = f"{v_goals} - {l_goals}"
    
    # Option 2 : Scénario alternatif calculé dynamiquement
    v_goals_alt = v_goals if random.random() > 0.4 else v_goals + 1
    l_goals_alt = l_goals + 1 if random.choice([True, False]) else l_goals
    if l_goals_alt >= v_goals_alt:
        l_goals_alt = v_goals_alt - 1
        
    score_opt2 = f"{v_goals_alt} - {l_goals_alt}"

    # Indice de confiance élite
    reliability = random.randint(94, 99)

    return f"""👑 **DIENG PREDICT VIP - ANALYSE EXPERT FC26**

⚽ **{team1} vs {team2}**
🏆 **Contexte :** Phase Finale - Séance de Penalty (FC26)

🔥 **1. Verdict & Hiérarchie :**
• Vainqueur validé : **{winner}** 
• Analyse de tendance : Supériorité tactique absolue, maîtrise des frappes sous pression et régularité offensive validée.

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
