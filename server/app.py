# coding: utf8
import time
import os

from flask import (Flask, render_template, g, url_for, send_from_directory,
                   session, flash, request, redirect, make_response)

from models import Book, Chapter, User
from database import db_session

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')


@app.before_request
def before_request():
    if app.debug:
        g.start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    if app.debug:
        diff = time.time() - g.start_time
        app.logger.debug('Response Time: %f ms' % float(diff * 1000))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def recent_reading(request):
    recent_reading = request.cookies.get('recent_reading')
    recent_book_chapters = []
    if recent_reading:
        for bid_cid in recent_reading.split(','):
            bid, cid = [int(id) for id in bid_cid.split(':', 1)]
            recent_book_chapters.append((Book.get(bid), Chapter.get(cid, bid)))
        recent_book_chapters = recent_book_chapters[:10]
    return recent_book_chapters


app.jinja_env.globals.update(recent_reading=recent_reading)


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    books = Book.query.all()
    recommend_books = books[:12]
    return render_template('index.html', **locals())


@app.route("/<int:book_id>")
def book(book_id):
    book = Book.get(book_id)
    chapters = Chapter.query.filter_by(book_id=book_id)
    first_twelve_chapters = chapters.limit(12)
    last_six_chapters = chapters.order_by(Chapter.id.desc()).limit(6).all()
    last_six_chapters.reverse()
    chapter_count = chapters.count()
    return render_template('book.html', **locals())


@app.route("/<int:book_id>/chapters")
def chapters(book_id):
    book = Book.get(book_id)
    chapters = db_session.query(Chapter.id, Chapter.title
                                ).filter_by(book_id=book_id).all()
    return render_template('chapters.html', **locals())


@app.route("/<int:book_id>/<int:chapter_id>")
def content(book_id, chapter_id):
    # NOTE read/set cookies for recent reading
    book = Book.get(book_id)
    chapter = Chapter.get(chapter_id, book_id)

    recent_reading = request.cookies.get('recent_reading')
    rec_book_chapters = []
    if recent_reading:
        for bid_cid in recent_reading.split(','):
            bid, cid = [int(id) for id in bid_cid.split(':', 1)]
            if not bid == book_id:
                rec_book_chapters.append(
                    (Book.get(bid), Chapter.get(cid, bid))
                )

    rec_book_chapters.insert(0, (book, chapter))
    rec_book_chapters = rec_book_chapters[:10]

    resp = make_response(render_template('content.html', **locals()))
    recent_reading_str = ','.join(['%s:%s' % (book.id, chapter.id)
                         for book, chapter in rec_book_chapters])
    resp.set_cookie('recent_reading', recent_reading_str)
    return resp


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('user', username=session.get('username')))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            empty_username_error = True
        elif not password:
            empty_password_error = True
        elif not User.login(username, password):
            login_error = True
        else:
            session['username'] = username
            return redirect(url_for('user', username=username))
    return render_template('login.html', **locals())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('user', username=session.get('username')))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            empty_username_error = True
        elif not password:
            empty_password_error = True
        elif not User.check_username(username):
            username_invalid_error = True
        elif User.is_exists(username):
            username_exists_error = True
        else:
            User.register(username, password)
            session['username'] = username
            return redirect(url_for('user', username=username))
    return render_template('register.html', **locals())


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/user/<username>")
def user(username):
    # NOTE  暂时无法查看他人页面
    if not session.get('username') == username:
        flash('请先登录帐号')
        return redirect(url_for('login'))
    else:
        user = User.get(username)
    return render_template('user.html', **locals())


@app.route('/favicon.ico')
def favicon():
    static_dir = os.path.join(app.root_path, 'static')
    return send_from_directory(static_dir, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return render_template('500.html'), 500


@app.errorhandler(404)
def not_found_error(exception):
    app.logger.debug(exception)
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
