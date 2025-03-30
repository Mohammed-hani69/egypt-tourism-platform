import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_babel import Babel


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///egypt_tourism.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure babel for internationalization
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel = Babel()

# Initialize the app with the extension
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db is defined to avoid circular imports
with app.app_context():
    # Import models to create tables
    import models
    db.create_all()
    
    # Import the user loader function
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
