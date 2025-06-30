from notion_database.page import Page
from notion_database.properties import Properties
from notion_database.database import Database
from dotenv import load_dotenv
from datetime import datetime
import os

# 참고한 링크: https://velog.io/@newnew_daddy/PYTHON10#-2-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%EC%83%9D%EC%84%B1

load_dotenv()
NOTION_API_KEY:str = os.getenv("NOTION_API_KEY") # type: ignore

class NotionDatabase:
    def __init__(self, DATABASE_ID):
        self.DATABASE_ID = DATABASE_ID

    def _dict_to_properties(self, properties_dict: dict) -> Properties:
        PROPERTY = Properties()
        PROPERTY.result = properties_dict

        return PROPERTY

    def get_database_properties(self):
        D = Database(NOTION_API_KEY)
        D.retrieve_database(self.DATABASE_ID)
        return D.result

    def create_database_page(self, properties: dict | Properties):
        if type(properties) is dict:
            PROPERTY = Properties()
    
            res = self.get_database_properties()
            
            for k, v in res['properties'].items():
                property_type = v['type']
                if k in properties:
                    if property_type == "date":
                        if "~" in properties[k]:
                            date = properties[k].split(" ~ ")
                            PROPERTY.set_date(k, date[0], date[1])
                            continue
                        else:
                            PROPERTY.set_date(k, start=properties[k])
                            continue
                    elif property_type == "files":
                        PROPERTY.set_files(k, [f"{properties[k]}",])  # 파일 URL을 리스트로 감싸서 전달
                        continue
                    getattr(PROPERTY, f'set_{property_type}')(k, properties[k])
        else:
            PROPERTY:Properties = properties # type: ignore
            
        P = Page(NOTION_API_KEY)
        P.create_page(database_id=self.DATABASE_ID, properties=PROPERTY)
        return P.result
    
    def get_page_ids(self):
        D = Database(NOTION_API_KEY)
        D.find_all_page(self.DATABASE_ID)

        result = []
        for page in D.result['results']:
            result.append(page['id'])   # 페이지 ID만 추출
        
        return result
    
    def delete_page(self, page_id):
        P = Page(NOTION_API_KEY)
        P.archive_page(page_id=page_id, archived=True)
        return P.result
    
    def get_page_properties(self, page_id:str) -> Properties:
        P = Page(NOTION_API_KEY)
        P.retrieve_page(page_id=page_id)
        # return P.result
        properties_dict = P.result["properties"]
        return self._dict_to_properties(properties_dict)
        
    def update_database_properties(self, page_id:str, properties: Properties):
        P = Page(NOTION_API_KEY)
        
        P.update_page(page_id=page_id, properties=properties)
        return P.result