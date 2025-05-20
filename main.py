import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import asyncio
import os

# Configurations
BOT_TOKEN = os.getenv("BOT_TOKEN", "TON_TOKEN_ICI")
WEBHOOK_URL = "https://goldenbrainbot-deploy-production.up.railway.app/webhook"

# Logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour, Omega∞ est à votre service.")

# Application Telegram
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Lancement webhook sans asyncio.run
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv("PORT", 8080)),
    webhook_url=WEBHOOK_URL,
)
