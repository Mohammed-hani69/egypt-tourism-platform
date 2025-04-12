
from app import app
from models import User
from extensions import db

def create_admin_account(username, email, password):
    with app.app_context():
        # التحقق من وجود المستخدم
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"المستخدم بالبريد الإلكتروني {email} موجود بالفعل.")
            return False
        
        # إنشاء مستخدم مسؤول جديد
        admin = User(
            username=username,
            email=email,
            is_admin=True,
            is_guide=False,
            is_student=False,
            is_tourist=False,
            phone="123456789",
            country="Egypt",
            profile_completed=True
        )
        admin.set_password(password)
        
        # حفظ المستخدم في قاعدة البيانات
        db.session.add(admin)
        db.session.commit()
        print(f"تم إنشاء حساب المسؤول {username} بنجاح!")
        return True

if __name__ == "__main__":
    username = input("اسم المستخدم: ")
    email = input("البريد الإلكتروني: ")
    password = input("كلمة المرور: ")
    
    create_admin_account(username, email, password)
