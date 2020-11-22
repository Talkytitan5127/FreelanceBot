import sqlite3
import logging
from functools import wraps
from decouple import config

logger = logging.getLogger(__name__)


class Subscription:
    def __init__(self):
        pass

    def check_user(self, user_id):
        logger.info('check user')
        conn = sqlite3.connect(config('DB_TABLE'))
        cursor = conn.cursor()
        cursor.execute('select user_id from subscribe where user_id = ?', (user_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def add_subscribe(self, user_id):
        # args[0] - user_id
        logger.info('add subscribe')
        conn = sqlite3.connect(config('DB_TABLE'))
        cursor = conn.cursor()
        if self.check_user(user_id) is None:
            cursor.execute("insert into subscribe values (?, ?)", (user_id, 1))
        else:
            cursor.execute('update subscribe set is_active = 1 where user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    def remove_subscribe(self, user_id):
        # args[0] - user_id
        logger.info('remove subscribe')
        conn = sqlite3.connect(config('DB_TABLE'))
        cursor = conn.cursor()
        if self.check_user(user_id) is None:
            conn.close()
            return

        cursor.execute('update subscribe set is_active = 0 where user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    def check_subscribe(self, user_id):
        # args[0] - user_id
        logger.info('check subscribe')

        if self.check_user(user_id) is None:
            return False

        conn = sqlite3.connect(config('DB_TABLE'))
        cursor = conn.cursor()
        cursor.execute('select is_active from subscribe where user_id = ? limit 1', (user_id,))
        res = cursor.fetchone()
        conn.close()
        return bool(res[0])

    def get_users(self):
        logger.info('get_users')
        conn = sqlite3.connect(config('DB_TABLE'))
        cursor = conn.cursor()
        cursor.execute('select user_id from subscribe where is_active = 1')
        res = cursor.fetchall()
        conn.close()
        return res

    def list(self, user_id):
        logger.info('list subscribe')
