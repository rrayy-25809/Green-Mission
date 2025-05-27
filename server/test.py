from db import NotionDatabase
from datetime import datetime

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
# user_list = user_db.get_pages_id()
# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(user_db.get_page_properties(user_list[1]).result, f, ensure_ascii=False, indent=4)

# print(user_db.get_page_properties(user_list[1]))
