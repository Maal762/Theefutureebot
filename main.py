import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

# Telegram credentials
BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
CHAT_ID = "5573886497"

@app.route("/")
def home():
    return "TradingView Telegram Bot is running!"

@app.route("/screenshot/<path:filename>")
def screenshot(filename):
    return send_from_directory("static", filename)

@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json()
    if not data:
        return "No data received", 400

    message = data.get("message", "Trade Alert!")
    screenshot_url = data.get("screenshot_url")

    send_telegram_message(message, screenshot_url)
    return "Alert sent!", 200

def send_telegram_message(message, screenshot_url=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

    if screenshot_url:
        photo_url = f"https://theefutureebot.onrender.com/screenshot/{screenshot_url}"
        
        photo_payload = {
            "chat_id": CHAT_ID,
            "photo": photo_url,
            "caption": message
        }
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data=photo_payload)

if __name__ == "__main__":
    app.run(debug=True)
