import os
import aiohttp
import asyncio
import traceback
import pytz
from datetime import datetime
from flask import Flask, request
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))
API_BASE = "https://goldenbrainapi-railway-production.up.railway.app"
USER_CHAT_ID = 1772461776

# === FLASK & TELEGRAM ===
flask_app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# === /start COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 GoldenBrainBot est connecté à l’IA Phase ∞ et prêt à détecter les signaux.")

application.add_handler(CommandHandler("start", start))

# === WEBHOOK ROUTES ===
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, application.bot)
        asyncio.run(application.process_update(update))
        return "OK", 200
    except Exception:
        print("❌ Erreur Webhook :")
        traceback.print_exc()
        return "Erreur", 500

@flask_app.route("/", methods=["GET"])
def home():
    return "GoldenBrainBot opérationnel."

# === BACKGROUND ALERT MONITOR ===
last_alert_id = None

async def alert_task():
    global last_alert_id
    print("🧠 Surveillance IA démarrée...")

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(f"{API_BASE}/alert", timeout=10) as resp:
                    if resp.status != 200:
                        print(f"⚠️ Phase ∞ API down: {resp.status}")
                        await asyncio.sleep(30)
                        continue

                    d = await resp.json()

                if d.get("alert") and d.get("alert_id") != last_alert_id:
                    last_alert_id = d["alert_id"]
                    now = datetime.now(pytz.timezone("Europe/Paris"))
                    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

                    message = (
                        f"🚨 *ALERTE IA DÉTECTÉE*\n"
                        f"Actif : {d.get('asset')}\n"
                        f"Entrée : {d.get('entry')} — TP : {d.get('tp')} — SL : {d.get('sl')}\n"
                        f"Confiance : {d.get('confidence')} % — R:R = {d.get('rr')}\n"
                        f"🕒 {timestamp}\n\n"
                        f"🧠 _{d.get('comment', 'Pas d’analyse')}_"
                    )

                    await application.bot.send_message(
                        chat_id=USER_CHAT_ID,
                        text=message,
                        parse_mode="Markdown"
                    )

                    # Graphique IA
                    asset = d.get("asset", "").lower()
                    if asset in ["or", "btc"]:
                        chart_url = f"{API_BASE}/chart?asset={asset}"
                        async with session.get(chart_url) as chart_resp:
                            if chart_resp.status == 200:
                                with open("chart.png", "wb") as f:
                                    f.write(await chart_resp.read())
                                with open("chart.png", "rb") as f:
                                    await application.bot.send_photo(chat_id=USER_CHAT_ID, photo=InputFile(f))
                                os.remove("chart.png")
                            else:
                                print(f"[Graphique] Erreur de téléchargement : {chart_resp.status}")
            except Exception as e:
                print(f"❌ Erreur boucle IA : {e}")
            await asyncio.sleep(30)

# === POST INIT TASK ===
async def post_init(app: Application):
    asyncio.create_task(alert_task())

application.post_init = post_init

# === LANCEMENT FINAL ===
if __name__ == "__main__":
    async def main():
        await application.initialize()
        await application.start()
        print(f"🚀 Webhook actif sur : {WEBHOOK_URL}")
        flask_app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
