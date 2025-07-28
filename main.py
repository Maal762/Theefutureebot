import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

TELEGRAM_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"

@app.route('/')
def index():
    return 'TradingView Screenshot + Telegram Bot is live.'

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = data.get('message', 'Trade Alert 🚨')
    image_url = data.get('image_url')

    if image_url:
        send_photo_to_telegram(image_url, message)
    else:
        send_text_to_telegram(message)

    return 'Alert sent!'

def send_text_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, json=payload)

def send_photo_to_telegram(photo_url, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'photo': photo_url,
        'caption': caption
    }
    requests.post(url, data=payload)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
