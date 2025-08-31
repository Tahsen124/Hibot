import os
import logging
from flask import Flask, request
import requests

# إعدادات بسيطة للّوق
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

# اجلب التوكن من متغيرات البيئة
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is missing!")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id: int, text: str):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload, timeout=10)
    if not r.ok:
        log.error("sendMessage failed: %s - %s", r.status_code, r.text)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    log.info("update: %s", data)

    msg = data.get("message") or data.get("edited_message")
    if not msg:
        return "ok"

    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    if text == "/start":
        send_message(chat_id, "👋 مرحبًا بك! أتمنى لك يومًا جميلًا ومليئًا بالنجاح 🌸")
    elif text == "/help":
        send_message(chat_id, "أرسل /start وسيصلك ترحيب لطيف ✨")
    else:
        # رد افتراضي اختياري
        pass

    return "ok"

@app.route("/")
def home():
    return "Bot is running!"
