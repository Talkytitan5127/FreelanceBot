import requests
import textwrap
from bs4 import BeautifulSoup
from typing import List

BASE_URL = 'https://freelance.habr.com/'


def smile(hex):
    return chr(int(hex, 16))


class TaskIndexPage:
    def __init__(self, task_url):
        self.url = BASE_URL + task_url

    def get_description(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            return 'Не получилось достать описание таски. Можете посмотреть его здесь: {}'.format(self.url)

        soup = BeautifulSoup(resp.text)
        task_description = soup.find('div', class_='task__description')
        return task_description.text


class ListItem:
    def __init__(self, article):
        # заголовок
        self.description = None
        header_article = article.find('div', class_='task__title')
        self.header = header_article.get('title')
        # href на task
        self.task_link = header_article.a.get('href')

        # отклик, просмотры, время публикации
        self.published_at = article.find('span', class_='params__published-at')
        self.published_at = self.published_at.span.string if self.published_at else 'нет времени публикации'
        self.count_views = article.find('span', class_='params__views')
        self.count_views = int(self.count_views.i.string) if self.count_views else 0
        self.count_responses = article.find('span', class_='params__responses')
        self.count_responses = int(self.count_responses.i.string) if self.count_responses else 0

        # цена вопроса
        price_aside = article.find('div', class_='task__price')
        negotiated_price = price_aside.find('span', class_='negotiated_price')

        # договорная
        if negotiated_price is not None:
            self.price = 0
            self.suffix = negotiated_price.string
        else:
            count_price = price_aside.find('span', class_='count')
            self.price = str(count_price.next)
            self.suffix = count_price.span.string

        self.tags = [tag.text for tag in article.find('ul', class_='tags').select('li')]

    def __str__(self):
        return '''
        Тема: {theme}
        Деньги: {cost} ({suffix})
        '''.format(theme=self.header, cost=self.price, suffix=self.suffix)

    def __eq__(self, other):
        if self.header == other.header:
            return True
        return False

    def __ne__(self, other):
        if self.header != other.header:
            return True
        return False

    def get_description(self):
        if self.description is None:
            self.description = TaskIndexPage(self.task_link).get_description()
        return self.description

    def get_task_page(self):
        return BASE_URL + self.task_link

    def markdown(self):
        return textwrap.dedent('''
        ## {header}
        {smile_views} {count_views}
        {smile_resps} {count_resps}
        {smile_cash} {count_cash} - {suffix}
        '''.format(header=self.header,
                   smile_views=smile('0x0001F440'), count_views=self.count_views,
                   smile_cash=smile('0x0001F4B0'), count_cash=self.price, suffix=self.suffix,
                   smile_resps=smile('0x0001F4DD'), count_resps=self.count_responses))


# на 0-ой позиции -> самая верхняя таска (самая новая)
class TaskListPage:
    def __init__(self):
        self.url = BASE_URL + 'tasks'

    def get_last_10_tasks(self) -> List[ListItem]:
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
