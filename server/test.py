from db import NotionDatabase
from datetime import datetime
from notion_database.properties import Properties

user_db = NotionDatabase("1f8dc33ef503801e81b0df64081aba0e")

# print(user_db.get_database_properties())

# properties = {
#     '유저명' : "VELOG",
#     '이메일' : "VELOGisGODforCODE@gmail.com",
#     '비밀번호' : "VELOGisGODforCODE",
#     '가입일' : datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '+0900',
#     '사용자 역할' : "관리자",
#     '전화번호' : "010-1234-5678"
# }
# result = user_db.create_database_page(properties)
# print(result)

# import json

# user_list = user_db.get_page_ids()

# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(user_db.get_page_properties(user_list[0]).result, f, ensure_ascii=False, indent=4)

# page = user_db.get_page_properties(user_list[0])
# today = datetime.now().strftime("%Y-%m-%d") + '+0900'
# # page.result["날짜"]["date"]["start"] 값이 "2025-05-28" 같은 문자열이라고 가정
# anniversary_date = page.result["날짜"]["date"]["start"]["start"]
# # If anniversary_date_value is a dict, extract the 'start' key; otherwise, use as is
# anniversary_date = datetime.strptime(anniversary_date, "%Y-%m-%d").date()
# today_date = datetime.now().date()

# if anniversary_date == today_date:
#     print("오늘의 기념일이 있습니다.")

# print(user_db.get_page_properties(user_list[1]))


properties = Properties()
properties.set_files("프로필 사진",["https://i.pinimg.com/736x/d5/6d/18/d56d1893c7e9930886e4c3fbfe30eff6.jpg"])

user_db.update_database_properties("20cdc33e-f503-81ea-bf68-c3289fba5dd0", properties)