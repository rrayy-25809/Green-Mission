from flask import Flask, render_template
from dotenv import load_dotenv
from db import NotionDatabase
import os

# 플라스크 기본 설정
flask = Flask(__name__, template_folder='../dist/client', static_folder='../dist/assets')
flask.secret_key = 'LN$oaYB9-5KBT7G'
logger = flask.logger

# 데이터베이스 설정
load_dotenv()
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

@flask.route("/")
def main():
    return render_template("index.html")
