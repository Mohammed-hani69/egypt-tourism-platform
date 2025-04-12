
import os
import sys
from flask import Flask
from extensions import db, login_manager

def create_directory(path):
    """إنشاء مجلد إذا لم يكن موجودًا"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"تم إنشاء المجلد: {path}")

def init_db():
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
    
    # حذف قاعدة البيانات القديمة إذا كانت موجودة
    sqlite_path = os.path.join(app.instance_path, 'egypt_tourism.db')
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)
        print(f"تم حذف قاعدة البيانات القديمة: {sqlite_path}")
    
    # إعداد قاعدة البيانات
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    print(f"مسار قاعدة البيانات: {sqlite_path}")
    
    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # استيراد النماذج هنا لتجنب الدوائر المتداخلة
        from models import User, Region, Attraction, Restaurant, Activity, Review, Guide, ChatGroup, ChatGroupMember, ChatMessage, TourPlan, TourPlanDestination, TourBooking, TourProgress, TourPhoto, LanguagePractice
        
        # إنشاء جميع الجداول
        db.create_all()
        print("تم إنشاء جميع الجداول بنجاح!")
        
        try:
            # إنشاء مستخدم مسؤول افتراضي
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                admin = User(
                    username="admin",
                    email="admin@example.com",
                    is_admin=True,
                    is_guide=False,
                    is_student=False,
                    is_tourist=False,
                    phone="123456789",
                    country="Egypt",
                    profile_completed=True
                )
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("تم إنشاء مستخدم مسؤول افتراضي")
                
            # إضافة بعض البيانات الأساسية
            if Region.query.count() == 0:
                # إضافة المناطق الأساسية
                regions = [
                    Region(name="Cairo", name_ar="القاهرة", description="Egypt's capital city", description_ar="عاصمة مصر"),
                    Region(name="Luxor", name_ar="الأقصر", description="Ancient Egyptian city", description_ar="مدينة مصرية قديمة"),
                    Region(name="Alexandria", name_ar="الإسكندرية", description="Coastal Mediterranean city", description_ar="مدينة ساحلية على البحر المتوسط"),
                ]
                db.session.add_all(regions)
                db.session.commit()
                print("تم إضافة المناطق الأساسية")

            print("تم تهيئة قاعدة البيانات بنجاح!")
            
        except Exception as e:
            print(f"حدث خطأ أثناء تهيئة قاعدة البيانات: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    init_db()
