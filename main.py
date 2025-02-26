from myges import MyGesAPI

import json

api = MyGesAPI()
profile = api.get_profile()

events = api.get_next_events()

print(profile)
print("===")
print(events)
