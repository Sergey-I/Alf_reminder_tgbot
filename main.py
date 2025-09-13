from flask import Flask, request
import requests
import logging
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # safer to use env variable
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

def send_message(chat_id, text):
    """Send a message to Telegram with retry"""
    for _ in range(3):
        try:
            requests.post(API_URL + "sendMessage", data={"chat_id": chat_id, "text": text})
            break
        except Exception as e:
            logging.error(f"Error sending message: {e}")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    """Handle incoming Telegram updates"""
    update = request.get_json()
    logging.info(f"Received update: {update}")

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/getid":
            send_message(chat_id, f"Your chat ID is {chat_id}")

    return "OK"

@app.route("/", methods=["GET"])
def index():
    """Optional: basic landing page for Render"""
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
