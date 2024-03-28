import generate_hash
import argparse
import requests
import hashlib
import random
import string
import json
import time

def sendRequest(method, host, path, params, headers):
    hmac = generate_hash.generate_hmac(method, host, path, params)
    headers['Authorization'] = hmac
    print('Full request:', method, host, path, params, headers, sep='\n')
    if method == "GET":
        res = requests.get("https://api.ask.fm:443" + path,
                        headers=headers,
                        params=params,
)
    elif method == "PUT":
        res = requests.put("https://api.ask.fm:443" + path,
                        headers=headers,
                        data=params,
)
    elif method == "POST":
        res = requests.post("https://api.ask.fm:443" + path,
                        headers=headers,
                        data=params,
)
    #params.rt += 1
    return json.loads(res.text)

def generate_random_md5():
    # Generate a random string
    characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(characters, k=20))

    md5_hash = hashlib.md5(random_str.encode()).hexdigest()

    return random_str


def init(username):
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

    access_token = get_access_token(headers)
    headers["X-Access-Token"] = access_token

   # Open session
    open_ses = open_session(headers)
    print(json.dumps(open_ses, indent=4, sort_keys=True))

    # Register User
    register_user = post_user(username, headers)
    print(json.dumps(register_user, indent=4, sort_keys=True))

    # Get the token from last response
    headers["X-Access-Token"] = register_user['at']

    # Get user
    user = get_user(username, headers)
    print(json.dumps(user, indent=4, sort_keys=True))


def open_session(headers):
    url = "https://api.ask.fm:443/open"
    method = "PUT"
    host = "api.ask.fm:443"
    path = "/open"
    params = {
        'json': '{"adid":"","connType":"wifi","deviceModel":"unknown Android SDK built for arm64","did":"3049e49e18cfdcb8","os_version":"Android 8.1.0","rt":"2","ts":"1711522315"}'
    }

    response = sendRequest(method, host, path, params, headers)
    return response

def get_user(username, headers):
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

    response = sendRequest(method, host, path, params, headers)
    return response

def post_user(usename, headers):
    url = "https://api.ask.fm:443/register"

    new_login = generate_random_md5()
    #new_login = "miaoooo12ggf243"

    # Query parameters
    method = "POST"
    host = "api.ask.fm:443"
    path = "/register"
    timestamp = str(int(time.time()))
    params = {
        'json': '{{"adid":"","did":"3049e49e18cfdcb8","gmt_offset":"540","guid":"3049e49e18cfdcb8","pass":"vVUie35u4n","rt":"3","short_reg":"true","source":"email","ts":"{timestamp}","uid":"{uid}","user":{{"assumedBirthday":true,"avatarUrl":null,"birthDate":"27.03.2011","consents":[{{"data":{{}},"enabled":false,"name":"termsOfUse","required":true,"value":false}},{{"data":{{}},"enabled":false,"name":"privacyPolicy","required":true,"value":false}},{{"data":{{"age":"16"}},"enabled":false,"name":"parentConsent","required":false,"value":false}},{{"data":{{}},"enabled":false,"name":"adsConsent","required":false,"value":false}},{{"data":{{}},"enabled":false,"name":"thirdPartiesConsent","required":false,"value":false}},{{"data":{{}},"enabled":true,"name":"nonEUConsent","required":true,"value":true}}],"email":"{email}","fullName":"{fullName}","genderId":0,"lang":"en","shortReg":true,"themeId":4,"uid":"{uid}"}}}}'
                .format(timestamp=timestamp, uid=new_login, email=new_login + "@anonym.com", fullName=new_login)
    }

    response = sendRequest(method, host, path, params, headers)
    return response

def get_access_token(headers):
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
        'ts': timestamp
    }

    # Sending GET request
    response = sendRequest(method, host, path, params, headers)
    print(response)
    return response['accessToken']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run AskFM')
    parser.add_argument('email', type=str, help='email to search for')

    args = parser.parse_args()

    init(args.email)