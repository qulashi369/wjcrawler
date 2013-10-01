# coding: utf8
import time
import os
import json

from flask import (Flask, render_template, g, url_for, send_from_directory,
                   flash, request, redirect, make_response, jsonify,
                   current_app)
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user, user_logged_in,
                             user_loaded_from_cookie)
from flask.ext.principal import (Principal, Permission, RoleNeed, UserNeed,
                                 identity_loaded, identity_changed, Identity,
                                 AnonymousIdentity)

from models import Book, Chapter, User, Favourite, UpdateTask, UpdateLog
from consts import FAILED
from database import db_session

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')

login_manager = LoginManager(app)
principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))


@login_manager.user_loader
def load_user(uid):
    return User.get_by_uid(uid)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'is_admin'):
        if current_user.is_admin():
            identity.provides.add(RoleNeed('admin'))


@user_loaded_from_cookie.connect_via(app)
def on_user_loaded_from_cookie(sender, user):
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))


@user_logged_in.connect_via(app)
def on_user_logged_in(sender, user):
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))


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
        for bid_cid in recent_reading.split('|'):
            bid, cid = [int(id) for id in bid_cid.split(':', 1)]
            book = Book.get(bid)
            chapter = Chapter.get(cid, bid)
            if (book and chapter):
                recent_book_chapters.append((book, chapter))
        recent_book_chapters = recent_book_chapters[:10]
    return recent_book_chapters


app.jinja_env.globals.update(recent_reading=recent_reading)


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    books = Book.query.all()
    recommend_books = books[:12]
    return render_template('index.html', **locals())


@app.route("/<int:bid>")
@app.route("/book/<int:bid>")
def book(bid):
    is_faved = False
    if not current_user.is_anonymous():
        is_faved = Favourite.is_faved(current_user.id, bid)

    book = Book.get(bid)
    chapters = Chapter.query.filter_by(book_id=bid)
    last_twelve_chapters = chapters.order_by(Chapter.id.desc()).limit(12)
    first_six_chapters = chapters.limit(6).all()
    first_six_chapters.reverse()
    return render_template('book.html', **locals())


@app.route("/<int:bid>/chapters")
@app.route("/book/<int:bid>/chapters")
def chapters(bid):
    book = Book.get(bid)
    chapters = Chapter.get_id_titles(book.id)
    return render_template('chapters.html', **locals())


@app.route("/<int:bid>/<int:cid>")
@app.route("/book/<int:bid>/<int:cid>")
def content(bid, cid):
    book = Book.get(bid)
    chapter = Chapter.get(cid, bid)

    # NOTE read/set cookies for recent reading
    recent_reading = request.cookies.get('recent_reading')
    rec_book_chapters = []
    if recent_reading:
        for bid_cid in recent_reading.split('|'):
            _bid, _cid = [int(id) for id in bid_cid.split(':', 1)]
            if not _bid == bid:
                rec_book_chapters.append(
                    (Book.get(_bid), Chapter.get(_cid, _bid))
                )
    rec_book_chapters.insert(0, (book, chapter))
    rec_book_chapters = rec_book_chapters[:10]

    resp = make_response(render_template('content.html', **locals()))
    recent_reading_str = '|'.join(['%s:%s' % (book.id, chapter.id)
                         for book, chapter in rec_book_chapters])
    resp.set_cookie('recent_reading', recent_reading_str)
    return resp


@app.route("/login", methods=['GET', 'POST'])
def login():
    target = request.values.get('target', '')
    if not current_user.is_anonymous():
        return redirect(url_for('uid', uid=current_user.id))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        target = request.form.get('target')
        if not username:
            empty_username_error = True
        elif not password:
            empty_password_error = True
        else:
            user = User.login(username, password)
            if not user:
                login_error = True
            else:
                login_user(user, remember=True)
                if target:
                    return redirect(target)
                return redirect(url_for('user', uid=user.id))
    return render_template('login.html', **locals())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if not current_user.is_anonymous():
        return redirect(url_for('user', uid=current_user.id))
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
            user = User.register(username, password)
            login_user(user, remember=True)
            return redirect(url_for('user', uid=current_user.id))
    return render_template('register.html', **locals())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('index'))


@app.route("/user", defaults={'uid': None})
@app.route("/user/<int:uid>")
def user(uid):
    if current_user.is_anonymous():
        flash(u'请先登录帐号', 'error')
        return redirect(url_for('login'))
    elif uid and not (uid == current_user.id):
        return '无法查看他人主页'
    else:
        favs = current_user.get_favs()
        favs_count = len(favs)
        return render_template('user.html', **locals())


