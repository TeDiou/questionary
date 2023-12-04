import sqlite3
import json
from dbOper import *

conn = OpenDb()
r, f = GetSqlResult('Select * from answers')
print(r, f)
# cur = conn.cursor()  
# cur.execute('DELETE from answers ')
# with sqlite3.connect("database.db") as con:  #建立与database.db数据库的连接
#     cur = con.cursor()    #获取游标
#     cur.execute("INSERT INTO users (id,name,password) VALUES (?,?,?)",(1,'admin','111') )     #添加数据，执行单条的sql语句
#     con.commit()     #提交事务

# conn.execute('drop table answers')
# conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)') #执行单条sql语句
# conn.close()       #关闭连接
# conn.execute('CREATE TABLE questionnaire (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, questions TEXT)') #执行单条sql语句
# conn.close()       #关闭连接
# conn.execute('CREATE TABLE answers (id INTEGER PRIMARY KEY AUTOINCREMENT, userId INTEGER, questionId INTEGER, answer TEXT)') #执行单条sql语句
conn.close()       #关闭连接

# with sqlite3.connect("database.db") as con:  #建立与database.db数据库的连接
#     cur = con.cursor()    #获取游标
#     cur.execute('delete from questionnaire where id = 2')
#     cur.execute("INSERT INTO questionnaire (id,title,questions) VALUES (?,?,?)",(2, '问卷调查', '["姓名","年龄","成绩单"]') )     #添加数据，执行单条的sql语句
#     con.commit()  

# data = '{"title":"Ti全明星阵容","questions":["1号位","2号位","3号位","4号位","5号位"]}'
# string = json.loads(data)
# print(type(string['questions']))