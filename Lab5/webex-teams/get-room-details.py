import requests
import json
import importlib

# load module from list rooms for room id
list_rooms_module = importlib.import_module("list-rooms")
list_rooms = list_rooms_module.list_rooms

access_token = 'NTY3YTg1ZTgtMmFkMi00NThmLTgyZjUtMjJiMzczYmY2OTFkOGVmMDk3OGUtMWU0_PS65_ef92af4f-1d50-4c94-ab19-69f00bce0a28'
room_id = list_rooms()["items"][0]["id"] # Get room that create from script (it's the first room)
url = 'https://webexapis.com/v1/rooms/{}/meetingInfo'.format(room_id)

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent = 4))
