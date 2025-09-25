from restaurant_management import app, db
from restaurant_management.models import User

if __name__ == '__main__':
    # تأكد من إنشاء قاعدة البيانات قبل تشغيل التطبيق
    with app.app_context():
        db.create_all()
        
        # إنشاء مستخدم افتراضي إذا لم يكن موجودًا
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('تم إنشاء مستخدم افتراضي: admin / admin123')
    
    # تشغيل التطبيق في وضع التصحيح
    app.run(debug=True)



