from flask import Blueprint, redirect, render_template, request, session, current_app
from server.db import NotionDatabase
from datetime import datetime
from dotenv import load_dotenv
import os

# 플라스크 기본 설정
bp = Blueprint('auth', __name__)
# logger will be accessed via current_app.logger inside route functions

# 데이터베이스 설정
load_dotenv()
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"] +"@"+ request.form["email-sever"]
        password = request.form["password"]

        print(f"로그인 시도: 이메일={email}, 비밀번호={password}")

        for i in user_db.get_page_ids(): # 모든 페이지 ID를 가져와 반복
            i_data = user_db.get_page_properties(i).result  # 각 페이지의 속성 가져오기
            if i_data["이메일"]["email"] == email and i_data["비밀번호"]["rich_text"][0]["text"]["content"] == password:
                session["page_id"] = i # 로그인 성공 시 세션에 페이지 ID 저장
                return "로그인 성공!", 200
            
        return "로그인 실패: 이메일 또는 비밀번호가 잘못되었습니다.", 400

    elif "page_id" in session:
        return "이미 로그인되어 있습니다.", 400
    return render_template("login.html")

@bp.route("/logout")
def logout():
    current_app.logger.info(f"사용자, {session.get('page_id')} 가 로그아웃했습니다.")
    session.pop("page_id", None)
    return redirect("/login")  # 로그아웃 후 로그인 페이지로 리다이렉트

@bp.route("/signup", methods=["GET", "POST"])
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
        current_app.logger.info(f"회원가입 성공: {result}")
        
        return redirect("/login")
    return render_template("signup.html")
