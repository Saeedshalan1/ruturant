@app.route('/')
def index():
    return 'الصفحة الرئيسية'

@app.route('/about')
def about():
    return 'صفحة عن الموقع'