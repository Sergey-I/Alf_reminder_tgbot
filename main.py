from flask import Flask, request
import requests


# main.py
from flask import Flask, request
import requests
import os

# Create the Flask app
app = Flask(__name__)


BOT_TOKEN = "8381801882:AAFL0nA5C8rRSoUzO9oXCj53glOqjZXRp_U"  # <-- replace with your token
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Your Telegram bot token (set as environment variable on Render for security)
#BOT_TOKEN = os.getenv("BOT_TOKEN")
#if not BOT_TOKEN:
#    raise ValueError("Please set the BOT_TOKEN environment variable in Render.")

#API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Route for Telegram webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data:
        return "No data", 400

    # Check for message
    message = data.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/getid":
            send_message(chat_id, f"Your chat ID is: {chat_id}")

    return "OK", 200

# Helper function to send messages
def send_message(chat_id, text):
    requests.post(API_URL + "sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# Optional root route to check server
@app.route("/")
def home():
    return "✅ Telegram bot is running!"

# For local testing only
if __name__ == "__main__":
    app.run(debug=True)
