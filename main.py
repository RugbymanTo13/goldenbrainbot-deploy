import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Application Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 GoldenBrainBot est actif avec Phase ∞ OMEGA∞.\n\n"
        "Tu recevras automatiquement les signaux IA en cas de changement réel (or / BTC).\n"
        "Pas besoin d’envoyer de commande. Surveillance continue activée."
    )

application.add_handler(CommandHandler("start", start))

# Flask pour le webhook
flask_app = Flask(__name__)

@flask_app.post("/webhook")
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"❌ Erreur Webhook : {e}")
    return "OK"

if __name__ == "__main__":
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
