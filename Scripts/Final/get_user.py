import time
import json
import x_access_token

def put_user():
    url = "https://api.ask.fm:443/open"
    headers = {
        'Authorization': 'HMAC 47ac4765725f08375cd583daf2f9b6b5085b6e97',
        'X-Client-Type': 'android_4.91.1',
        'Accept': 'application/json; charset=utf-8',
        'X-Forwarded-Proto': 'https',
        'Host': 'api.ask.fm:443',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Api-Version': '1.18',
        'X-Access-Token': '.5psGLHDuksXYAA7KzPV_zbCyhHWk',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; Android SDK built for arm64 Build/OSM1.180201.044.D2)',
        'Connection': 'close'
    }

    # Data for the request
    data = {
        'json': '{"adid":"","connType":"wifi","deviceModel":"unknown Android SDK built for arm64","did":"3049e49e18cfdcb8","os_version":"Android 8.1.0","rt":"2","ts":"1711522315"}'
    }

    response = requests.put(url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)


def get_user(username):
    # API endpoint
    url = "https://api.ask.fm/search"

    # Query parameters
    method = "GET"
    host = "api.ask.fm:443"
    path = "/search"
    timestamp = str(int(time.time()))
    params = {
        'fav_first': 'true',
        'limit': '25',
        'name': username,
        'offset': '0',
        'rt': '2',
        'ts': timestamp
    }

    # Headers
    headers = {
        "Authorization": "",
        "X-Client-Type": "android_4.91.1",
        "Accept": "application/json; charset=utf-8",
        "X-Forwarded-Proto": "https",
        "Host": "api.ask.fm:443",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Api-Version": "1.18",
        "X-Access-Token": '.3L7MzEEFQ-TKT_7UwbhOxzusUQX4G',
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Android SDK built for arm64 Build/OSM1.180201.044.D2)",
        "Connection": "close"
    }

    # Sending GET request
    headers.update({'X-Access-Token': x_access_token.get_access_token()})
    #print("Header:", json.dumps(headers, indent=4))

    response = x_access_token.sendRequest(method, host, path, params, headers)

    # Check if the request was successful
    print("Response:", response)

# Usage
user = get_user(username="miaooo@mailinator.com")
