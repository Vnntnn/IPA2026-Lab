import requests
import json

access_token = 'NTY3YTg1ZTgtMmFkMi00NThmLTgyZjUtMjJiMzczYmY2OTFkOGVmMDk3OGUtMWU0_PS65_ef92af4f-1d50-4c94-ab19-69f00bce0a28'
url = 'https://webexapis.com/v1/people/me'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=4))
