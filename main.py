
import requests
from bs4 import BeautifulSoup

import parser.parser as prs

if __name__ == '__main__':
    soup = None
    with open('htmls/task_page_1.html', 'r') as f:
        soup = BeautifulSoup(f.read())

    print()
