from mygesapi import MyGesAPI

import json

api = MyGesAPI()
profile = api.get_profile()

print(profile)
