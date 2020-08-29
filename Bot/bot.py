import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext, Filters
from typing import List

from parser import TaskListPage, ListItem

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class FreelanceBot:
    def __init__(self, token):
        self.__token = token
        self.cursor = TaskListPage()
        self.updater = Updater(token, use_context=True)

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
            keyboard = [[InlineKeyboardButton("description", callback_data=task.get_description(logger))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(update.effective_chat.id, text=task.markdown(),
                                     reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    def process_callback_query(self, update: Update, context: CallbackContext):
        query = update.callback_query
        context.bot.answer_callback_query(query.id, query.data, show_alert=True)

    def __add_handler(self, dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))
        dispatcher.add_handler(CommandHandler('last_10_tasks', self.get_last_10_tasks))
        dispatcher.add_handler(CallbackQueryHandler(self.process_callback_query))

    def run(self):
        self.__add_handler(self.updater.dispatcher)
        self.updater.start_polling()
        self.updater.idle()
