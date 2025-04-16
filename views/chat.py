from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from models import Chat, db
from utils.telegram_helper import require_telegram_auth

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@require_telegram_auth
@login_required
def direct_chat(user_id):
    if request.method == 'POST':
        message = request.form.get('content')
        
        # إرسال الرسالة عبر Telegram
        telegram_response = current_app.telegram.send_message(
            chat_id=user_id,
            text=message
        )
        
        if telegram_response.ok:
            telegram_message_id = telegram_response.json()['result']['message_id']
            
            # حفظ الرسالة في قاعدة البيانات
            chat = Chat(
                sender_id=current_user.id,
                receiver_id=user_id,
                message=message,
                telegram_message_id=telegram_message_id
            )
            db.session.add(chat)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'telegram_message_id': telegram_message_id
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to send message via Telegram'}), 500
    
    # Handle GET request or other logic
    return jsonify({'success': False, 'error': 'Invalid request method'}), 400