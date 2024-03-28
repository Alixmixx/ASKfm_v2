import requests

url = "https://api.ask.fm:443/search"
params = {
    'fav_first': 'true',
    'limit': '25',
    'name': 'miaooo@mailinator.com',
    'offset': '0',
    'rt': '25',
    'ts': '1711520804'
}
headers = {
    'Authorization': 'HMAC 34da4895cb912e9200c84f47d91c2c239795ff43',
    'X-Client-Type': 'android_4.91.1',
    'Accept': 'application/json; charset=utf-8',
    'X-Forwarded-Proto': 'https',
    'Host': 'api.ask.fm:443',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Api-Version': '1.18',
    'X-Access-Token': '.3L7MzEEFQ-TKT_7UwbhOxzusUQX4G',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; Android SDK built for arm64 Build/OSM1.180201.044.D2)',
    'Connection': 'close'
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.text)