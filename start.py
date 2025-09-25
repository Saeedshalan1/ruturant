import os
import subprocess
import sys

print("تشغيل نظام إدارة المطعم...")

# تشغيل التطبيق
try:
    from restaurant_management import app
    app.run(debug=True)
except Exception as e:
    print(f"حدث خطأ أثناء تشغيل التطبيق: {e}")
    input("اضغط Enter للإغلاق...")


