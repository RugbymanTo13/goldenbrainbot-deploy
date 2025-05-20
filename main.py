import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8111065684:AAELiMg5Kjuj71fPLqSmGk0QNn33VyRazhY"
WEBHOOK_URL = "https://goldenbrainbot-deploy-production.up.railway.app/webhook"

# Init bot + Flask
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Log
logging.basicConfig(level=logging.INFO)

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour, Omega∞ est à votre service.")

application.add_handler(CommandHandler("start", start))

# Route webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    loop = asyncio.get_event_loop()
    loop.create_task(application.update_queue.put(update))
    return "OK"

# Setup Webhook
async def main():
    await application.bot.set_webhook(WEBHOOK_URL)
    logging.info(f"🚀 Webhook configuré sur {WEBHOOK_URL}")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # facultatif si tu veux backup polling

# Lancement
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    app.run(host="0.0.0.0", port=8080)
