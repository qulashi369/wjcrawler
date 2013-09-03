#coding: utf8
import time
import os
import logging
from logging import Formatter, getLogger
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, g, abort
from flask import send_from_directory

from models import Book, Chapter
from database import db_session

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')

# 设置logger

loggers = [app.logger, getLogger('sqlalchemy'),
           getLogger('Tornado')]
file_handler = RotatingFileHandler(
    app.config['LOG'],
    maxBytes=500000,
    backupCount=5
)

file_handler.setLevel(app.config['LOG_LEVEL'])
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

for logger in loggers:
    logger.addHandler(file_handler)


@app.before_request
def before_request():
    if app.debug:
        g.start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    if app.debug:
        diff = time.time() - g.start_time
        app.logger.debug('Response Time: %f ms' % float(diff*1000))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    books = Book.query.all()
    recommend_books = books[:12]
    return render_template('index.html', **locals())


@app.route("/<int:id>")
def book(id):
    book = Book.query.filter_by(id=id).first()
    chapters = Chapter.query.filter_by(book_id=id)
    first_twelve_chapters = chapters.limit(12)
    last_six_chapters = chapters.order_by(Chapter.id.desc()).limit(6).all()
    last_six_chapters.reverse()
    chapter_count = chapters.count()
    return render_template('book.html', **locals())


@app.route("/<int:book_id>/chapters")
def chapters(book_id):
    book = Book.query.filter_by(id=book_id).first()
    chapters = db_session.query(Chapter.id,
                                Chapter.title
                                ).filter_by(book_id=book_id).all()
    return render_template('chapters.html', **locals())


@app.route("/<int:book_id>/<int:chapter_id>")
def content(book_id, chapter_id):
    book = Book.query.filter_by(id=book_id).first()
    chapter = Chapter.query.filter_by(id=chapter_id,
                                      book_id=book_id
                                      ).first()
    return render_template('content.html', **locals())


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
