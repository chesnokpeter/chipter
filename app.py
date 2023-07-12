from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
import json
import mysql.connector
from server.toolsdb import get_id_from_user
from server.reg import registration
from server.login import logging
from server.posts import get_all_posts, send_post
from server.password_hash import hashed, dehashed

app = Flask(__name__, template_folder='./website', static_folder='./website/static')


socketio = SocketIO(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        a = get_id_from_user(username, conn)
        if a:
            return render_template('reg.html', error='Такой ник уже существует')
        password = hashed(password)
        registration(username, password, conn, cfg)
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('reg.html', error='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        a = get_id_from_user(username, conn)
        if not a:
            return render_template('login.html', error='Логин или пароль неправильные')
        hashed = logging(username, conn, cfg)
        a = dehashed(password, hashed)
        if not a:
            return render_template('login.html', error='Логин или пароль неправильные')
        else:
            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('login.html', error='')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        username = session['username']
        a = get_id_from_user(username, conn)
        if not a:
            return redirect(url_for('login'))
        posts = get_all_posts(conn, cfg)
        return render_template('homenew.html', username=username, posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    content = data['content']
    send_post(username, content, conn, cfg)
    send({'username': username, 'content': content}, broadcast=True)

@app.route('/more_posts', methods=['POST'])
def get_posts():
    offset = int(request.form['offset'])
    limit = 10
    posts = get_all_posts(conn, cfg, limit, offset)
    return {'posts': posts}






if __name__ == '__main__':
    global cfg, conn

    with open('config.json', 'r') as f:
        cfg = json.loads(f.read())
    app.config['SECRET_KEY'] = cfg['secretKey']
    conn = mysql.connector.connect(
        host=cfg['mysql']['host'],
        user=cfg['mysql']['user'],
        password=cfg['mysql']['password'],
        database=cfg['mysql']['database']
    )
    socketio.run(app, port=9999, log_output=True)