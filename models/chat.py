from datetime import datetime
from app import db

class Chat(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.Integer, primary_key=True)
    guide_id = db.Column(db.Integer, db.ForeignKey('guides.id'), nullable=False)
    tourist_id = db.Column(db.Integer, db.ForeignKey('tourists.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    telegram_chat_id = db.Column(db.String(100))
    telegram_message_id = db.Column(db.String(100))