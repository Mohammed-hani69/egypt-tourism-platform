
import os
from app import app

if __name__ == '__main__':
    # تأكد من وجود مجلد instance قبل التشغيل
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
        print(f"تم إنشاء مجلد instance: {instance_path}")
    
    try:
        print("جاري تشغيل التطبيق على المنفذ 5000...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل التطبيق: {str(e)}")
