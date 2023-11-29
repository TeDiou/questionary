import sqlite3
from dbOper import *

conn = OpenDb()
r, f = GetSqlResult('Select * from users')
print(r, f)

# with sqlite3.connect("database.db") as con:  #建立与database.db数据库的连接
#     cur = con.cursor()    #获取游标
#     cur.execute("INSERT INTO users (id,name,password) VALUES (?,?,?)",(1,'admin','111') )     #添加数据，执行单条的sql语句
#     con.commit()     #提交事务

# conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)') #执行单条sql语句
# conn.close()       #关闭连接