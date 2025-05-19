import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Bot Telegram
bot = Bot(token=BOT_TOKEN)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Flask App
flask_app = Flask(__name__)

# Répondre à /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à Phase ∞.")

telegram_app.add_handler(CommandHandler("start", start))

# Route /webhook appelée par Telegram
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put(update)
    return "OK", 200

# Route GET de test
@flask_app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot opérationnel."

# Lancer le serveur
if __name__ == "__main__":
    print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)
    flask_app.run(host="0.0.0.0", port=PORT)
