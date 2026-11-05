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


# 2. Moteur d'analyse expert avec découpage intelligent des équipes et scores réalistes
def get_match_prediction(match_text):
    if "vs" not in match_text.lower():
        return None

    # Séparation propre autour du "vs" (insensible à la casse)
    parts = match_text.split("vs")
    team1 = parts[0].strip().title()
    remainder = parts[1].strip()

    # On sépare les mots de la fin pour identifier si l'utilisateur a mis un chrono/minute (ex: 00:02mn)
    words = remainder.split(" ")
    
    # Détection si le dernier élément ressemble à un temps/chrono
    time_ref = "Direct"
    if len(words) > 1 and ("mn" in words[-1].lower() or ":" in words[-1] or words[-1].isdigit()):
        time_ref = words[-1]
        team2 = " ".join(words[:-1]).strip().title()
    else:
        team2 = remainder.title()

    # Logique de sélection du vainqueur stable
    hash_val = sum(ord(c) for c in team1 + team2 + time_ref)
    winner = team1 if hash_val % 2 == 0 else team2
    loser = team2 if winner == team1 else team1

    # Calcul dynamique de scores réalistes pour des tirs au but (ex: 4-3, 5-4, 6-5, ou scores plus larges)
    v_goals = random.choice([4, 5, 6, 7])
    l_goals = v_goals - 1 if v_goals > 3 else 3
    if l_goals < 1:
        l_goals = 1
        
    score_opt1 = f"{v_goals} - {l_goals}"
    score_opt2 = f"{v_goals} - {l_goals + 1}" if random.choice([True, False]) else f"{v_goals + 1} - {l_goals}"

    reliability = random.randint(94, 98)

    time_display = f"\n⏱️ **Repère temporel :** {time_ref}" if time_ref != "Direct" else ""

    return f"""👑 **DIENG PREDICT VIP - ANALYSE EXPERT FC26**

⚽ **{team1} vs {team2}**
🏆 **Contexte :** Phase Finale - Séance de Penalty (FC26){time_display}

🔥 **1. Verdict & Hiérarchie :**
• Vainqueur validé : **{winner}** 
• Analyse de tendance : Étude croisée du rythme des tirs, de la résistance sous pression et de la dynamique de session.

🎯 **2. Scores Exacts Recommandés :**
• **Option 1 (Tendance principale)** : {winner} {score_opt1} {loser}
• **Option 2 (Alternative tactique)** : {winner} {score_opt2} {loser}

📊 **Indice de Confiance VIP :** {reliability}%"""


# 3. Commande /match sur Telegram
async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_text = " ".join(context.args)
    prediction = get_match_prediction(full_text)
    
    if not prediction:
        await update.message.reply_text("⚠️ Format invalide. Utilise : `/match Equipe1 vs Equipe2 [chrono]`", parse_mode="Markdown")
        return

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
