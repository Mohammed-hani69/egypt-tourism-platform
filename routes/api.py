from flask import Blueprint, request, jsonify, current_app
from models import ChatMessage, db

api = Blueprint('api', __name__)

@api.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    
    # Handle incoming Telegram messages
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        # Save message to database
        chat_message = ChatMessage(
            telegram_chat_id=str(chat_id),
            telegram_message_id=str(message['message_id']),
            content=text,
            is_sent_telegram=True
        )
        db.session.add(chat_message)
        db.session.commit()
        
    return jsonify({'ok': True})

@api.route('/api/message-status/<message_id>')
def message_status(message_id):
    message = ChatMessage.query.filter_by(telegram_message_id=message_id).first()
    if message:
        return jsonify({
            'is_read': message.is_sent_telegram,
            'timestamp': message.timestamp.isoformat()
        })
    return jsonify({'error': 'Message not found'}), 404
