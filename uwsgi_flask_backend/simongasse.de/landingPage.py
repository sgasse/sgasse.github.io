from flask import Flask, render_template, url_for, request
from datetime import datetime

from news_crawler import main as nc_main

app = Flask(__name__)


@app.route('/')
def landing_page():
    month = datetime.now().month
    if month in [11, 12, 1, 2, 3]:
        bg_url_ = url_for('static', filename='img/bg_ice_small.jpg')
    elif month in [4, 5]:
        bg_url_ = url_for('static', filename='img/bg_lawn_small.jpg')
    elif month in [6, 7, 8]:
        bg_url_ = url_for('static', filename='img/bg_sea_small.jpg')
    elif month in [9, 10]:
        bg_url_ = url_for('static', filename='img/bg_field_small.jpg')
    else:
        bg_url_ = url_for('static', filename='img/bg_field_small.jpg')
    return render_template('index.html', bg_url=bg_url_)


@app.route('/form', methods=['GET', 'POST'])
def login_form():

    if request.method == 'POST':
        if request.form['password'] != 'abc':
            return render_template('form.html')
        else:
            nc_main()
            bg_url_ = url_for('static', filename='img/bg_ice_small.jpg')
            return render_template('index.html', bg_url=bg_url_)
    return render_template('form.html')

