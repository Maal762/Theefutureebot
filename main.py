import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your Render URL:
RENDER_URL = "https://theefutureebot.onrender.com/"

TELEGRAM_BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json(force=True)

    ticker = data.get("ticker", "UNKNOWN")
    price = data.get("price", "N/A")
    signal = data.get("signal", "NO SIGNAL")
    note = data.get("note", "")
    time = data.get("time", "")

    message = (
        f"📉 *Options Trade Alert!*\n"
        f"📌 *Ticker:* {ticker}\n"
        f"💵 *Price:* {price}\n"
        f"🕒 *Time:* {time}\n"
        f"🎯 *Action:* {signal}\n"
        f"📝 *Note:* {note}"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    resp = requests.post(telegram_url, json=payload)

    if resp.status_code == 200:
        return jsonify({"status": "Alert sent to Telegram ✅"}), 200
    else:
        return jsonify({"status": "Telegram Error", "details": resp.text}), 500

@app.route('/')
def home():
    return "Options Alert Bot is Running 🟢"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
