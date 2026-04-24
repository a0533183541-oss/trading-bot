import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    price = float(data.get("price", 0))
    signal = data.get("signal", "NONE")

    if signal == "BUY":
        strike = round(price / 50) * 50
        message = f"""
🚀 CALL SIGNAL

Strike: {strike}
Entry: {price}
Target: {price + 80}
Stop: {price - 40}
"""
        send_telegram(message)

    elif signal == "SELL":
        strike = round(price / 50) * 50
        message = f"""
🔻 PUT SIGNAL

Strike: {strike}
Entry: {price}
Target: {price - 80}
Stop: {price + 40}
"""
        send_telegram(message)

    return {"status": "ok"}

app.run(host="0.0.0.0", port=10000)
