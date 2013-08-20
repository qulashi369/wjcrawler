#coding: utf8

from flask import Flask, render_template

from config import DB_URL
from models import Book, Chapter, Category
from libs.db import get_db_session

app = Flask(__name__, template_folder='templates')
db_session = get_db_session(DB_URL)


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    books = db_session.query(Book).limit(12)
    return render_template('index.html',**locals())


@app.route("/book/<id>")
def book(id):
    return render_template('book.html')


@app.route("/chapter")
def chapters():
    return render_template('chapters.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
