import sqlite3 as sql
import os


def create_db():
    if os.path.isfile('db.db'):
        os.remove('db.db')

    with sql.connect('db.db') as db:
        # Если файл уже существует, то функция connect осуществит подключение к нему.

        # Еще один способ создания баз данных с помощью SQLite в Python — создание их в памяти.
        # Это отличный вариант для тестирования, ведь такие базы существуют только в оперативной памяти.
        #
        # conn = sqlite3.connect(:memory:)

        curs = db.cursor()

        curs.execute("PRAGMA foreign_keys = ON")
        # Сохраняем изменения
        db.commit()

        # создание таблицы masters
        curs.execute("""CREATE TABLE IF NOT EXISTS masters(
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        description TEXT,
                        instagram_username TEXT,
                        adress TEXT,
                        telegram_username TEXT)
                    """)
        # Сохраняем изменения
        db.commit()


