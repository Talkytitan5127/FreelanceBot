import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://freelance.habr.com/'


class TaskListPage:
    def __init__(self):
        self.url = BASE_URL + 'tasks'

    def get_last_10_tasks(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            return []

        result = []
        soup = BeautifulSoup(resp.text)
        articles = soup.find_all('article', limit=10)
        for article in articles:
            article = ListItem(article)
            result.append(article)
        return result


class TaskIndexPage:
    def __init__(self, task_url):
        self.url = BASE_URL + task_url


class ListItem:
    def __init__(self, article):
        # заголовок
        header_article = article.find('div', class_='task__title')
        self.header = header_article.get('title')
        # href на task
        self.task_link = header_article.a.get('href')

        # отклик, просмотры, время публикации
        self.published_at = article.find('span', class_='params__published-at').span.string
        self.count_views = int(article.find('span', class_='params__views').i.string)
        self.count_responses = int(article.find('span', class_='params__responses').i.string)

        # цена вопроса
        price_aside = article.find('div', class_='task__price')
        negotiated_price = price_aside.find('span', class_='negotiated_price')

        # договорная
        if negotiated_price is not None:
            self.price = None
            self.suffix = negotiated_price.string
        else:
            count_price = price_aside.find('span', class_='count')
            self.price = count_price.text
            self.suffix = count_price.span.string

        self.tags = [tag.text for tag in article.find('ul', class_='tags').select('li')]

    def __str__(self):
        return '''
        Тема: {theme}
        Деньги: {cost} ({suffix})
        '''.format(theme=self.header, cost=self.price, suffix=self.suffix)

    def get_description(self):
        return 'very soon'