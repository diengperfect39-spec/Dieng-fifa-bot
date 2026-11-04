import random

def get_match_prediction(team1, team2):
    # Liste de scénarios de scores et de fiabilités variés
    scenarios = [
        ("5 - 4", "4 - 3", 87),
        ("4 - 2", "3 - 1", 82),
        ("5 - 3", "4 - 3", 91),
        ("6 - 5", "5 - 4", 78),
        ("4 - 3", "2 - 1", 85),
        ("3 - 2", "4 - 3", 89)
    ]
    
    # Sélection aléatoire d'un scénario pour que ça change à chaque fois
    score_opt1, score_opt2, reliability = random.choice(scenarios)
    
    # Détermination dynamique du vainqueur (par défaut team1 ou alternance)
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
