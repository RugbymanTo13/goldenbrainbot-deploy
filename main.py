import os
import asyncio
import traceback
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Init
flask_app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à Phase ∞.")

application.add_handler(CommandHandler("start", start))

# Webhook
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.post_update(update))
        return "OK", 200
    except Exception as e:
        print("❌ Erreur Webhook :")
        traceback.print_exc()
        return "Erreur", 500

# Test GET
@flask_app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot opérationnel."

# Lancement
if __name__ == "__main__":
    async def run():
        await application.initialize()
        print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)
        flask_app.run(host="0.0.0.0", port=PORT)

    asyncio.run(run())
