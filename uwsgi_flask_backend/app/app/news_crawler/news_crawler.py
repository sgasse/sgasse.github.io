import re
import requests
import sqlite3
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.news_crawler.sentiment import SiteProcessor


DecBase = declarative_base()
SP = SiteProcessor()
DB_FILE = '/db/news.db'


class News(DecBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    retrieved = Column(Date)
    headline = Column(String)
    link = Column(String)
    content = Column(String)
    senti_score = Column(Float)


def _get_top_10_tagesschau():
    def _clean(in_str):
        return in_str.replace('"', '').replace("'", "")

    page = "http://www.tagesschau.de"
    response = requests.get(page)
    m = re.findall(r'<li><a title="(.+)" href="(.+)"><span', response.text)
    news = list()
    for ind, (headline, link) in enumerate(m):
        a_link = f'{page}{link}'
        rank = (ind + 1)
        retrieved = datetime.now().date()
        cnt_words = SP.parse_page_content(requests.get(a_link).text)
        senti_score = SP.get_text_score(cnt_words)
        news.append(dict(rank=rank, headline=headline, retrieved=retrieved,
                         link=a_link, content=' '.join(cnt_words),
                         senti_score=senti_score))
    return news


class NewsCrawler:

    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DB_FILE}?check_same_thread=False')
        self.DecBase = DecBase
        self.DecBase.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _write_news_to_db(self, news):
        session = self.Session()
        for n_ in news:
            _existing = session.query(News).filter(News.rank == n_['rank']).\
                filter(News.retrieved == datetime.now().date())
            _help = _existing.all()
            if _existing.all():
                _existing.update(n_)
            else:
                session.add(News(**n_))
            session.commit()

    def query_news_from_db(self, max_rank=10, days=0):
        if days == 0:
            min_date = datetime(2020, 1, 1)
        else:
            min_date = datetime.now().date() - timedelta(days=(days - 1))
        session = self.Session()
        news_ = session.query(News).filter(News.rank < max_rank).\
            filter(News.retrieved > min_date).all()
        senti_norm = max([abs(t.senti_score) for t in news_])
        news_struct = [{'headline': t.headline,
                        'rank': t.rank,
                        'link': t.link,
                        'retrieved': t.retrieved.strftime("%Y-%m-%d"),
                        'senti_score': t.senti_score,
                        'senti_color': self._senti_color(t.senti_score,
                                                         senti_norm)}
                       for t in news_]
        return news_struct 

    def _senti_color(self, senti_score, senti_norm):
        red = int(255 * -0.5 * ((senti_score / senti_norm) - 1))
        green = int(255 * 0.5 * ((senti_score / senti_norm) + 1))
        return f'rgb({red}, {green}, 0)'

    def retrieve_and_store_news(self):
        news = _get_top_10_tagesschau()
        self._write_news_to_db(news)
        t = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
        print(f'News retrieval complete at {t}')

    def empty_table(self):
        self.DecBase.metadata.drop_all(self.engine)
        self.DecBase.metadata.create_all(self.engine)


def main():
    NC = NewsCrawler()
    NC.retrieve_and_store_news()
    NC.query_news_from_db()
    pass


if __name__ == '__main__':
    DB_FILE = '/home/simon/workspace/personalPage/data/sqlite_data/news.db'
    main()