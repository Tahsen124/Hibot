import os
from flask import Flask, request
import requests

# جلب التوكن من Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# دالة إرسال رسالة
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# استقبال التحديثات من تيليجرام
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "👋 مرحبًا بك! أتمنى لك يومًا رائعًا مليئًا بالنجاح 🌸")
    return "ok"

# صفحة افتراضية لفحص السيرفر
@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
