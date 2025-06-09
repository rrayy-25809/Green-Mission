from flask import Blueprint, jsonify, redirect, render_template, request, session, current_app
from server.db import NotionDatabase
from dotenv import load_dotenv
from datetime import datetime
import base64
import os

# 플라스크 기본 설정
bp = Blueprint('user', __name__)

# 데이터베이스 설정
load_dotenv()
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

@bp.route("/mypage", methods=["GET", "POST"])
def mypage():
    if "page_id" not in session:
        return "먼저 로그인 해주세요.", 403
    
    if request.method == "POST":
        page_id = session["page_id"]
        user_info = user_db.get_page_properties(page_id)
        join_day = datetime.fromisoformat(user_info.result["가입일"]["date"]["start"]['start']).date()

        properties = {
            '유저명': user_info.result["유저명"]["title"][0]["text"]["content"],
            '이메일': user_info.result["이메일"]["email"],
            '가입일': f"{join_day.year}년 {join_day.month}월 {join_day.day}일",
            '사용자 역할': user_info.result["사용자 역할"]["select"]["name"]["name"],
            '프로필 사진': user_info.result["프로필 사진"]["files"][0]["external"]["url"] if user_info.result["프로필 사진"]["files"] else None,
        }

        return jsonify(properties)

    return render_template("mypage.html")

@bp.route("/delete_account")
def delete_account():
    if "page_id" not in session:
        return redirect("/login")
    
    page_id = session["page_id"]
    user_db.delete_page(page_id)
    current_app.logger.info(f"사용자, {page_id} 가 계정을 삭제했습니다.")
    
    session.pop("page_id", None)

    return redirect("/login")


@bp.route("/change_profile", methods=["POST"])
def change_profile():
    img = request.files.get('image')
    page_id = session["page_id"]
    properties = user_db.get_page_properties(page_id)
    current_app.logger.info(f"유저 {page_id}가 프로필 사진 변경 시도")

    base64_encoded = base64.b64encode(img.stream)
    base64_string = base64_encoded.decode('utf-8')

    properties.set_files("프로필 사진",[base64_string])
    user_db.update_database_properties(page_id,)

    return "프로필 사진 업데이트 완료!", 200