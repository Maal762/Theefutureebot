import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"
RENDER_URL = "https://theefutureebot.onrender.com"

# Route to serve static image files
@app.route("/static/snapshots/<path:filename>")
def snapshot(filename):
    return send_from_directory("static/snapshots", filename)

# Webhook to receive alerts from TradingView
@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No JSON received", 400

    ticker = data.get("ticker", "UNKNOWN")
    message = data.get("message", "No message content provided.")

    image_path = f"static/snapshots/{ticker}.png"
    image_url = f"{RENDER_URL}/static/snapshots/{ticker}.png"

    if os.path.exists(image_path):
        send_telegram_photo(image_path, message)
    else:
        send_telegram_message(f"{message}\n\n[Chart Image]({image_url})")

    return "Alert received", 200

# Function to send image to Telegram
def send_telegram_photo(image_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"photo": photo})

# Function to send message to Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
