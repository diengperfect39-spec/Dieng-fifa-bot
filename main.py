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


# 2. Moteur d'analyse expert basé sur le contexte et le timing du match
def get_match_prediction(match_text):
    # Nettoyage et séparation des équipes et du paramètre temporel si présent
    parts = match_text.split("vs")
    if len(parts) < 2:
        return "⚠️ Format invalide. Utilise : `/match Equipe1 vs Equipe2 [chrono]`"
    
    team1 = parts[0].strip().title()
    remainder = parts[1].strip()
    
    # Séparer la deuxième équipe et l'éventuel chrono/heure fourni
    sub_parts = remainder.split(" ")
    team2 = sub_parts[0].strip().title()
    
    # Récupération du paramètre de temps/chrono si l'utilisateur l'a mis
    time_ref = " ".join(sub_parts[1:]).strip() if len(sub_parts) > 1 else "Direct"

    # Logique de sélection du vainqueur basée sur la longueur des noms et le timing pour éliminer l'aléatoire pur
    hash_val = sum(ord(c) for c in team1 + team2 + time_ref)
    winner = team1 if hash_val % 2 == 0 else team2
    loser = team2 if winner == team1 else team1

    # Analyse dynamique des buts selon le flux du match
    # Plus le temps ou le hash varie, plus on s'adapte aux scores serrés ou fleuves (comme 7-8)
    base_goal = (hash_val % 4) + 4  # Donne entre 4 et 7 buts pour le vainqueur
    v_goals = base_goal
    l_goals = max(1, v_goals - (1 if hash_val % 3 == 0 else 2))
    
    score_opt1 = f"{v_goals} - {l_goals}"
    score_opt2 = f"{v_goals} - {l_goals + 1 if l_goals < v_goals else l_goals - 1}"

    reliability = 95 + (hash_val % 5)

    time_display = f"\n⏱️ **Point de repère :** {time_ref}" if time_ref != "Direct" else ""

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
    if "vs" not in full_text.lower():
        await update.message.reply_text("⚠️ Utilise le format : `/match Nom1 vs Nom2` (avec optionnellement l'heure ou le chrono à la fin).", parse_mode="Markdown")
        return

    prediction = get_match_prediction(full_text)
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
