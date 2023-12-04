import os
import sqlite3
import redis
from dbOper import *
from flask import Flask, render_template, request, flash, jsonify, redirect, url_for, session, g, \
    send_from_directory, make_response, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'questionnaireDemo'
from io import BytesIO
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter

redis_client = redis.Redis(host='localhost', port=6379, db=0)
#验证码
@app.route('/imgCode')
def imgCode():
    return imageCode().getImgCode()


class imageCode():
    '''
    验证码处理
    '''
    def rndColor(self):
        '''随机颜色'''
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def geneText(self):
        '''生成4位验证码'''
        return ''.join(random.sample(string.ascii_letters + string.digits, 4)) #ascii_letters是生成所有字母 digits是生成所有数字0-9

    def drawLines(self, draw, num, width, height):
        '''划线'''
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)
    def getImgCode(self):
        image, code = self.getVerifyCode()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        # 将验证码字符串储存在session中
        session['imageCode'] = code
        return response
    def getVerifyCode(self):
        '''生成验证码图形'''
        code = self.geneText()
        # 图片大小120×50
        width, height = 120, 50
        # 新图片对象
        im = Image.new('RGB', (width, height), 'white')
        # 字体
        font = ImageFont.truetype('app/static/arial.ttf', 40)
        # draw对象
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for item in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                      text=code[item], fill=self.rndColor(), font=font)
        # 划线
        self.drawLines(draw, 2, width, height)
        return im, code

@app.route('/', methods=['GET', 'POST'])  
@app.route('/Login.html', methods=['GET', 'POST'])  
@app.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    else:
        id = request.form.get('id')             
        password = request.form.get('password')    
        captcha = request.form.get('captcha').lower()  
        if captcha==session['imageCode'].lower():
            pass
        else:
            return u'图片验证码错误'
        sql = "select * from users where id = %s" % id
        result, _ = GetSqlResult(sql)
        print(result)
        if len(result)>0:
            
            if result[0][2] == password: 
                redis_client.set("userId", result[0][0])
                redis_client.set("userName", result[0][1])
                
                return redirect(url_for('index'))       
            else:
                return u'账号或密码错误'
        else:
            return u'不存在这个用户'
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    print(redis_client.get("userId").decode())
    result, _ = GetSqlResult("select * from questionnaire")
    return render_template('index.html', result = result)

@app.route('/questions', methods=['GET', 'POST'])
def question():
    id = request.values.get('id')
    result, _ = GetSqlResult("select * from questionnaire where id = %s" % id)
    print(result)
    return render_template('question.html', result = result)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    userId = redis_client.get("userId").decode()
    id = request.values.get('id')
    answer = []
    i = 0
    for key, value in request.values.items():
        if i == 0:
            i+=1
            continue
        print('{0}={1}<br/>'.format(key, value))
        answer.append(str(value))
    f = request.files['file']
    # print(request.values.get('birth'), request.values)
    if f.filename != None:
        basepath = os.path.dirname(__file__)
        filename = userId+"_"+id+"_"+f.filename
        answer.append(filename)
        upload_path = os.path.join(basepath, r'uploads', filename)
        f.save(upload_path)
    print('uploading ...')
    result, _ = GetSqlResult("select * from questionnaire")
    sql = 'INSERT INTO answers (userId,questionId,answer) VALUES (%s ,%s,"%s")' % (
    userId,id, str(answer))
    executeSql(sql)
    return render_template('index.html', result = result)

@app.route('/register', methods=['POST'])
def register():
    sql = "INSERT INTO users (id,name,password) VALUES (%s,'%s','%s')" % (
    request.form.get('id'), request.form.get('name'), request.form.get('password'))
    executeSql(sql)

@app.route('/myAnswers', methods=['GET', 'POST'])
def myAnswers():
    userId = redis_client.get("userId").decode()
    result, _ = GetSqlResult("select * from answers where userId = %s" % userId)
    titles = []
    for i in result:
        title, _ = GetSqlResult("select title from questionnaire where id = %s" % i[2])
        titles.append(title)
    result = zip(result, titles)
    print(titles)
    return render_template('myAnswers.html', result = result)   

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    id = request.values.get('id')
    result, _ = GetSqlResult("select * from answers where id = %s" % id)
    # print(result)
    questionId = result[0][2]
    answer = result[0][3]
    questionList, _ = GetSqlResult("select questions from questionnaire where id = %s" % questionId)
    questionList = list(eval(questionList[0][0]))
    questionList.append('上传文件名')
    print(eval(answer), questionList)
    result = zip(eval(answer), questionList)
    return render_template('answer.html', result = result)

@app.route('/search', methods=['GET', 'POST'])
def search():
    print(redis_client.get("userId").decode())
    keyword = request.values.get('keyword')
    print(keyword)
    result, _ = GetSqlResult("select * from questionnaire where title like '%{}%'".format(keyword))
    return render_template('index.html', result = result)

if __name__ == '__main__':
    app.run("127.0.0.1", debug=True)
