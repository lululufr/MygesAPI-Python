from myges import MyGesAPI
from datetime import datetime
from myges_to_notion import *
import os
import dotenv

import json

myges = MyGesAPI()
events = myges.get_next_events()
print(events)

#notion = NotionAPI()
#DATABASE_ID = os.getenv("DATABASE_ID")
#notion.import_myges_to_notion_calendar(DATABASE_ID, 30)
