# -*- coding: utf-8 -*- 
from flask import Flask, render_template, request,flash,escape
import requests

app = Flask(__name__)

def log_request(req:'flask_request',res:str) -> None:
    with open('vsearch.log','a') as log:
        print(req.form,req.remote_addr,req.user_agent,res,file=log,sep='|')

def geocode(consName,type)->str:
    parameters = {'consName': consName,'type':type,'key': 'adb9c9304658af5e037f9a2e42046ef1'}
    base = 'http://web.juhe.cn:8080/constellation/getAll'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = '这是查询结果:'
    results = geocode(phrase, letters)
    name = results['name']
    datetime = results['datetime']
    all = results['all']
    color = results['color']
    health = results['health']
    love = results['love']
    money = results['money']
    number = results['number']
    QFriend = results['QFriend']
    work = results['work']
    summary = results['summary']
    log_request(request,results)
    return render_template('results.html',
                            the_title=title,
                            the_phrase=phrase,
                            the_letters=letters,
                            the_name=name,
                            the_datetime=datetime,
                            the_all=all,
                            the_color=color,
                            the_health=health,
                            the_love=love,
                            the_money=money,
                            the_number=number,
                            the_QFriend=QFriend,
                            the_work=work,
                            the_summary=summary,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='欢迎使用星座运势测试网页')

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('输入数据','地址','浏览器','结果')
    return render_template('viewlog.html',
                           the_title='历史记录',
                           the_row_titles=titles,
                           the_data=contents,)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def not_found(e):
    return render_template('500.html')



if __name__ == '__main__':
    app.run(debug=True)
