from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "مرحباً بك في نظام إدارة المطعم!"

if __name__ == '__main__':
    print("جاري تشغيل النظام...")
    app.run(debug=True)