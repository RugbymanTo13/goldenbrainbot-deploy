import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de Flask
flask_app = Flask(__name__)

# Récupération du token et webhook
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ex: https://ton-projet.up.railway.app/webhook

# Application Telegram
application = Application.builder().token(BOT_TOKEN).build()

# Handler de commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour, Omega∞ est à votre service.")

application.add_handler(CommandHandler("start", start))

# Route Flask pour le webhook
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    asyncio.create_task(application.update_queue.put(update))
    return "OK", 200

# Lancement Flask et Telegram
if __name__ == "__main__":
    async def main():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        print(f"🚀 Webhook configuré sur {WEBHOOK_URL}")

    asyncio.get_event_loop().run_until_complete(main())
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
