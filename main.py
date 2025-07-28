import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ✅ Your Telegram Bot Token + Chat ID (PRE-FILLED)
TELEGRAM_BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
TELEGRAM_CHAT_ID = "5573886497"

# ✅ Function to generate AI-style trade commentary
def generate_ai_message(ticker, direction, strike, expiry, contracts):
    direction_word = "Call Option 🔼" if direction.lower() == "call" else "Put Option 🔽"
    style = f"🔥 **{ticker} {direction_word} Alert** 🔥\n"
    details = (
        f"🎯 **Strike Price:** {strike}\n"
        f"📅 **Expiry Date:** {expiry}\n"
        f"📦 **Contracts:** {contracts}\n"
    )
    comment = f"📈 Aristotle x Chris Sain-style move. Aiming for +$10K/week on this setup. Stay sharp. 📊"
    return f"{style}{details}{comment}"

# ✅ Route to receive TradingView alerts
@app.route('/alert', methods=['POST'])
def alert():
    try:
        data = request.get_json()
        
        # Validate keys
        required = ['ticker', 'direction', 'strike', 'expiry', 'contracts', 'chart_url']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing keys in JSON'}), 400

        # Extract values
        ticker = data['ticker'].upper()
        direction = data['direction'].capitalize()
        strike = data['strike']
        expiry = data['expiry']
        contracts = data['contracts']
        chart_url = data['chart_url']

        # AI-style message
        message = generate_ai_message(ticker, direction, strike, expiry, contracts)

        # Get screenshot from chart_url using Screenshot API
        screenshot_api = f"https://image.thum.io/get/width/1000/crop/900/noanimate/{chart_url}"

        # Send Telegram message with screenshot
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': message,
            'photo': screenshot_api,
            'parse_mode': 'Markdown'
        }
        r = requests.post(send_url, data=payload)

        if r.status_code != 200:
            return jsonify({'error': 'Telegram send failed', 'details': r.text}), 500

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Root check
@app.route('/', methods=['GET'])
def home():
    return "🟢 TheeFuture-Bot is LIVE and running."
