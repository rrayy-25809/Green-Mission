from db import NotionDatabase
from datetime import datetime
from notion_database.properties import Properties

challenge_db = NotionDatabase("20bdc33ef503801e9d94d96404fe33d7")

# # print(user_db.get_database_properties())

# properties = {
#     '챌린지 제목': '요즘 ado 들음',
#     '챌린지 작성자': '20adc33e-f503-8192-86a7-dee7b3c5bf93',
#     '챌린지 설명': '보컬 긁는 거 지림',
#     '참여기한': '2025-06-28 ~ 2025-07-28',
#     '챌린지 아이콘': 'https://i.scdn.co/image/ab67616d0000b273e204aafb5c393179c77c5253'
# }
# result = challenge_db.create_database_page(properties)
# print(result)

import json

# user_db = NotionDatabase("1f8dc33ef503801e81b0df64081aba0e")
user_list = challenge_db.get_page_ids()

with open("test.json", "w", encoding="utf-8") as f:
    json.dump(challenge_db.get_page_properties(user_list[0]).result, f, ensure_ascii=False, indent=4)

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

# properties = Properties()
# properties.set_files("프로필 사진",["https://i.pinimg.com/736x/d5/6d/18/d56d1893c7e9930886e4c3fbfe30eff6.jpg"])

# user_db.update_database_properties("20cdc33e-f503-81ea-bf68-c3289fba5dd0", properties)