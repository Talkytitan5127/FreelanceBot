
from decouple import config

from Bot import FreelanceBot

if __name__ == '__main__':
    token = config('TOKEN')
    bot = FreelanceBot(token)
    bot.run()
