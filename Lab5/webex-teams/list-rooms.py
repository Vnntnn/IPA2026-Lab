import requests
import json

def list_rooms():
    access_token = 'NTY3YTg1ZTgtMmFkMi00NThmLTgyZjUtMjJiMzczYmY2OTFkOGVmMDk3OGUtMWU0_PS65_ef92af4f-1d50-4c94-ab19-69f00bce0a28'
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    params={'max': '100'}
    res = requests.get(url, headers=headers, params=params)
    
    return res.json()

# print(json.dumps(list_rooms(), indent = 4))
