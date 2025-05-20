import os
import asyncio
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from updater import get_decision

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Omega∞ est en ligne et à votre service.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    decision = get_decision(text)
    await update.message.reply_text(f"🔍 Analyse : {decision}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.update_queue.put(update)
        return "OK", 200
    except Exception as e:
        logger.exception("Erreur dans le webhook")
        return "Erreur", 500

async def main():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    logger.info(f"🚀 Webhook configuré sur {WEBHOOK_URL}")
    await application.start()
    import hypercorn.asyncio
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    await hypercorn.asyncio.serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())