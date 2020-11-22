import sqlite3 as s3

from decouple import config


def init():
    conn = s3.connect(config('DB_TABLE'))
    cursor = conn.cursor()
    cursor.execute('create table subscribe (user_id numeric, is_active boolean)')
    cursor.execute('create index subscribe_index on subscribe(user_id)')
    conn.commit()
    conn.close()
