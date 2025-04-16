from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel

# Initialize SQLAlchemy without model class
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()

# Configure login manager
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
