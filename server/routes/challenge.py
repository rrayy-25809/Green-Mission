from flask import Blueprint, jsonify, request, current_app, render_template, session
from notion_database.properties import Properties
from server.db import NotionDatabase
from dotenv import load_dotenv
import html
import os

# 플라스크 기본 설정
bp = Blueprint('challenge', __name__)

# 데이터베이스 설정
load_dotenv()
challenge_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))
user_db = NotionDatabase(os.getenv("USER_DB_ID"))

def get_author_name(author_id):
    try:
        author_page = user_db.get_page_properties(author_id[0]["text"]["content"])
        return author_page.result["유저명"]["title"][0]["text"]["content"]
    except IndexError:
        return "Green Mission"
    
def get_author_profile(author_id):
    try:
        author_page = user_db.get_page_properties(author_id[0]["text"]["content"])
        profile_url = author_page.result["프로필 사진"]["files"][0][author_page.result["프로필 사진"]["files"][0]["type"]]["url"] if author_page.result["프로필 사진"]["files"] else None
        return profile_url
    except IndexError:
        return "https://blog.kakaocdn.net/dna/bfZZQd/btrua3HciZ9/AAAAAAAAAAAAAAAAAAAAAFQMJkBr5W9Jsfmwj46M-CKXp7KDfMoYD6Bb7uc29T6x/%EC%B9%B4%ED%86%A1%20%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84%20%EC%82%AC%EC%A7%84(%EC%97%B0%EC%B4%88%EB%A1%9Dver).jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1753973999&allow_ip=&allow_referer=&signature=v0HPR0mRWcSXeBu1%2FU3iCJ1IeVo%3D&attach=1&knm=img.jpg"

