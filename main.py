import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Config depuis Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Initialisation du bot Telegram
bot = Bot(token=BOT_TOKEN)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Initialisation Flask
flask_app = Flask(__name__)

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à Phase ∞.")

# Ajouter le handler à l’application Telegram
telegram_app.add_handler(CommandHandler("start", start))

# Webhook Telegram → déclenché automatiquement par Telegram
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run_coroutine_threadsafe(
        telegram_app.update_queue.put(update),
        telegram_app._loop
    )
    return "OK", 200

# Route GET de test
@flask_app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot est en ligne."

# Lancement du serveur Flask
if __name__ == "__main__":
    print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)
    flask_app.run(host="0.0.0.0", port=PORT)
