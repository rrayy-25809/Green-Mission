from flask import Blueprint, jsonify, request, current_app, render_template, session
from server.db import NotionDatabase
from dotenv import load_dotenv
import os

# 플라스크 기본 설정
bp = Blueprint('challenge', __name__)

# 데이터베이스 설정
load_dotenv()
# challenge_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))
challenge_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

def get_author_name(author_id):
    try:
        author_page = user_db.get_page_properties(author_id[0]["text"]["content"])
        return author_page.result["유저명"]["title"][0]["text"]["content"]
    except KeyError:
        return "Green Mission"

def get_challenge_data(page_id):
    page = challenge_db.get_page_properties(page_id)
    return {
        "챌린지 ID": page_id,
        "챌린지 제목": page.result["챌린지 제목"]['title'][0]['text']['content'],
        "챌린지 작성자": get_author_name(page.result["챌린지 작성자"]["rich_text"]),
        "챌린지 아이콘": page.result["챌린지 아이콘"]["files"][0]["external"]["url"],
        "챌린지 설명": page.result["챌린지 설명"]["rich_text"][0]["text"]["content"],
    }

@bp.route('/challenge/<what_kinda>', methods=['POST'])
def post_challenge(what_kinda):
    if what_kinda == "s":
        data = [get_challenge_data(i) for i in challenge_db.get_page_ids()]
        return jsonify(data)
    elif what_kinda == "user":
        user_properties = user_db.get_page_properties(session["page_id"])
        try:
            challenge_list_str = user_properties.result["참여한 챌린지"]["rich_text"][0]["text"]["content"]
        except KeyError:
            return "참여한 챌린지가 없습니다.", 200

        challenge_list = challenge_list_str.split(",")
        data = [get_challenge_data(i) for i in challenge_list]
        return jsonify(data)
    else:
        return jsonify([get_challenge_data(what_kinda)])
    

@bp.route('/challenge/<what_kinda>', methods=['GET'])
def get_challenge(what_kinda):
    
    return render_template("challenge.html")
    
@bp.route('/make_challenge', methods=['GET', 'POST'])
def make_challenge():
    if request.method == "POST":
        properties = {
            "챌린지 제목" : request.form.get("title"),
            "챌린지 작성자" : session["page_id"],
            "챌린지 설명" : request.form.get("description"),
            "date" : f"{request.form.get("start_day")} ~ {request.form.get("end_day")}",
            "챌린지 아이콘" : request.form.get("img_url"),
        }

        challenge_db.create_database_page(properties)
        current_app.logger.info(f"사용자, {properties["챌린지 작성자"]} 가 새 챌린지{properties["챌린지 제목"]}를 만들었습니다.")
        return "제작중", 500
    return render_template("make_challenge.html")