import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Liste complète des championnats virtuels
CHAMPIONNATS = {
    "fc26_super": "🌐 FC 26. 5x5 Rush. Superligue",
    "fc24_eng": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 FC 24. 4x4. Championnat d'Angleterre",
    "fc25_conf": "🇪🇺 FC 25. 3x3. Ligue de conférence",
    "fc26_champ": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 FC 26. Championship d'Angleterre",
    "fc26_ucl": "🏆 FC 26. Ligue des champions",
    "fc26_world": "🌍 FC 26. Championnat du monde",
    "bundes_sim": "🇩🇪 Allemagne. Bundesliga. Simulation",
    "pl_sim": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Angleterre. Premier League. Simulation",
    "liga_sim": "🇪🇸 Espagne. La Liga. Simulation",
    "fc26_GER": "🇩🇪 FC 26. Championnat d'Allemagne",
    "fc26_ESP": "🇪🇸 FC 26. Championnat d'Espagne",
    "fc26_ITA": "🇮🇹 FC 26. Championnat d'Italie",
    "fc26_EL": "🇪🇺 FC 26. Europe League",
    "fc26_pen": "⚽ FC26. Penalty",
    "ita_sim": "🇮🇹 Italie. Série A. Simulation",
    "ucl_sim": "🏆 Ligue des champions UEFA. Simulation"
}

# Base d'équipes virtuelles types
EQUIPES_VIRTUELLES = [
    ("Team Alpha (eSport)", "Team Omega (eSport)"),
    ("Manchester Red (Sim)", "London Blue (Sim)"),
    ("Madrid White (eSport)", "Munich Red (Sim)"),
    ("Paris Saint-Virtual", "Milano Black (Sim)"),
    ("Buenos Aires e-Club", "Tokyo Samurai (Sim)")
]

def generer_analyse_pro(home, away):
    """Génère une analyse robuste incluant les scores, over/under et le total pair (Oui/Non) par mi-temps"""
    # Forme récente simulée
    form_home = f"{random.randint(2, 5)}V {random.randint(0, 2)}N {random.randint(0, 1)}D"
    form_away = f"{random.randint(1, 4)}V {random.randint(1, 3)}N {random.randint(0, 2)}D"
    
    # 1ère Période (1H)
    h_1h = random.choices([0, 1, 2], weights=[40, 45, 15])[0]
    a_1h = random.choices([0, 1, 2], weights=[50, 35, 15])[0]
    total_1h = h_1h + a_1h
    pair_1h = "OUI 🟢" if total_1h % 2 == 0 else "NON 🔴"

    # 2ème Période (2H - buts marqués spécifiquement dans la 2ème mi-temps)
    h_2h = random.choices([0, 1, 2], weights=[45, 40, 15])[0]
    a_2h = random.choices([0, 1, 2], weights=[45, 40, 15])[0]
    total_2h = h_2h + a_2h
    pair_2h = "OUI 🟢" if total_2h % 2 == 0 else "NON 🔴"

    # Temps Réglementaire (FT)
    h_ft = h_1h + h_2h
    a_ft = a_1h + a_2h
    total_ft = h_ft + a_ft
    pair_ft = "OUI 🟢" if total_ft % 2 == 0 else "NON 🔴"
    
    over_under = "+2.5 Buts" if total_ft > 2.5 else "-2.5 Buts"
    
    # Issue du match (1X2)
    if h_ft > a_ft:
        tendance_1x2 = "Victoire V1 🟢"
    elif h_ft < a_ft:
        tendance_1x2 = "Victoire V2 🔵"
    else:
        tendance_1x2 = "Match Nul 🟡"

    # Cotes simulées
    cote_v1 = round(random.uniform(1.70, 2.40), 2)
    cote_n = round(random.uniform(3.10, 3.80), 2)
    cote_v2 = round(random.uniform(2.10, 3.50), 2)

    return {
        "home": home,
        "away": away,
        "form_home": form_home,
        "form_away": form_away,
        "score_1h": f"{h_1h} - {a_1h}",
        "pair_1h": pair_1h,
        "score_2h": f"{h_2h} - {a_2h}",
        "pair_2h": pair_2h,
        "score_ft": f"{h_ft} - {a_ft}",
        "pair_ft": pair_ft,
        "total_buts": total_ft,
        "over_under": over_under,
        "prediction": tendance_1x2,
        "cotes": f"V1: {cote_v1} | N: {cote_n} | V2: {cote_v2}"
    }

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=code)] for code, name in CHAMPIONNATS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Bienvenue sur le **FIFA Virtual Match Bot** de Dieng !\n\n"
        "📊 *Module d'analyse prédictive professionnelle actif.*\n"
        "Sélectionnez un championnat ci-dessous pour analyser les matchs en cours :",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Gestion de la sélection d'un championnat
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    champ_code = query.data
    
    if champ_code == "retour":
        await start(update, context)
        return

    champ_name = CHAMPIONNATS.get(champ_code, "Championnat")
    matchs_selectionnes = random.sample(EQUIPES_VIRTUELLES, 2)

    text = f"🏆 **ANALYSE EXPERTE : {champ_name}** 🏆\n\n"
    
    for equipe_h, equipe_a in matchs_selectionnes:
        an = generer_analyse_pro(equipe_h, equipe_a)
        
        text += f"🎮 **{an['home']}** vs **{an['away']}**\n"
        text += f"📈 *Forme* : {an['form_home']} | {an['form_away']}\n"
        text += f"⏱ **1ère Période (1H)** : Score `{an['score_1h']}` | Pair ? **{an['pair_1h']}**\n"
        text += f"⏱ **2ème Période (2H)** : Score `{an['score_2h']}` | Pair ? **{an['pair_2h']}**\n"
        text += f"🎯 **Temps Réglementaire (FT)** : Score `{an['score_ft']}` | Pair ? **{an['pair_ft']}**\n"
        text += f"⚽ **Total Buts** : `{an['total_buts']} buts ({an['over_under']})`\n"
        text += f"💡 **Tendance 1X2** : **{an['prediction']}**\n"
        text += f"📊 *Cotes* : `{an['cotes']}`\n"
        text += "----------------------------------------\n"

    keyboard = [[InlineKeyboardButton("🔙 Retour aux championnats", callback_data="retour")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

# Lancement du Bot
if __name__ == "__main__":
    TOKEN = "9068698544:AAFIhEz56h_fF1L7qNa8_OtRNpCX4LjjQrU"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot mis à jour avec les options Pair/Impair 1H, 2H et FT !")
    app.run_polling()
