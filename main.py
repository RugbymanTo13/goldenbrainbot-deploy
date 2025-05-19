import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ENV vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Crée l'application Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 GoldenBrainBot est actif avec Phase ∞ OMEGA∞.\n\n"
        "Tu recevras automatiquement les alertes IA dès qu’un signal BTC ou OR est détecté."
    )

application.add_handler(CommandHandler("start", start))

# Flask app pour recevoir les requêtes Telegram
flask_app = Flask(__name__)

@flask_app.post("/webhook")
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)

        async def process():
            await application.initialize()
            await application.process_update(update)

        asyncio.run(process())
        return "OK", 200

    except Exception as e:
        print(f"❌ Erreur Webhook : {e}")
        return "Error", 500

if __name__ == "__main__":
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
