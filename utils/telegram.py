import requests
from flask import current_app
from functools import wraps
import logging
from time import sleep

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.max_retries = current_app.config.get('TELEGRAM_MAX_RETRIES', 3)
        
    def _make_request(self, method, endpoint, data=None, params=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = requests.get(url, params=params)
                else:
                    response = requests.post(url, json=data, params=params, files=files)
                    
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logging.error(f"Telegram API error: {e}")
                if attempt == self.max_retries - 1:
                    raise
                sleep(1 * (attempt + 1))
                
    def send_message(self, chat_id, text, reply_to_message_id=None):
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        return self._make_request("POST", "sendMessage", data=data)
    
    def get_message_status(self, chat_id, message_id):
        return self._make_request("GET", "getMessage", params={
            "chat_id": chat_id,
            "message_id": message_id
        })
        
    def set_webhook(self, url):
        return self._make_request("POST", "setWebhook", data={"url": url})
        
    def delete_webhook(self):
        return self._make_request("POST", "deleteWebhook")
        
    def get_webhook_info(self):
        return self._make_request("GET", "getWebhookInfo")
        
    def send_photo(self, chat_id, photo, caption=None):
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
            
        if isinstance(photo, str):
            data["photo"] = photo
            return self._make_request("POST", "sendPhoto", data=data)
        else:
            files = {"photo": photo}
            return self._make_request("POST", "sendPhoto", data=data, files=files)

def init_telegram(app):
    telegram_bot = TelegramBot(app.config['TELEGRAM_BOT_TOKEN'])
    # تحقق من حالة Webhook عند بدء التشغيل
    webhook_info = telegram_bot.get_webhook_info()
    if not webhook_info.get('url'):
        logging.warning("Telegram webhook is not set")
    app.telegram = telegram_bot

def require_telegram_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التحقق من صحة الطلب
        if not current_app.telegram:
            return {'error': 'Telegram bot not initialized'}, 500
        return f(*args, **kwargs)
    return decorated_function
