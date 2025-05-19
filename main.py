import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, Dispatcher

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à l'IA Phase ∞.")

application.add_handler(CommandHandler("start", start))

# Route webhook réelle
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "OK", 200

# Route GET test
@app.route("/", methods=["GET"])
def index():
    return "GoldenBrainBot est en ligne."

if __name__ == "__main__":
    print("✅ Lancement du bot Flask + Telegram Webhook")
    application.run_polling(allowed_updates=[])
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
