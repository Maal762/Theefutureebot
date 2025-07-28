import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your Telegram Bot token and Chat ID
TELEGRAM_BOT_TOKEN = '8034746391:AAFEi1HrMNdDS3jLX8mFGz5vWjR7K1Aw3LY'
CHAT_ID = '5573886497'

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload)
        return response.ok
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json

    # Extract expected fields from TradingView alert JSON (adjust if needed)
    ticker = data.get('ticker', 'Unknown')
    price = data.get('price', 'N/A')
    signal = data.get('signal', 'Alert')
    timeframe = data.get('timeframe', '')
    extra = data.get('extra', '')

    # Compose message without mentioning strategy names, clean format
    message = f"📊 *{ticker}* Alert\nPrice: {price}\nSignal: {signal}\nTimeframe: {timeframe}"
    if extra:
        message += f"\n{extra}"

    sent = send_telegram_message(message)
    if sent:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