@app.route("/fav/<int:bid>/", methods=['POST'])
def fav(bid):
    if current_user.is_anonymous():
        flash(u'请先登录帐号，再收藏小说', 'error')
        return (
            redirect(url_for('login', target=url_for('book', bid=bid)))
        )
    else:
        action = request.form.get('action', 'fav')
        refer = request.form.get('refer', '')
        if action == 'fav':
            Favourite.add(current_user.id, bid)
        else:
            Favourite.remove(current_user.id, bid)
        if refer == 'user_page':
            return redirect(url_for('user', uid=current_user.id))
        return redirect(url_for('book', bid=bid))


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


'''
======================================
            爬虫相关API
======================================
'''


@app.route('/api/update/tasks')
def tasks():
    limit = int(request.args.get('limit', 20))
    tasks = UpdateTask.get_tasks(limit)
    UpdateTask.delete_tasks(tasks)
    return jsonify(tasks=[task.serialize for task in tasks])


@app.route('/api/update/<int:bid>', methods=['POST'])
def update_book(bid):
    data = json.loads(request.data)
    assert data, 'no data...'
    chapter = data.get('chapter')
    crawler = data.get('crawler', '')
    title = chapter.get('title', '')
    type = chapter.get('type', 'text')
    if type == 'text':
        content = chapter.get('content', '')
    elif type == 'image':
        content = ''
    chapter = Chapter.add(bid, title, content)
    log = UpdateLog.add(bid, chapter.id, crawler)
    return jsonify(status='success', log=log.id)


@app.route('/api/update/error/<int:bid>', methods=['POST'])
def update_error(bid):
    data = json.loads(request.data)
    assert data, 'no data...'
    latest_chapter = data.get('latest_chapter')
    crawler = data.get('crawler')
    log = UpdateLog.add(bid, 0, crawler, type=FAILED,
                        latest_chapter=latest_chapter)
    return jsonify(status='success', log=log.id)


'''
======================================
            后台相关页面
======================================
'''


@app.route('/ash', methods=['GET'])
@admin_permission.require(http_exception=404)
def ash():
    return redirect(url_for('m_book', page=1))


@app.route('/ash/m_book', methods=['GET'], defaults={'page': 1})
@app.route('/ash/m_book/page/<int:page>', methods=['GET'])
@admin_permission.require(http_exception=404)
def m_book(page):
    limit = 50
    start = limit * (page - 1)
    books = Book.query.slice(start, limit + start).all()
    if len(books) < limit:
        has_next = False
    else:
        has_next = True
    return render_template('admin/book.html', **locals())


@app.route('/ash/m_book/modal/<int:bid>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=404)
def m_book_modal(bid):
    book = Book.get(bid)
    if request.method == 'POST':
        title = request.form.get('bookname')
        author = request.form.get('author')
        description = request.form.get('description')
        status = request.form.get('status')
        book.update(title, author, description, status)
        return redirect(request.referrer)
    return render_template('admin/book_modal.html', **locals())


@app.route('/ash/m_book/modal/delete', methods=['POST'])
@admin_permission.require(http_exception=404)
def m_book_delete():
    bid = request.form.get('bid')
    Book.delete(bid)
    return redirect(request.referrer)


@app.route('/ash/m_chapter/<int:bid>', methods=['GET'], defaults={'page': 1})
@app.route('/ash/m_chapter/<int:bid>/page/<int:page>', methods=['GET'])
@admin_permission.require(http_exception=404)
def m_chapter(bid, page):
    limit = 50
    start = limit * (page - 1)
    chapters = Chapter.query.filter_by(
        book_id=bid).slice(start, limit + start).all()
    if len(chapters) < limit:
        has_next = False
    else:
        has_next = True
    return render_template('admin/chapter.html', **locals())


@app.route('/ash/m_chapter/modal/<int:bid>/<int:cid>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=404)
def m_chapter_modal(bid, cid):
    chapter = Chapter.get(cid, bid)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        chapter.update(title, content)
        return redirect(request.referrer)
    return render_template('admin/chapter_modal.html', **locals())


@app.route('/ash/m_chapter/modal/delete', methods=['POST'])
@admin_permission.require(http_exception=404)
def m_chapter_delete():
    bid = request.form.get('bid')
    cid = request.form.get('cid')
    Chapter.delete(bid, cid)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
