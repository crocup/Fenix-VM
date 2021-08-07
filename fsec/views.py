from flask import render_template

from fsec import app


@app.route('/')
def index():
    return render_template('index.html')
