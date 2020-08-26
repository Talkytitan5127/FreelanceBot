

BASE_URL = 'https://freelance.habr.com/'


class TaskListPage:
    def __init__(self):
        pass


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
        self.published_at = article.find('span', class_='params__published_at').i.string
        self.count_views = int(article.find('span', class_='params__views').i.string)
        self.count_responses = int(article.find('span', class_='params_responses').i.string)

        # цена вопроса
        price_aside = article.find('div', class_='task__price')
        negotiated_price = price_aside.find('span', class_='negotiated_price')

        # договорная
        if negotiated_price is not None:
            self.price = None
            self.suffix = negotiated_price.string
        else:
            count_price = price_aside.find('span', class_='count')
            self.price = count_price.string
            self.suffix = count_price.span.string
            self.tags = [tag.text for tag in article.find('ul', class_='tag').select('li')]
