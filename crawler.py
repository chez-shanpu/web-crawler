# -*- coding: utf-8 -*-

from shibboleth_login import ShibbolethClient
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing
import os.path

name = "your name"
password = "your password"
url = "URL where you want to access"


class EditDB:
    dates = []
    charges = []
    categories = []
    notices = []

    def __init__(self):
        with ShibbolethClient(name, password) as client:
            res = client.get(url)

        soup = BeautifulSoup(res.text, "lxml")

        EditDB.dates = soup.select('dd.nl_notice_date')
        EditDB.charges = soup.select('dd.nl_div_in_charge')
        EditDB.categories = soup.select('dd.nl_category')
        EditDB.notices = soup.select('dd.nl_notice')

    def table_isexists(self, database_name):
        DBpath = "./" + database_name
        if (not os.path.isfile(DBpath)):
            print("There is no " + database_name)
        else:
            with closing(sqlite3.connect(database_name)) as conn:
                cur = conn.cursor()
                cur.execute("""
                        SELECT COUNT(*) FROM sqlite_master 
                        WHERE TYPE='table' AND name='kit_notice'
                        """)
                if cur.fetchone()[0] == 0:
                    return False
                return True

    def createDBtable(self, database_name):
        with closing(sqlite3.connect(database_name)) as conn:
            c = conn.cursor()
            create_table = '''create table kit_notice (date VARCHAR, charge VARCHAR ,category VARCHAR , notice text )'''
            c.execute(create_table)
            conn.commit()

    def add_row(self, database_name):
        with closing(sqlite3.connect(database_name)) as conn:
            c = conn.cursor()

            for date, charge, category, notice in zip(EditDB.dates, EditDB.charges, EditDB.categories, EditDB.notices):
                sql = 'insert into kit_notice (date, charge, category, notice) values (?,?,?,?)'
                row = (date.get_text(), charge.get_text(), category.get_text(), notice.get_text().replace("\t", ""))
                c.execute(sql, row)

            conn.commit()


if __name__ == "__main__":
    DBname = 'KIT.db'

    editDB = EditDB()
    if not editDB.table_isexists(DBname):
        editDB.createDBtable(DBname)
    editDB.add_row(DBname)
