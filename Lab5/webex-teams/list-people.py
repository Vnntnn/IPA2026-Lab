import requests
import json

access_token = 'NTY3YTg1ZTgtMmFkMi00NThmLTgyZjUtMjJiMzczYmY2OTFkOGVmMDk3OGUtMWU0_PS65_ef92af4f-1d50-4c94-ab19-69f00bce0a28'
url = 'https://webexapis.com/v1/people'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {
    'email': 'thanabodee.nine@gmail.com'
}

peoples = requests.get(url, headers=headers, params=params)
# print(json.dumps(peoples.json(), indent=4))

# Get personal detail with admin
person_id = f'{peoples.json()["items"][0]["id"]}'
url = 'https://webexapis.com/v1/people/{}'.format(person_id)

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=4))
