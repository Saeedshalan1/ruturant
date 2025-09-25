import os
from restaurant_management import app, db
from restaurant_management.models import User

# إنشاء قاعدة البيانات والمستخدم الافتراضي
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run()
