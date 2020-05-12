import re
import os
import bs4

from nltk.corpus import stopwords
from multiprocessing import Pool


class SiteProcessor:

    def __init__(self):
        self.senti_map = _get_combined_senti_map()
        try:
            self.stopwords_german = set(stopwords.words('german'))
        except LookupError:
            import nltk
            nltk.download('stopwords')
            self.stopwords_german = set(stopwords.words('german'))

    def parse_page_content(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('p', attrs={'class': 'text small'})
        words = [w for elem in paragraphs
                 for w in elem.get_text().split(' ')]
        
        with Pool(processes=4) as pool:
            res = pool.map(self._clean_word, words)

        words = list(filter(lambda x: x is not None, res))
        return words

    def get_text_score(self, words):
        with Pool(processes=4) as pool:
            res = pool.map(self._word_score, words)
        
        senti_weights = list(filter(lambda x: x != 0.0, res))
        return sum(senti_weights) / len(senti_weights)

    def _word_score(self, word):
        return self.senti_map.get(word, 0.0)

    def _clean_word(self, word):
        word = ''.join([c for c in word.lower() if str.isalpha(c)])
        if word not in self.stopwords_german:
            return word
        else:
            return None


def _parse_sentiment_file(s_file):
    r_filter = r'([\S]*)\|[A-Z]*\s(-?[\d]*.[\d]*)\s([\S]*)'
    senti_map = dict()

    with open(s_file, 'r') as f:
        txt = f.readlines()

    for line in txt:
        [[stem, weight, versions]] = re.findall(r_filter, line)
        if versions:
            words = versions.split(',') + [stem]
        else:
            words = [stem]
        for word in words:
            senti_map[word.lower()] = float(weight)

    return senti_map


def _get_combined_senti_map():
    _path = os.path.dirname(os.path.abspath(__file__))
    n_file = os.path.join(_path, 'SentiWS/SentiWS_v2.0_Negative.txt')
    p_file = os.path.join(_path, 'SentiWS/SentiWS_v2.0_Positive.txt')
    senti_map = _parse_sentiment_file(n_file)
    senti_map.update(_parse_sentiment_file(p_file))
    return senti_map


if __name__ == '__main__':
    senti_map = _get_combined_senti_map()
    pass