def get_challenge_data(page_id):
    page = challenge_db.get_page_properties(page_id)

    try:
        end_date = page.result["참여기한"]["date"]["end"]
    except TypeError:
        end_date = "무기한"

    if page.result["현재 참여 인원"]["rich_text"]:
        user_list = page.result["현재 참여 인원"]["rich_text"][0]["text"]["content"].split(",")
        file_list = page.result["챌린지 파일 첨부"]["files"]
        join_uesr = [{
                "이름": user_db.get_page_properties(user).result["유저명"]["title"][0]["text"]["content"],
                "파일": file[file["type"]]["url"] if file else "None",
            } for user, file in zip(user_list, file_list)
        ]
    else :
        join_uesr = []

    return {
        "챌린지_ID": page_id,
        "챌린지_제목": page.result["챌린지 제목"]['title'][0]['text']['content'],
        "챌린지_작성자": get_author_name(page.result["챌린지 작성자"]["rich_text"]),
        "챌린지_작성자_프로필": get_author_profile(page.result["챌린지 작성자"]["rich_text"]),
        "챌린지_아이콘": page.result["챌린지 아이콘"]["files"][0][page.result["챌린지 아이콘"]["files"][0]["type"]]["url"],
        "챌린지_설명": html.escape(page.result["챌린지 설명"]["rich_text"][0]["text"]["content"]).replace('\n', '<br>'),
        "챌린지_응원수" : page.result["응원 수"]["number"],
        "챌린지_시작기한" : page.result["참여기한"]["date"]["start"] if page.result["참여기한"]["date"] else "무기한",
        "챌린지_종료기한" : end_date,
        "챌린지_작성일" : page.result["생성 일시"]["created_time"],
        "챌린지_참여자" : join_uesr,
        "챌린지_태그" : page.result["태그"]["rich_text"][0]["text"]["content"].split("\n") if page.result["태그"]["rich_text"] else [],
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
        except IndexError:
            return "참여한 챌린지가 없습니다.", 200

        challenge_list = challenge_list_str.split(",")
        data = [get_challenge_data(i) for i in challenge_list]
        return jsonify(data)
    else:
        return jsonify([get_challenge_data(what_kinda)])
    

@bp.route('/challenge/<what_kinda>', methods=['GET'])
def get_challenge(what_kinda):
    current_app.logger.info(f"챌린지 {what_kinda}에 접속")
    challenge = get_challenge_data(what_kinda)
    
    return render_template("challenge.html",**challenge)
    
@bp.route('/make_challenge', methods=['GET', 'POST'])
def make_challenge():
    if request.method == "POST":
        if request.form.get("tag") is None or not "," in request.form.get("tag"): # type: ignore
            current_app.logger.error(f"사용자, {session['page_id']} 가 챌린지를 제작하려고 했으나 태그가 없거나 쉼표로 구분되어 있지 않습니다.")
            return "챌린지 제작에 실패했습니다. 태그가 없거나 쉼표로 구분되어 있지 않습니다.", 400
        try:
            img = request.files.get("img")
            url = request.form.get('url')
            if img:
                path = os.path.join(current_app.instance_path, 'uploads', f'icon_{session["page_id"]}.jpg')
                img.save(path) # 비디오 저장(이미지로 할까 비디오로 할까)
            else:
                current_app.logger.error(f"사용자, {session['page_id']} 가 챌린지를 제작하려고 했으나 아이콘을 업로드하지 않았습니다.")
                return "챌린지 제작에 실패했습니다. 챌린지 아이콘이 없습니다.", 400
    
            properties = {
                "챌린지 제목" : request.form.get("title"),
                "챌린지 작성자" : session["page_id"],
                "챌린지 설명" : request.form.get("description"),
                "참여기한" : f"{request.form.get('start_day')} ~ {request.form.get('end_day')}",
                "챌린지 아이콘" : f"{url}/uploads/icon_{session['page_id']}.jpg",
                "태그" : request.form.get("tag").replace(",", "\n"), # type: ignore
                "응원 수" : 0,
            }

            challenge_db.create_database_page(properties)
            current_app.logger.info(f"사용자, {properties['챌린지 작성자']} 가 새 챌린지{properties['챌린지 제목']}를 만들었습니다.")
            return "제작완료", 200
        except ValueError:
            current_app.logger.error(f"사용자, {session['page_id']} 가 챌린지 제작에 실패했습니다. 필수 정보가 누락되었을 수 있습니다.")
            return "챌린지 제작에 실패했습니다. 필수 정보를 확인해주세요.", 400
        except Exception as e:
            current_app.logger.error(f"사용자, {session['page_id']} 가 챌린지 제작에 실패했습니다. 오류: {e}")
            return "챌린지 제작에 실패했습니다. 다시 시도해주세요.", 500
    else: #GET
        if "page_id" not in session:
            return "먼저 로그인 해주세요.", 403
        return render_template("make_challenge.html")

@bp.route('/join/<challenge_id>', methods=['POST']) # type: ignore
def join_challenge(challenge_id):
    user = user_db.get_page_properties(session["page_id"])
    challenge = challenge_db.get_page_properties(challenge_id)
    img = request.files.get("image")
    url = request.form.get('url')
    challenge_properties = Properties()
    user_properties = Properties()

    join_challenge_list = user.result["참여한 챌린지"]["rich_text"][0]["text"]["content"].split(",") if user.result["참여한 챌린지"]["rich_text"] else []
    join_user_list = challenge.result["현재 참여 인원"]["rich_text"][0]["text"]["content"].split(",") if challenge.result["현재 참여 인원"]["rich_text"] else []
    join_img_list = challenge.result["챌린지 파일 첨부"]["files"] if challenge.result["챌린지 파일 첨부"]["files"] else []

    if img:
        path = os.path.join(current_app.instance_path, 'uploads', f'{challenge_id}_{session["page_id"]}.jpg')
        img.save(path) # 비디오 저장(이미지로 할까 비디오로 할까)
    else:
        current_app.logger.error(f"사용자, {session['page_id']} 가 챌린지 {challenge_id}에 참여하려고 했으나 사진을 업로드하지 않았습니다.")
        return "챌린지 사진이 없습니다.", 400
    
    join_challenge_list.append(challenge_id)
    user_properties.set_rich_text("참여한 챌린지", ",".join(join_challenge_list))
    challenge_properties.set_rich_text("현재 참여 인원", ",".join(join_user_list + [session["page_id"]]))
    join_img_list.append({"type": "external", "name": f"{challenge_id}_{session['page_id']}.jpg", "external": {"url": f"{url}/uploads/{challenge_id}_{session['page_id']}.jpg"}})
    challenge_properties.result.update({"챌린지 파일 첨부": {"files": join_img_list}})

    challenge_db.update_database_properties(challenge_id, challenge_properties)
    user_db.update_database_properties(session["page_id"], user_properties)
    current_app.logger.info(f"사용자, {session['page_id']} 가 챌린지 {challenge_id}에 참여했습니다.")
    return "챌린지 참여 성공", 200

@bp.route('/cheer', methods=['POST'])
def cheer_challenge():
    challenge_id = request.form["challenge_id"]
    if "page_id" not in session:
        return "먼저 로그인 해주세요.", 403
    user = user_db.get_page_properties(session["page_id"])
    user_properties = Properties() # 업데이트 할 사용자 속성
    challenge_properties = Properties() # 업데이트 할 챌린지 속성
    
    try:
        cheer_list = user.result["응원한 챌린지"]["rich_text"][0]["text"]["content"].split(",")
    except IndexError:
        cheer_list = []

    if challenge_id not in cheer_list:
        cheer_list.append(challenge_id) # 응원한 챌린지 목록에 추가
        user_properties.set_rich_text("응원한 챌린지", ", ".join(cheer_list))

        cheer_count = challenge_db.get_page_properties(challenge_id).result["응원 수"]["number"]
        if cheer_count == None:
            cheer_count = 0
        challenge_properties.set_number("응원 수", cheer_count + 1) # 챌린지의 응원 수 증가

        challenge_db.update_database_properties(challenge_id, challenge_properties)
        user_db.update_database_properties(session["page_id"], user_properties) # 각 DB에 업데이트

        current_app.logger.info(f"사용자, {session['page_id']} 가 챌린지 {challenge_id}를 응원했습니다.")
        return "응원 성공", 200
    else:
        return "이미 응원한 챌린지입니다.", 400
