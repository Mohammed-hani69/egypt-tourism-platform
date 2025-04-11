import os
from app import app, db
from models import *

def create_instance_dir():
    """إنشاء مجلد instance إذا لم يكن موجودًا"""
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
        print(f"تم إنشاء مجلد instance: {instance_path}")

# Function to recreate tables with integrity issues
def full_db_setup():
    """إعداد هيكل قاعدة البيانات الكامل"""
    print("إعداد هيكل قاعدة البيانات الكامل...")

    # إنشاء مجلد instance أولاً
    create_instance_dir()

    with app.app_context():
        # حذف وإعادة إنشاء جميع الجداول
        db.drop_all()
        db.create_all()
        print("تم إعادة إنشاء جميع جداول قاعدة البيانات!")

# تشغيل البرنامج النصي
if __name__ == "__main__":
    try:
        full_db_setup()
    except Exception as e:
        print(f"حدث خطأ أثناء إعداد قاعدة البيانات: {str(e)}")