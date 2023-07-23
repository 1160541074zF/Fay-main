import sqlite3
import time
import threading
import functools


def synchronized(func):
  @functools.wraps(func)


  def wrapper(self, *args, **kwargs):
    with self.lock:

      return func(self, *args, **kwargs)

      return wrapper


class Content_Db:

    def __init__(self) -> None:
        self.lock = threading.Lock()


  #初始化
    def init_db(self):
        conn = sqlite3.connect('fay.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE user_inform
            (id INTEGER PRIMARY KEY     user_id,
            name          char(10),
            gender        char(10),
            age           char(10),
            createtime         Int);''')
        conn.commit()
        conn.close()
