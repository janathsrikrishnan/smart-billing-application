import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class CreateTable:

    """ create database files and add tables in it"""
    # setup the connection with sqlite3 and open the billing database file
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("billing.db")

    if not database.open():
        print("Unable to connect the database")
        sys.exit(1)                                                                                                     # error code

    insertquery = QSqlQuery()

    # create table items using
    insertquery.exec_("""CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(30) NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL)""")

    # for inserting data into table used prepare
    insertquery.prepare("""INSERT INTO items (
    name, quantity, price)
    VALUES (?, ?, ?)""")

    insertquery.addBindValue("Null")
    insertquery.addBindValue(0)
    insertquery.addBindValue(0)
    insertquery.exec_()
    bill_query = QSqlQuery()
    # create billbook table
    bill_query.exec_("""CREATE TABLE billBook (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(30) NOT NULL,
    number INTEGER NOT NULL,
    items TEXT NOT NULL,
    amount REAL NOT NULL)""")

    bill_query.prepare("""INSERT INTO billBook (
    name, number, items, amount)
    VALUES (?, ?, ?, ?)""")
    print("table created success")

    bill_query.addBindValue("null")
    bill_query.addBindValue(0)
    bill_query.addBindValue("null")
    bill_query.addBindValue(0.0)
    bill_query.exec_()
    sys.exit(0)

if __name__ == '__main__':
    CreateTable()
