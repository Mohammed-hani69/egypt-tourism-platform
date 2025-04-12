import os
import logging
from flask import Flask
from extensions import db, login_manager, babel, migrate

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure app
    app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # حفظ الجلسة لمدة يوم (24 ساعة)
    app.config['SESSION_COOKIE_SECURE'] = True  # تأمين ملف تعريف الارتباط
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # منع الوصول عبر جافا سكريبت
    
    # التأكد من وجود مجلد instance
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"تم التأكد من وجود مجلد instance: {app.instance_path}")
    except OSError:
        print(f"غير قادر على إنشاء مجلد instance")
    
    # Database configuration
    sqlite_path = os.path.join(app.instance_path, 'egypt_tourism.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{sqlite_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print(f"مسار قاعدة البيانات: {sqlite_path}")
    
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Babel configuration
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة.'
    login_manager.login_message_category = 'info'
    login_manager.refresh_view = 'main.login'
    login_manager.needs_refresh_message = 'يرجى إعادة تسجيل الدخول لتأكيد هويتك.'
    login_manager.needs_refresh_message_category = 'info'
    
    with app.app_context():
        # Import models here to avoid circular imports
        from models import User
        from datetime import datetime, timedelta
        from flask import session
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
            
        @app.before_request
        def before_request():
            # تحديث وقت آخر نشاط للمستخدم
            if current_user.is_authenticated:
                # فحص وقت آخر نشاط، إذا مر وقت طويل، أعد تحقق من صلاحية الجلسة
                if 'last_activity' in session:
                    last_activity = datetime.fromisoformat(session['last_activity'])
                    # فحص إذا مرت ساعة دون نشاط
                    if datetime.now() - last_activity > timedelta(hours=1):
                        # تحقق من المستخدم في قاعدة البيانات للتأكد من أن الحساب لم يتم حظره أو تعديله
                        user = User.query.get(current_user.id)
                        if not user:
                            logout_user()
                            session.clear()
                            flash('انتهت صلاحية جلستك. يرجى تسجيل الدخول مرة أخرى.', 'warning')
                            return redirect(url_for('main.login'))
                
                # تحديث وقت آخر نشاط
                session['last_activity'] = datetime.now().isoformat()
        
        # Import and register blueprints
        from routes import main, get_locale
        app.register_blueprint(main)
        
        # Initialize babel after registering blueprints
        babel.init_app(app, locale_selector=get_locale)
        
        # Create database tables
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
