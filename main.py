from myges import MyGesAPI
from datetime import datetime
from myges_to_notion import *
import os
import dotenv

import json

myges = MyGesAPI()
events = myges.get_next_events(30)
print(events["result"][1])

notion = NotionAPI()

DATABASE_ID = os.getenv("DATABASE_ID")


# res = notion.get_events_database(DATABASE_ID)

for event in events["result"]:
    notion.create_event(DATABASE_ID, event)
    print("Event created")

# print(json.dumps(res, indent=4))
