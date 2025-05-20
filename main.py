import asyncio
import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

# === Configuration ===
TOKEN = os.getenv("BOT_TOKEN", "8111065684:AAELiMg5Kjuj71fPLqSmGk0QNn33VyRazhY")  # À sécuriser !
WEBHOOK_URL = "https://goldenbrainbot-deploy-production.up.railway.app/webhook"

# === Initialisation ===
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
telegram_app: Application = None  # Global défini dans main()

# === Handler /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Bonjour, Omega∞ est prêt à vous assister.")
    except Exception as e:
        logger.error(f"[Handler /start] Erreur : {e}")

# === Webhook endpoint ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, telegram_app.bot)
        asyncio.get_event_loop().create_task(telegram_app.update_queue.put(update))
        return "OK", 200
    except Exception as e:
        logger.exception("[Webhook] Erreur lors du traitement de l'update :")
        return "Erreur interne", 500

# === Lancement principal ===
async def main():
    global telegram_app

    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))

    await telegram_app.bot.delete_webhook(drop_pending_updates=True)
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"✅ Webhook configuré sur {WEBHOOK_URL}")

    asyncio.create_task(telegram_app.run_polling())  # fallback polling si webhook inactif

# === Exécution ===
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        logger.exception("[Main] Erreur critique au démarrage :")
