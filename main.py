import os
import logging
import asyncio
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from updater import get_decision

# Configuration
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Initialisation
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application Telegram
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Omega∞ est en ligne et à votre service.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    decision = get_decision(text)
    await update.message.reply_text(f"🔍 Analyse : {decision}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook
@app.route('/webhook', methods=['POST'])
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)

        # ✅ Utiliser la boucle interne de Telegram Application (toujours active)
        asyncio.run_coroutine_threadsafe(
            application.update_queue.put(update), application._loop
        )

        return "OK", 200
    except Exception as e:
        logger.exception("Erreur dans le webhook")
        return "Erreur", 500
# Lancement principal
async def main():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    logger.info(f"🚀 Webhook configuré sur {WEBHOOK_URL}")
    await application.start()
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    asyncio.run(main())
