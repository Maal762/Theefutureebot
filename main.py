import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"
RENDER_URL = "https://theefutureebot.onrender.com"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    resp = requests.post(url, json=payload)
    return resp.status_code == 200

@app.route('/alert', methods=['POST'])
def alert():
    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 415
    data = request.get_json()
    # Example: extract some info from TradingView alert JSON payload
    # Customize this according to your alert format
    message = f"📈 *TradingView Alert*\n\nPayload:\n{data}"

    success = send_telegram_message(message)
    if success:
        return jsonify({"status": "Telegram message sent"}), 200
    else:
        return jsonify({"error": "Failed to send Telegram message"}), 500

@app.route('/')
def index():
    return "TheeFuture Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
