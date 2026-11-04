from flask import Flask
import threading
import os

# Petit serveur web pour satisfaire Render
app = Flask('')

@app.route('/')
def home():
    return "Bot Telegram actif !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Lancement du serveur web en arrière-plan
threading.Thread(target=run_web).daemon = True
