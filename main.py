from myges import MyGesAPI
from datetime import datetime


import json

api = MyGesAPI()
profile = api.get_profile()

print(profile)
