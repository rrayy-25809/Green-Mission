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

@bp.route('/challenge/<what_kinda>', methods=['POST'])
def challenge(what_kinda):
    if what_kinda == "s": # 챌린지 목록 조회(기본 페이지)
        data = []
        for i in challenge_db.get_page_ids():
            page = challenge_db.get_page_properties(i)

            try:
                author_id = user_db.get_page_properties(page.result["챌린지 작성자"]["rich_text"][0]["text"]["content"])
                author = author_id.result["유저명"]["title"][0]["text"]["content"]
            except KeyError:
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
    elif what_kinda == "user": # 유저가 참여한 챌린지 목록(현 페이지가 마이페이지일 때)
        user_properties = user_db.get_page_properties(session["page_id"])
        try:
            challenge_list_str:str = user_properties.result["참여한 챌린지"]["rich_text"][0]["text"]["content"] # 챌린지 리스트를 문자열로 저장 (id1,id2)(괄호는 그냥 한거임 대괄호 없음)
        except KeyError:
            return "참여한 챌린지가 없습니다.", 200
        
        challenge_list:list[str] = challenge_list_str.split(",")
        data = []

        for i in challenge_list:
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
    else: # 페이지가 /challenge일 때
        page = challenge_db.get_page_properties(what_kinda)

        try:
            author_id = user_db.get_page_properties(page.result["챌린지 작성자"]["rich_text"][0]["text"]["content"])
            author = author_id.result["유저명"]["title"][0]["text"]["content"]
        except:
            author = "Green Mission"
        
        return [{
            "챌린지 ID" : what_kinda,
            "챌린지 제목": page.result["챌린지 제목"]['title'][0]['text']['content'],
            "챌린지 작성자" : author,
            "챌린지 아이콘" : page.result["챌린지 아이콘"]["files"][0]["external"]["url"],
            "챌린지 설명" : page.result["챌린지 설명"]["rich_text"][0]["text"]["content"],
        }]
    
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