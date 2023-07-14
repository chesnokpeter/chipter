from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
import json
import mysql.connector
from server.toolsdb import get_id_from_user, get_post_from_id
from server.reg import registration
from server.login import logging
from server.posts import get_all_posts, send_post, get_last_id_post, get_username_from_id_post
from server.password_hash import hashed, dehashed
from server.comments import get_all_comments, send_comment
from server.user import get_posts_from_userid

app = Flask(__name__, template_folder='./website')


socketio = SocketIO(app)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        if len(username) > 30:
            return render_template('reg.html', error='Ник не может больше 30 символов')
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


@app.route('/home', methods=['GET'])
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

@app.route('/more_posts', methods=['POST'])
def get_posts():
    offset = int(request.form['offset'])
    limit = 10
    posts = get_all_posts(conn, cfg, limit, offset)
    return {'posts': posts}


@app.route('/post<post>', methods=['GET'])
def get_post(post):
    idpost = get_post_from_id(post, conn)
    if not idpost:
        return redirect(url_for('home'))
    cmnt = get_all_comments(post, conn, cfg)
    if not cmnt:
        cmnt = []
    usernameid = get_id_from_user(idpost[2], conn)
    if 'username' in session:
        username = session['username']
        a = get_id_from_user(username, conn)
        if not a:
            return redirect(url_for('login'))
        return render_template('post.html', post=idpost, comment=cmnt, authorized=True, username=username, userid=usernameid)
    else:
        return render_template('post.html', post=idpost, comment=cmnt, authorized=False, userid=usernameid)
    


@app.route('/user<userid>', methods=['GET'])
def get_userpage(userid):
    posts = get_posts_from_userid(userid, conn, cfg)
    print(posts)
    if not posts:
        return redirect(url_for('home'))
    return render_template('userpage.html', postsss=posts, author=posts[0][2])

@socketio.on('message',  namespace='/home')
def handle_message(data):
    username = session.get('username')
    content = data['content']
    send_post(username, content, conn, cfg)
    lastidpost = get_last_id_post(conn, cfg)
    send({'username': username, 'content': content, 'id' : lastidpost}, broadcast=True)

@socketio.on('newcmnt', namespace='/post')
def handle_comment(data):
    username = session.get('username')
    content = data['content']
    idpost = data['idpost']
    iduser = get_id_from_user(username, conn)
    send_comment(idpost, iduser, username, content, conn, cfg)
    send({'username': username, 'content': content, 'idpost': idpost}, broadcast=True)






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