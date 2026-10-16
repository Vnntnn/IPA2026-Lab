import requests
import json

access_token = 'NTY3YTg1ZTgtMmFkMi00NThmLTgyZjUtMjJiMzczYmY2OTFkOGVmMDk3OGUtMWU0_PS65_ef92af4f-1d50-4c94-ab19-69f00bce0a28'
url = 'https://webexapis.com/v1/rooms'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

params={'title': 'DevNet Associate Training!'}
res = requests.post(url, headers=headers, json=params)

print(json.dumps(res.json(), indent = 4))
