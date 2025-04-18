import os
import logging
from flask import Flask
from config import Config
from extensions import db, login_manager, babel, migrate
from routes import main, get_locale, csrf

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    # Configure app
    app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
    
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
    csrf.init_app(app)  # Initialize CSRF protection
    
    # Configure login
    login_manager.login_view = 'main.login'
    
    with app.app_context():
        # Import models here to avoid circular imports
        from models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Import and register blueprints
        app.register_blueprint(main)
        
        # Initialize babel with locale selector
        babel.init_app(app)
        babel.localeselector(get_locale)
        
        # Create database tables
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
