from flask import Blueprint, redirect, render_template, session, current_app
from server.db import NotionDatabase
from dotenv import load_dotenv
from datetime import datetime
import os

# 플라스크 기본 설정
bp = Blueprint('today', __name__)

# 데이터베이스 설정
load_dotenv()
daylist_db = NotionDatabase(os.getenv("DAYLIST_DB_ID"))

@bp.route('/today', methods=['POST'])
def today():
    for i in daylist_db.get_page_ids():
        page = daylist_db.get_page_properties(i)
        # page.result["날짜"]["date"]["start"] 값이 "2025-05-28" 같은 문자열이라고 가정
        anniversary_date = page.result["날짜"]["date"]["start"]["start"]
        # If anniversary_date_value is a dict, extract the 'start' key; otherwise, use as is
        anniversary_date = datetime.strptime(anniversary_date, "%Y-%m-%d").date()
        today_date = datetime.now().date()

        if anniversary_date == today_date:
            current_app.logger.info("오늘의 기념일이 있습니다.")
            return page.result["기념일 명"]["title"][0]["text"]["content"]
        
    current_app.logger.info("오늘의 기념일이 없습니다.")
    return "오늘의 기념일이 없습니다."