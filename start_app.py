import os
import sys
from restaurant_management import app, db
from restaurant_management.models import User

if __name__ == '__main__':
    print("تشغيل نظام إدارة المطعم...")
    
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('تم إنشاء مستخدم افتراضي: admin / admin123')
    
    print("بدء تشغيل الخادم...")
    app.run(host='0.0.0.0', port=5000, debug=True)