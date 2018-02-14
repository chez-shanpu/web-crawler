# -*- coding: utf-8 -*-

from shibboleth_login import ShibbolethClient
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing

name = "your username"
password = "your password"
dbname = 'KIT.db'


class EditDB:
    dates = []
    charges = []
    categories = []
    notices = []

    def __init__(self):
        with ShibbolethClient(name, password) as client:
            res = client.get('URL where you want to access')

        soup = BeautifulSoup(res.text, "lxml")

        EditDB.dates = soup.select('dd.nl_notice_date')
        EditDB.charges = soup.select('dd.nl_div_in_charge')
        EditDB.categories = soup.select('dd.nl_category')
        EditDB.notices = soup.select('dd.nl_notice')

    def createDB(self):
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()
            create_table = '''create table kit_notice (date VARCHAR, charge VARCHAR ,category VARCHAR , notice text )'''
            c.execute(create_table)
            conn.commit()

    def addinfo(self):
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()

            for date, charge, category, notice in zip(EditDB.dates, EditDB.charges, EditDB.categories, EditDB.notices):
                sql = 'insert into kit_notice (date, charge, category, notice) values (?,?,?,?)'
                info = (date.get_text(), charge.get_text(), category.get_text(), notice.get_text().replace("\t", ""))
                c.execute(sql, info)

            conn.commit()


if __name__ == "__main__":
    editdb = EditDB()
    editdb.createDB()
    editdb.addinfo()
