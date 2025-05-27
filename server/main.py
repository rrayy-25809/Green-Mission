from flask import Flask, redirect, render_template, request, session, url_for
from dotenv import load_dotenv
from server.db import NotionDatabase
from datetime import datetime
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

@flask.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for i in user_db.get_page_ids(): # 모든 페이지 ID를 가져와 반복
            i_data = user_db.get_page_properties(i).result  # 각 페이지의 속성 가져오기
            if i_data["이메일"]["email"] == email and i_data["비밀번호"]["rich_text"][0]["text"]["content"] == password:
                session["page_id"] = i # 로그인 성공 시 세션에 페이지 ID 저장
                return redirect(url_for("main"))  # 로그인 성공 시 메인 페이지로 리다이렉트

        return "로그인 실패: 이메일 또는 비밀번호가 잘못되었습니다.", 400
        
    elif "page_id" in session:
        return "이미 로그인되어 있습니다.", 400
    return render_template("login.html")

@flask.route("/logout")
def logout():
    logger.info(f"사용자, {session["page_id"]} 가 로그아웃했습니다.")
    session.pop("page_id", None)
    return redirect(url_for("login"))  # 로그아웃 후 로그인 페이지로 리다이렉트

@flask.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        properties = {
            '유저명' : request.form["username"],
            '이메일' : request.form["email"],
            '비밀번호' : request.form["password"],
            '가입일' : datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '+0900',
            '사용자 역할' : "유저",
            '전화번호' : request.form["phone_number"]
        }
        result = user_db.create_database_page(properties)
        logger.info(f"회원가입 성공: {result}")
        
        return redirect(url_for("login"))