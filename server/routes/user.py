from flask import Blueprint, jsonify, redirect, render_template, request, session, current_app
from notion_database.properties import Properties
from server.db import NotionDatabase
from dotenv import load_dotenv
from datetime import datetime
import os

# 플라스크 기본 설정
bp = Blueprint('user', __name__)

# 데이터베이스 설정
load_dotenv()
user_db = NotionDatabase(os.getenv("USER_DB_ID"))
challenge_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))

@bp.route("/mypage", methods=["GET", "POST"])
def mypage():
    if "page_id" not in session:
        return "먼저 로그인 해주세요.", 403
    page_id = session["page_id"]

    return render_template("mypage.html", **user_info(page_id))

def user_info(page_id:str) -> dict:
    user_info = user_db.get_page_properties(page_id)
    join_day = datetime.fromisoformat(user_info.result["가입일"]["date"]["start"]).date()

    properties = {
        '유저명': user_info.result["유저명"]["title"][0]["text"]["content"],
        '이메일': user_info.result["이메일"]["email"],
        '가입일': f"{join_day.year}년 {join_day.month}월 {join_day.day}일",
        '사용자_역할': user_info.result["사용자 역할"]["select"]["name"],
        '프로필_사진': user_info.result["프로필 사진"]["files"][0]["file"]["url"] if user_info.result["프로필 사진"]["files"] else None,
        '참여한_챌린지': user_info.result["참여한 챌린지"]["rich_text"][0]["text"]["content"].split(",") if user_info.result["참여한 챌린지"]["rich_text"] else [],
        '응원_수': len(user_info.result["응원한 챌린지"]["rich_text"][0]["text"]["content"].split(",")) if user_info.result["응원한 챌린지"]["rich_text"] else 0,
        '챌린지_작성수' : challenge_make_count(page_id),
    }
    
    return properties

def challenge_make_count(page_id):
    for i in challenge_db.get_page_ids():
        challenge = challenge_db.get_page_properties(i)
        count = 0
        try:
            if challenge.result["챌린지 작성자"]["rich_text"][0]["text"]["content"] == page_id:
                count += 1
        except IndexError:
            continue

    return count

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
    url = request.form.get('url')
    page_id = session["page_id"]
    properties = Properties()

    # 파일 저장 (예: 업로드된 파일을 'uploads' 폴더에 저장)
    if img:
        path = os.path.join(current_app.instance_path, 'uploads', f'profile_{session["page_id"]}.jpg')
        img.save(path)
    else:
        return "프로필 사진이 없습니다.", 400

    properties.set_files("프로필 사진",[f"{url}/uploads/profile_{session["page_id"]}.jpg"])
    user_db.update_database_properties(page_id, properties)
    current_app.logger.info(f"사용자, {page_id} 가 프로필 사진을 변경했습니다.")
    
    return "프로필 사진 업데이트 완료!", 200