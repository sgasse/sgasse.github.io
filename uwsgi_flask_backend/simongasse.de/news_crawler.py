import re
import requests
import pg8000

def get_top_10_tagesschau():
    def _clean(in_str):
        return in_str.replace('"', '')

    page = "http://www.tagesschau.de"
    response = requests.get(page)
    m = re.findall(r'<li><a title="(.+)" href="(.+)"><span', response.text)
    news = [(ind + 1, _clean(headline), _clean(f'{page}{link}'))
            for ind, (headline, link) in enumerate(m)]
    return news


def maybe_initialize_table(conn, name='news'):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id serial PRIMARY KEY,
                    rank integer,
                    headline varchar,
                    link varchar);
                """)
        conn.commit()
    return True


def write_news_to_db(conn, news, table_name):
    insert = f'INSERT INTO {table_name} (rank, headline, link) VALUES'
    vals = [f"({rank}, '{headline}', '{link}');"
            for rank, headline, link in news]
    with conn.cursor() as cur:
        for val in vals:
            sql_cmd = f'{insert}\n   {val};'
            cur.execute(sql_cmd)
        conn.commit()


def _setup_db_connection():
    conn = pg8000.connect(database='postgres', user='postgres',
                          password='docker', host='127.0.0.1', port=5432)
    return conn


def main():
    table_name = 'news'
    conn = _setup_db_connection()
    maybe_initialize_table(conn, name=table_name)
    news = get_top_10_tagesschau()
    write_news_to_db(conn, news, table_name)
