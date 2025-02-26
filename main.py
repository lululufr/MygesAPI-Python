from mygesapi import MyGesAPI

import json

api = MyGesAPI()
profile = api.get_profile()

print(profile)
print(api.get_classes(2024)["result"][0]["puid"])
