
import os
import sys
from flask import Flask
from extensions import db, login_manager

def create_directory(path):
    """إنشاء مجلد إذا لم يكن موجودًا"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"تم إنشاء المجلد: {path}")

def initialize_database():
    """تهيئة قاعدة البيانات وإنشاء البيانات الأساسية"""
    print("بدء تهيئة قاعدة البيانات...")
    
    # إنشاء تطبيق فلاسك مؤقت
    app = Flask(__name__, instance_relative_config=True)
    
    # التأكد من وجود مجلد instance
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"تم التأكد من وجود مجلد instance: {app.instance_path}")
    except OSError:
        print(f"غير قادر على إنشاء مجلد instance")
    
    # إعداد قاعدة البيانات
    sqlite_path = os.path.join(app.instance_path, 'egypt_tourism.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    print(f"مسار قاعدة البيانات: {sqlite_path}")
    
    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # استيراد النماذج هنا لتجنب الدوائر المتداخلة
        from models import User, Region
        
        # إنشاء جميع الجداول
        db.create_all()
        print("تم إنشاء جميع الجداول بنجاح!")
        
        # التحقق من وجود مسؤول النظام
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            # إنشاء مستخدم مسؤول
            admin = User(
                username="admin",
                email="admin@example.com",
                is_admin=True,
                phone="+201234567890",
                country="مصر"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("تم إنشاء حساب المسؤول بنجاح!")
        
        # التحقق من وجود منطقة واحدة على الأقل
        region_count = Region.query.count()
        if region_count == 0:
            # إنشاء منطقة افتراضية
            region = Region(
                name="القاهرة",
                name_ar="القاهرة",
                description="The capital city of Egypt",
                description_ar="عاصمة جمهورية مصر العربية"
            )
            db.session.add(region)
            db.session.commit()
            print("تم إنشاء منطقة افتراضية!")

if __name__ == "__main__":
    try:
        initialize_database()
        print("تم تهيئة قاعدة البيانات بنجاح!")
    except Exception as e:
        print(f"حدث خطأ أثناء تهيئة قاعدة البيانات: {str(e)}")
        sys.exit(1)
