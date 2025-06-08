from flask import Blueprint
from server.db import NotionDatabase
from dotenv import load_dotenv
import os

# 플라스크 기본 설정
bp = Blueprint('challenge', __name__)

# 데이터베이스 설정
load_dotenv()
daylist_db = NotionDatabase(os.getenv("CHALLENGE_DB_ID"))

@bp.route('/challenge/<what_kinda>', methods=['POST'])
def challenge(what_kinda):
    if what_kinda == "s":
        return "챌린지 기능은 아직 구현되지 않았습니다."
    else:
        return "챌린지 기능은 아직 구현되지 않았습니다."