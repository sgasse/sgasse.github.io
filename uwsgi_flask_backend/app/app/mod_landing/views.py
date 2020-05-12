from flask import render_template, url_for, request, Blueprint
from datetime import datetime
#from apscheduler.schedulers.background import BackgroundScheduler

from app.news_crawler.news_crawler import NewsCrawler


mod_landing = Blueprint('landing', __name__, url_prefix='')


NC = NewsCrawler()
try:
    import uwsgi
except ImportError:
    UWSGI_ENABLED = False
else:
    def ret_wrapper(num):
        t = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
        print(f'Retrieval triggered with signal {num} at {t}')
        NC.retrieve_and_store_news()
    UWSGI_ENABLED = True
    # call ret_wrapper with the first free worker upon receiving signal 10
    uwsgi.register_signal(10, 'worker', ret_wrapper)
    # triggering retrieval with signal 10 every hour
    uwsgi.add_timer(10, 3600)


@mod_landing.route('/')
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
    return render_template('landing/index.html', bg_url=bg_url_)


@mod_landing.route('/news')
def news_renderer():
    maxrank = request.args.get('minrank', default=10, type=int)
    days = request.args.get('days', default=0, type=int)
    news = NC.query_news_from_db(max_rank=maxrank, days=days)
    return render_template('landing/news.html', news=news)
