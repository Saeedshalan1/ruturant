@echo off
echo تشغيل نظام إدارة المطعم...
echo.

:: تنشيط البيئة الافتراضية
call .venv\Scripts\activate.bat

:: تشغيل التطبيق
python run.py

:: في حالة حدوث خطأ، انتظر قبل الإغلاق
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo حدث خطأ أثناء تشغيل التطبيق.
    pause
)

