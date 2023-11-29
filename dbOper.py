# -*- coding: utf-8 -*-
import sqlite3


# 建立数据库连接
def OpenDb():
    database = "./database.db"
    conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    return conn


# 获取数据库连接
def GetSql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    fields = []
    for field in cur.description:
        fields.append(field[0])

    result = cur.fetchall()
    # for item in result:
    #     print(item)
    cur.close()
    return result, fields


# 关闭数据库连接
def CloseDb(conn):
    conn.close()


def GetSqlResult(sql):
    conn = OpenDb()
    result, fields = GetSql(conn, sql)
    CloseDb(conn)
    return result, fields


def executeSql(sql):
    conn = OpenDb()
    cur = conn.cursor()
    print(sql)
    cur.execute(sql)    
    conn.commit()
    CloseDb(conn)