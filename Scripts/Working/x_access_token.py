import time
import requests
import json
import generate_hash

def sendRequest(method, host, path, params, headers):
    hmac = generate_hash.generate_hmac(method, host, path, params)
    headers['Authorization'] = hmac
    res = requests.session().get("https://api.ask.fm:443" + path,
                        headers=headers,
                        params=params,
)
    #params.rt += 1
    print(headers)
    return json.loads(res.text)

def get_access_token():
    url = "https://api.ask.fm/token"

    timestamp = str(int(time.time()))
    # Query parameters
    method = "GET"
    host = "api.ask.fm:443"
    path = "/token"
    params = {
        'adid': '',
        'did': '3049e49e18cfdcb8',
        'rt': '1',
        'ts': '1711519981'
    }

    # Get timestamp
    #print(params['ts'])

    # Headers
    headers = {
        "Authorization": "",
        "X-Client-Type": "android_4.91.1",
        "Accept": "application/json; charset=utf-8",
        "X-Forwarded-Proto": "https",
        "Host": "api.ask.fm:443",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Api-Version": "1.18",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Android SDK built for arm64 Build/OSM1.180201.044.D2)",
        "Connection": "close"
    }

    # Sending GET request
    response = sendRequest(method, host, path, params, headers)
    print(response)

get_access_token()