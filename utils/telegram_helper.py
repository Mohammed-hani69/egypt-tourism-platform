import requests
from flask import current_app
from functools import wraps

class TelegramAPI:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        return requests.post(url, json=data)

    def create_chat(self, user1_id, user2_id):
        # Create a group chat between two users
        url = f"{self.base_url}/createChat"
        data = {
            "title": f"Chat_{user1_id}_{user2_id}",
            "user_ids": [user1_id, user2_id]
        }
        return requests.post(url, json=data)

def init_telegram(app):
    telegram = TelegramAPI(app.config['TELEGRAM_BOT_TOKEN'])
    app.telegram = telegram
    return telegram

def require_telegram_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(current_app, 'telegram'):
            raise RuntimeError('Telegram API not initialized')
        return f(*args, **kwargs)
    return decorated_function
