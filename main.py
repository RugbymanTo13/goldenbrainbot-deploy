import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Flask app
flask_app = Flask(__name__)

# Telegram bot + Application
bot = Bot(token=BOT_TOKEN)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à Phase ∞.")

telegram_app.add_handler(CommandHandler("start", start))

# Route d'accueil
@flask_app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot est actif."

# Webhook
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        loop = telegram_app._loop
        if loop and loop.is_running():
            asyncio.run_coroutine_threadsafe(
                telegram_app.update_queue.put(update),
                loop
            )
        return "OK", 200
    except Exception as e:
        print(f"❌ Erreur webhook : {e}")
        return "Erreur interne", 500

# Lancement serveur Flask
if __name__ == "__main__":
    print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)
    telegram_app.initialize()
    flask_app.run(host="0.0.0.0", port=PORT)
