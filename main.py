import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Config Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Init Flask + Telegram
flask_app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à Phase ∞.")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook route
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        telegram_app.update_queue.put_nowait(update)
        return "OK", 200
    except Exception as e:
        print(f"❌ Erreur webhook : {e}")
        return "Erreur interne", 500

# Route test
@flask_app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot est actif."

# Lancement serveur Flask + Telegram (dans thread)
if __name__ == "__main__":
    print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)

    # Lancer l'application Telegram dans un thread
    threading.Thread(target=telegram_app.run_polling, daemon=True).start()

    # Lancer le serveur Flask
    flask_app.run(host="0.0.0.0", port=PORT)
