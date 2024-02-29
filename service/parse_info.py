import requests
from bs4 import BeautifulSoup
import lxml


class CollectDescription:
    def __init__(self, image_url):
        self.image_url = image_url
        self.domain = 'https://bidlot.ru'
        self.collected_info = None
        self.title = None
        self.description = None
        self.start()

    def start(self):
        self.collect_words()
        self.get_title()
        self.get_description()

    def collect_words(self):
        words = list()
        soup = BeautifulSoup(get_page(self.image_url).text, 'lxml')
        soup = soup.find_all('span', attrs={'class': 'Button2-Text'})
        for each in soup:
            words.append(each.getText())
        self.collected_info = words[:-1]

    def get_title(self):
        short_title = list()
        max_chars = 128
        for word in self.collected_info:
            max_chars -= len(word) + 1
            if max_chars > 0:
                short_title.append(word)
        self.title = ' '.join(self.collected_info).title()

    def get_description(self):
        self.description = ' '.join(self.collected_info)


def get_page(image_url):
    url = 'https://bidlot.ru' + image_url
    payload = {
        'source': 'collections',
        'rpt': 'imageview',
        'url': url
    }
    response = requests.get(f'https://yandex.ru/images/search/', params=payload)
    response.raise_for_status()
    return response
