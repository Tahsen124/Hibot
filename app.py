import requests
from flask import Flask, request

# ⚠️ توكن البوت موضوع مباشرة داخل الكود بناءً على طلبك
TOKEN = "8321031169:AAHd7BIrJrNr3bR44wj7HBO8ADwXLXGANKA"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("sendMessage error:", e)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    msg = data.get("message") or {}
    chat = msg.get("chat") or {}
    text = (msg.get("text") or "").strip()

    if text == "/start":
        send_message(chat.get("id"), "👋 مرحبًا بك! أتمنى لك يومًا جميلًا ومليئًا بالنجاحات 🌸")
    elif text == "/help":
        send_message(chat.get("id"), "أرسل /start وسيصلك ترحيب لطيف ✨")

    return "ok"

@app.route("/")
def home():
    return "Bot is running!"
