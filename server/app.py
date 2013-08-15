#coding: utf8

from flask import Flask

from config import DB_URL
from libs.db import get_db_session

app = Flask(__name__)

db_session = get_db_session(DB_URL)


@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
