from flask import Blueprint, redirect, render_template, session, current_app
from server.db import NotionDatabase
from dotenv import load_dotenv
import os

# 플라스크 기본 설정
bp = Blueprint('user', __name__)

# 데이터베이스 설정
load_dotenv()
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

@bp.route("/mypage")
def mypage():
    if "page_id" not in session:
        return "먼저 로그인 해주세요.", 403
    page_id = session["page_id"]
    user_info = user_db.get_page_properties(page_id)
    return render_template("mypage.html",user_info=user_info)

@bp.route("/delete_account")
def delete_account():
    if "page_id" not in session:
        return redirect("/login")
    
    page_id = session["page_id"]
    user_db.delete_page(page_id)
    current_app.logger.info(f"사용자, {page_id} 가 계정을 삭제했습니다.")
    
    session.pop("page_id", None)

    return redirect("/login")