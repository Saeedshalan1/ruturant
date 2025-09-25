@echo off
echo تشغيل نظام إدارة المطعم...
echo.

:: تنشيط البيئة الافتراضية
call .venv\Scripts\activate.bat

:: تشغيل التطبيق
set FLASK_APP=restaurant_management
set FLASK_DEBUG=1
flask run

pause