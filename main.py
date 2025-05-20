import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask pour gérer le webhook
app = Flask(__name__)
application = None  # Déclaré globalement pour accès dans le webhook


# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour, ici Omega∞ — votre IA connectée.")


# Commande /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envoyez un message et je répondrai intelligemment.")


# Gestion des messages textes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Omega∞ a bien reçu : « {update.message.text} »")


# Gestion des erreurs
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Erreur détectée : {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Une erreur est survenue, Omega∞ tente de se corriger...")


# Initialisation du bot Telegram
async def main():
    global application

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    await application.bot.set_webhook(WEBHOOK_URL)
    logging.info(f"🚀 Webhook configuré sur {WEBHOOK_URL}")
    await application.initialize()
    await application.start()


# Point d'entrée Webhook depuis Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.get_event_loop().create_task(application.update_queue.put(update))
    except Exception as e:
        logger.exception("Erreur dans le webhook")
    return "ok"


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    app.run(host="0.0.0.0", port=8080)
