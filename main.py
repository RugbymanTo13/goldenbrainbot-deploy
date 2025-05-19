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
    await update.message.reply_text("🤖 GoldenBrainBot est en ligne et relié à Phase ∞.")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), telegram_app.bot)
            asyncio.run(telegram_app.process_update(update))
        except Exception as e:
            print("❌ Erreur Webhook :", e)
        return "OK"
    return "Invalid request", 400

if __name__ == "__main__":
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")
    telegram_app.bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
