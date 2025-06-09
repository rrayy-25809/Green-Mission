from flask import Blueprint, jsonify, request, current_app, render_template
from server.db import NotionDatabase
from dotenv import load_dotenv
import os

# 플라스크 기본 설정
bp = Blueprint('challenge', __name__)

# 데이터베이스 설정
load_dotenv()
# challenge_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))
challenge_db = NotionDatabase("20bdc33ef503801e9d94d96404fe33d7")
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

@bp.route('/challenge/<what_kinda>', methods=['POST'])
def challenge(what_kinda):
    if what_kinda == "s":
        data = []
        for i in challenge_db.get_page_ids():
            page = challenge_db.get_page_properties(i)

            try:
                author_id = user_db.get_page_properties(page.result["챌린지 작성자"]["rich_text"][0]["text"]["content"])
                author = author_id.result["유저명"]["title"][0]["text"]["content"]
            except:
                author = "Green Mission"
                
            challenge = {
                "챌린지 ID" : i,
                "챌린지 제목": page.result["챌린지 제목"]['title'][0]['text']['content'],
                "챌린지 작성자" : author,
                "챌린지 아이콘" : page.result["챌린지 아이콘"]["files"][0]["external"]["url"],
                "챌린지 설명" : page.result["챌린지 설명"]["rich_text"][0]["text"]["content"],
            }
            data.append(challenge)

        return jsonify(data)
    else:
        return [{ # 테스트용 더미 데이터
                "챌린지 ID" : "11111234",
                "챌린지 제목": "page.result[]['title'][0]['text']['content']",
                "챌린지 작성자" : "author",
                "챌린지 아이콘" : "awef",
                "챌린지 설명" : "awfe",
            }]
    
@bp.route('/make_challenge', methods=['GET', 'POST'])
def make_challenge():
    if request.method == "POST":
        current_app.logger.info("챌린지 만드는 중")
        return "제작중", 500
    return render_template("make_challenge.html")