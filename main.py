import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()

    # Extract fields from JSON alert
    ticker = data.get("ticker", "UNKNOWN")
    price = data.get("price", "N/A")
    signal = data.get("signal", "NO SIGNAL")
    note = data.get("note", "")
    time = data.get("time", "")

    # Format the Telegram message
    message = (
        f"📉 *Options Trade Alert!*\n"
        f"📌 *Ticker:* {ticker}\n"
        f"💵 *Price:* {price}\n"
        f"🕒 *Time:* {time}\n"
        f"🎯 *Action:* {signal}\n"
        f"📝 *Note:* {note}"
    )

    # Send Telegram message
    send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(send_url, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "Alert sent to Telegram ✅"}), 200
    else:
        return jsonify({"status": "Telegram Error", "details": response.text}), 500

@app.route('/')
def index():
    return "Options Alert Bot Live 🟢"

if __name__ == '__main__':
    app.run()
