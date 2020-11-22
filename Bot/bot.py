import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext, Filters
from typing import List

from parser import TaskListPage, ListItem
from .Subscription import Subscription
from .TaskQueue import TaskQueue

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

subs = Subscription()
tasks = TaskQueue()


class FreelanceBot:
    def __init__(self, token):
        logger.info('init bot')
        self.__token = token
        self.cursor = TaskListPage()
        self.updater = Updater(token, use_context=True)
        self.job = self.updater.job_queue

    def echo(self, update: Update, context: CallbackContext):
        logger.info('echo method')
        context.bot.send_message(update.effective_chat.id, update.message.text)

    def get_last_10_tasks(self, update: Update, context: CallbackContext):
        logger.info('get last 10 tasks method')
        tasks = []
        try:
            tasks: List[ListItem] = self.cursor.get_last_10_tasks()
        except Exception as e:
            logger.info('catch exception: ' + str(e))
            context.bot.send_message(update.effective_chat.id, text='smth goes wrong, sorry')
        for task in tasks:
            keyboard = [[InlineKeyboardButton("Открыть страницу таски", url=task.get_task_page())]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(update.effective_chat.id, text=task.markdown(),
                                     reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    def subscribe(self, update: Update, context: CallbackContext):
        logger.info('subscribe method')
        args = context.args
        user = update.effective_user
        subs.add_subscribe(user.id)
        context.bot.send_message(user.id, text='success')

    def unsubscribe(self, update: Update, context: CallbackContext):
        logger.info('unsubscribe method')
        args = context.args
        user = update.effective_user
        subs.remove_subscribe(user.id)
        context.bot.send_message(user.id, text='success')

    def check(self, update: Update, context: CallbackContext):
        logger.info('check method')
        args = context.args
        user = update.effective_user
        result = subs.check_subscribe(user.id)
        if result:
            text = 'Вы подписаны'
        else:
            text = 'Вы не подписаны'
        context.bot.send_message(user.id, text=text)

    def start(self, update: Update, context: CallbackContext):
        user = update.effective_user
        context.bot.send_message(user.id, text='''
        Бот, присылающий описание тасков с "Хабр.Фриланс"
        /subscribe - подписаться на уведомления
        /unsubscribe - отписаться от уведомлений
        /check - проверить, подписан ли на уведомления
        ''')

    def task_watcher(self, context: CallbackContext):
        logger.info('task watcher')

        # update queue
        new_tasks = tasks.update()
        logger.info('New tasks - ' + str(new_tasks))

        # is need to notify users?
        if new_tasks is None:
            return

        # get user id to notify
        user_ids = subs.get_users()

        # notify users with new tasks
        for elem in user_ids:
            user_id = elem[0]
            logger.info(user_id)
            for i in range(len(new_tasks)-1, -1, -1):
                keyboard = [[InlineKeyboardButton("Открыть страницу таски", url=new_tasks[i].get_task_page())]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(user_id, text=new_tasks[i].markdown(),
                                         reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    def __add_handler(self, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler('subscribe', self.subscribe))
        dispatcher.add_handler(CommandHandler('unsubscribe', self.unsubscribe))
        dispatcher.add_handler(CommandHandler('check', self.check))
        dispatcher.add_handler(CommandHandler('start', self.start))

    def __add_jobs(self):
        self.job.run_repeating(self.task_watcher, interval=60 * 20, first=0)

    def run(self):
        self.__add_handler(self.updater.dispatcher)
        self.__add_jobs()
        self.updater.start_polling()
        self.updater.idle()
