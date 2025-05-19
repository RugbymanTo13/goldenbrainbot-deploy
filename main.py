import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Phase ∞ est prête à te servir.")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook Flask
@app.post("/webhook")
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        asyncio.get_event_loop().create_task(telegram_app.process_update(update))
        return "OK", 200
    except Exception as e:
        print("❌ Erreur Webhook :", e)
        return "Erreur Webhook", 500

# Lancement complet
async def main():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    asyncio.run(main())
