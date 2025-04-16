from flask import Flask
from utils.telegram_helper import init_telegram
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # تهيئة Telegram
    init_telegram(app)
    
    return app