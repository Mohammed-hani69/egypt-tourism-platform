import os
import json
import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    try:
        # Check if running in development mode
        is_development = os.environ.get('FLASK_ENV') == 'development'
        
        if is_development:
            # Use mock implementation for development
            return MockFirebaseDB()
            
        # Get credentials path
        creds_path = os.path.join(os.path.dirname(__file__), 'config', 'serviceAccountKey.json')
        
        if not os.path.exists(creds_path):
            print("Warning: Firebase credentials file not found")
            return MockFirebaseDB()
            
        cred = credentials.Certificate(creds_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://egypt-tourism-platform.firebaseio.com'
        })
        return db.reference('/')
        
    except Exception as e:
        print(f"Firebase initialization error: {str(e)}")
        return MockFirebaseDB()

class MockFirebaseDB:
    """Mock implementation for development/testing"""
    def child(self, path):
        return self
        
    def push(self, data):
        print("Mock Firebase: Would push data:", data)
        return None
        
    def update(self, data):
        print("Mock Firebase: Would update data:", data)
        return None

# Initialize database reference
db_realtime = initialize_firebase()

def mark_message_as_read(message_id):
    """Update message read status"""
    try:
        if db_realtime:
            db_realtime.child('chats').child(message_id).update({'is_read': True})
    except Exception as e:
        print(f"Error marking message as read: {str(e)}")
