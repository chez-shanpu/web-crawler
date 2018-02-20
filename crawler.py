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

    def table_isexists(self, database_name, database_table_name):
        DBpath = "./" + database_name

        if (not os.path.isfile(DBpath)):
            print("There is no " + database_name)
            sys.exit(1)
        else:
            with closing(sqlite3.connect(database_name)) as conn:
                cur = conn.cursor()
                sql = "SELECT COUNT(*) FROM sqlite_master " \
                      "WHERE TYPE='table' AND name='" + database_table_name + "'"
                cur.execute(sql)
                if cur.fetchone()[0] == 0:
                    return False
                return True

    def createDBtable(self, database_name, database_table_name):
        with closing(sqlite3.connect(database_name)) as conn:
            c = conn.cursor()
            create_table = "create table " + database_table_name \
                           + " (date VARCHAR, charge VARCHAR ,category VARCHAR , notice text )"
            c.execute(create_table)
            conn.commit()

    def insert_row(self, database_name, database_table_name):
        with closing(sqlite3.connect(database_name)) as conn:
            cur = conn.cursor()

            for date, charge, category, notice \
                    in zip(EditDB.dates, EditDB.charges, EditDB.categories, EditDB.notices):
                sql = "insert into " + database_table_name \
                      + " (date, charge, category, notice) values (?,?,?,?)"
                row = (date.get_text(), charge.get_text(), category.get_text(),
                       notice.get_text().replace("\t", ""))
                cur.execute(sql, row)

            conn.commit()

    def delete_row(self, database_name, database_table_name, condition):
        with closing(sqlite3.connect(database_name)) as conn:
            cur = conn.cursor()
            if condition == "":
                sql = 'DELETE FROM ' + database_table_name
                cur.execute(sql)
            else:
                sql = 'DELETE FROM ' + database_table_name + ' WHERE ' + condition
                cur.execute(sql)
            conn.commit()

        print("Delete completed")

    def update_row(self, database_name, database_table_name, set_str, condition):
        with closing(sqlite3.connect(database_name)) as conn:
            cur = conn.cursor()
            if condition == "":
                sql = 'UPDATE ' + database_table_name + " SET " + set_str
                cur.execute(sql)
            else:
                sql = 'UPDATE ' + database_table_name + " SET " + set_str + ' WHERE ' + condition
                cur.execute(sql)
            conn.commit()

        print("Update completed")

    def print_table(self, database_name, database_table_name):
        with closing(sqlite3.connect(database_name)) as conn:
            cur = conn.cursor()
            sql = 'select * from ' + database_table_name
            cur.execute(sql)
            for row in cur.fetchall():
                print(row)

    def reacquire_table(self, database_name, database_table_name):
        with ShibbolethClient(name, password) as client:
            res = client.get(url)

        soup = BeautifulSoup(res, "lxml")
        EditDB.dates = soup.select('dd.nl_notice_date')
        EditDB.charges = soup.select('dd.nl_div_in_charge')
        EditDB.categories = soup.select('dd.nl_category')
        EditDB.notices = soup.select('dd.nl_notice')

        self.insert_row(database_name, database_table_name)
        print("Acquire completed")


if __name__ == "__main__":
    DBname = input("Please input DB name:")
    DBtable_name = input("Please input table name:")

    editDB = EditDB()
    if not editDB.table_isexists(DBname, DBtable_name):
        editDB.createDBtable(DBname, DBtable_name)
    editDB.insert_row(DBname, DBtable_name)

    while True:
        command = input("Please input command:")
        if command == "exit":
            break
        elif command == "print":
            editDB.print_table(DBname, DBtable_name)
        elif command == "delete":
            condition_str = input("Please input condition:")
            editDB.delete_row(DBname, DBtable_name, condition_str)
        elif command == "update":
            set_str = input("Please input SET sentence:")
            condition_str = input("Please input condition")
            editDB.update_row(DBname, DBtable_name, set_str, condition_str)
        elif command == "acquire":
            editDB.reacquire_table(DBname, DBtable_name)
        else:
            print("This command is wrong")
