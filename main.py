import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_BASE = "https://goldenbrainapi-railway-production.up.railway.app"

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et relié à l'IA Phase ∞.")

# /btc
async def handle_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(f"{API_BASE}/btc", timeout=10)
        d = r.json()
        await update.message.reply_text(
            f"📊 *Analyse IA BTC*\n"
            f"Entrée : {d['entry']}\n"
            f"SL : {d['sl']} — TP : {d['tp']}\n"
            f"R:R = {d['rr']} — Confiance : {d['confidence']} %\n\n"
            f"🧠 _{d['comment']}_",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur IA BTC : {str(e)}")

# /or
async def handle_or(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(f"{API_BASE}/or", timeout=10)
        d = r.json()
        await update.message.reply_text(
            f"📊 *Analyse IA OR*\n"
            f"Entrée : {d['entry']}\n"
            f"SL : {d['sl']} — TP : {d['tp']}\n"
            f"R:R = {d['rr']} — Confiance : {d['confidence']} %\n\n"
            f"🧠 _{d['comment']}_",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur IA OR : {str(e)}")

# /alerte
async def handle_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(f"{API_BASE}/alert", timeout=10)
        d = r.json()
        if d["alert"]:
            await update.message.reply_text(
                f"🚨 *ALERTE IA DÉTECTÉE*\n"
                f"Actif : {d['asset']}\n"
                f"Entrée : {d['entry']} — TP : {d['tp']} — SL : {d['sl']}\n"
                f"Confiance : {d['confidence']} % — R:R = {d['rr']}\n\n"
                f"🧠 _{d['comment']}_",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("✅ Aucune alerte IA détectée pour le moment.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur IA alerte : {str(e)}")

# /resume
async def handle_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Résumé IA bientôt disponible avec comparaison multi-actifs.")

# Lancement Webhook
async def main():
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("btc", handle_btc))
    telegram_app.add_handler(CommandHandler("or", handle_or))
    telegram_app.add_handler(CommandHandler("resume", handle_resume))
    telegram_app.add_handler(CommandHandler("alerte", handle_alert))

    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print(f"🚀 Lancement du bot avec webhook : {WEBHOOK_URL}")

    await telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    asyncio.run(main())
