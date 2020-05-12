from flask import Flask, render_template, url_for, request
from datetime import datetime

from news_crawler import NewsCrawler
from secret import auth_key


app = Flask(__name__)
NC = NewsCrawler()


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


@app.route('/cmd', methods=['GET', 'POST'])
def command_prompt():
    valid_cmds = {
        'retrieve': NC.retrieve_and_store_news,
        'empty': NC.empty_table
    }
    if request.method == 'POST':
        if request.form['auth_code'] != auth_key:
            return render_template('form.html', msg='Wrong password')
        else:
            if request.form['command'] in valid_cmds:
                valid_cmds[request.form['command']]()
                return render_template('form.html', msg=f"Ran command {request.form['command']}")
            else:
                return render_template('form.html', msg=f"Unknown command '{request.form['command']}'")

    return render_template('form.html')


@app.route('/news')
def news_renderer():
    maxrank = request.args.get('minrank', default=10, type=int)
    days = request.args.get('days', default=0, type=int)
    news = NC.query_news_from_db(max_rank=maxrank, days=days)
    return render_template('news.html', news=news)
