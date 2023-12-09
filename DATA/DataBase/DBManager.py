import mysql.connector
from DATA.DataBase.Constants import *


def connect_to_db():
    # print(mysql.connector.Timestamp.)
    return mysql.connector.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                                   database=DB_NAME)

