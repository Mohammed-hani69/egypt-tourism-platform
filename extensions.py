from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# إعداد مدير تسجيل الدخول مع خيارات أمان إضافية
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # حماية الجلسة القوية
migrate = Migrate()
babel = Babel()
