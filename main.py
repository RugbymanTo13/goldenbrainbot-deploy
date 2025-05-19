import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 GoldenBrainBot est opérationnel et connecté à Phase ∞.")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        await telegram_app.process_update(update)
        return "OK", 200
    except Exception as e:
        print(f"❌ Erreur Webhook : {e}")
        return "Error", 500

if __name__ == "__main__":
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )
