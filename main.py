import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Your Telegram Bot Token and Chat ID (filled)
BOT_TOKEN = "8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY"
CHAT_ID = "5573886497"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    return requests.post(url, json=payload).json()

def send_telegram_photo(photo_url, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    return requests.post(url, json=payload).json()

# Your actual Render app URL with TradingView snapshots (all use your URL here)
BASE_URL = "https://theefutureebot.onrender.com/static/snapshots"

SNAPSHOTS = {
    "SPY": f"{BASE_URL}/spy.png",
    "NVDA": f"{BASE_URL}/nvda.png",
    "AAPL": f"{BASE_URL}/aapl.png",
    "TSLA": f"{BASE_URL}/tsla.png",
    "AMD": f"{BASE_URL}/amd.png",
    "META": f"{BASE_URL}/meta.png"
}

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/send_spy')
def send_spy():
    text = "🚀 *SPY Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["SPY"], caption="SPY Chart Snapshot")
    return jsonify({"status": "SPY alert sent"})

@app.route('/send_nvda')
def send_nvda():
    text = "🚀 *NVDA Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["NVDA"], caption="NVDA Chart Snapshot")
    return jsonify({"status": "NVDA alert sent"})

@app.route('/send_aapl')
def send_aapl():
    text = "🚀 *AAPL Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["AAPL"], caption="AAPL Chart Snapshot")
    return jsonify({"status": "AAPL alert sent"})

@app.route('/send_tsla')
def send_tsla():
    text = "🚀 *TSLA Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["TSLA"], caption="TSLA Chart Snapshot")
    return jsonify({"status": "TSLA alert sent"})

@app.route('/send_amd')
def send_amd():
    text = "🚀 *AMD Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["AMD"], caption="AMD Chart Snapshot")
    return jsonify({"status": "AMD alert sent"})

@app.route('/send_meta')
def send_meta():
    text = "🚀 *META Alert:* Potential trade signal detected! 📈"
    send_telegram_message(text)
    send_telegram_photo(SNAPSHOTS["META"], caption="META Chart Snapshot")
    return jsonify({"status": "META alert sent"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
