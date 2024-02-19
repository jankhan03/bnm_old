import sqlite3 as sql
import datetime




def add_master(data_about_master: list):

    with sql.connect('masters.db') as db:

        curs = db.cursor()

        curs.execute("""INSERT INTO masters (name, description, instagram_username, telegram_username, photo_id)
                          VALUES (?, ?, ?, ?, ?)
                        """,
                     data_about_master)

        db.commit()


def get_masters_list():

    with sql.connect('masters.db') as db:

        curs = db.cursor()

        curs.execute("""select name, description, telegram_username, instagram_username, photo_id
                        from masters
                        """)

        return curs.fetchall()

