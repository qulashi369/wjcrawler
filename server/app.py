#coding: utf8
import time
import os

from flask import Flask, render_template, g
from flask import send_from_directory

from config import DB_URL
from models import Book, Chapter
from libs.db import get_db_session

app = Flask(__name__, template_folder='templates')


def db_session():
    return get_db_session(DB_URL)


@app.before_request
def before_request():
    if app.debug:
        g.start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    if app.debug:
        diff = time.time() - g.start_time
        app.logger.debug('Response Time: %f ms' % float(diff*1000))


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    session = db_session()
    books = session.query(Book).all()
    session.close()
    recommend_books = books[:12]
    return render_template('index.html', **locals())


@app.route("/<int:id>")
def book(id):
    session = db_session()
    book = session.query(Book).filter_by(id=id).first()
    chapters = session.query(Chapter).filter_by(book_id=id)
    first_twelve_chapters = chapters.limit(12)
    last_six_chapters = chapters.order_by(Chapter.id.desc()).limit(6).all()
    last_six_chapters.reverse()
    chapter_count = chapters.count()
    session.close()
    return render_template('book.html', **locals())


@app.route("/<int:book_id>/chapters")
def chapters(book_id):
    session = db_session()
    book = session.query(Book).filter_by(id=book_id).first()
    chapters = session.query(Chapter.id,
                                  Chapter.title).filter_by(book_id=book_id).all()
    session.close()
    return render_template('chapters.html', **locals())


@app.route("/<int:book_id>/<int:chapter_id>")
def content(book_id, chapter_id):
    session = db_session()
    book = session.query(Book).filter_by(id=book_id).first()
    chapter = session.query(Chapter).filter_by(id=chapter_id,
                                                    book_id=book_id).first()
    session.close()
    return render_template('content.html', **locals())


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
