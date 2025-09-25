from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)