import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bienvenue sur GoldenBrainBot !\n"
        "L’IA Phase ∞ est prête à t’assister.\n\n"
        "Commandes disponibles :\n"
        "/btc — Analyse IA Bitcoin\n"
        "/or — Analyse IA Or\n"
        "/alerte — Dernier signal IA\n"
        "/resume — Vue d’ensemble IA"
    )

# Commande par défaut
async def default(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Test reçu. L'IA Phase ∞ est connectée.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("resume", default))
    app.add_handler(CommandHandler("btc", default))
    app.add_handler(CommandHandler("or", default))
    app.add_handler(CommandHandler("alerte", default))

    print("🚀 Lancement du bot avec webhook :", WEBHOOK_URL)
    
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
