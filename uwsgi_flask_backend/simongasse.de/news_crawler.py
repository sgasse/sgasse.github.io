import re
import requests
import pg8000
from datetime import datetime, timedelta


def _to_db_date(dtime):
    return dtime.strftime('%Y-%m-%d')


def _get_top_10_tagesschau():
    def _clean(in_str):
        return in_str.replace('"', '')

    page = "http://www.tagesschau.de"
    response = requests.get(page)
    m = re.findall(r'<li><a title="(.+)" href="(.+)"><span', response.text)
    news = [(ind + 1, _clean(headline), _clean(f'{page}{link}'))
            for ind, (headline, link) in enumerate(m)]
    return news


def _setup_db_connection():
    conn = pg8000.connect(database='postgres', user='postgres',
                            password='docker', host='127.0.0.1', port=5432)
    return conn


class NewsCrawler:

    def __init__(self, table_name='news'):
        self.table_name = table_name
        self.conn = _setup_db_connection()
        self._maybe_initialize_table()

    def _maybe_initialize_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS {} (
                        id serial PRIMARY KEY,
                        rank integer,
                        retrieved date,
                        headline varchar,
                        link varchar);
                    """.format(self.table_name))
            self.conn.commit()
        return True

    def _write_news_to_db(self, news):
        insert = f'INSERT INTO {self.table_name} (rank, retrieved, headline, link) VALUES'
        td = _to_db_date(datetime.now())
        vals = [f"({rank}, '{td}', '{headline}', '{link}');"
                for rank, headline, link in news]
        with self.conn.cursor() as cur:
            for val in vals:
                sql_cmd = f'{insert}\n   {val};'
                cur.execute(sql_cmd)
            self.conn.commit()

    def query_news_from_db(self, max_rank=10, days=0):
        if days == 0:
            min_date = '2020-01-01'
        else:
            min_date = _to_db_date(datetime.now() - timedelta(days=(days - 1)))
        sel_ = (f"SELECT rank, retrieved, headline, link ",
                f"FROM {self.table_name} WHERE rank <= {max_rank} ",
                f"AND retrieved >= '{min_date}';")
        with self.conn.cursor() as cur:
            cur.execute(sel_)
            news_tuple = cur.fetchall()
            news_struct = [dict(rank=t[0], date=t[1], headline=t[2], link=t[3])
                           for t in news_tuple]
            return news_struct 

    def retrieve_and_store_news(self):
        news = _get_top_10_tagesschau()
        self._write_news_to_db(news)

    def empty_table(self):
        del_cmd = f"DELETE FROM {self.table_name}"
        with self.conn.cursor() as cur:
            cur.execute(del_cmd)
            self.conn.commit()


def main():
    NC = NewsCrawler(table_name='news')
    #NC.retrieve_and_store_news()


if __name__ == '__main__':
    main()