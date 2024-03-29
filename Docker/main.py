from flask import Flask, request, jsonify
import generate_hash
import requests
import hashlib
import random
import string
import time

app = Flask(__name__)

# When the client sends a POST request to the /run endpoint, the server will run the script with the provided email.
@app.route('/run', methods=['POST'])
def run_script():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
    
    email = data['email']
    try:
        result = init(email)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Send a request to the Ask.fm API
def sendRequest(method, host, path, params, headers):
    hmac = generate_hash.generate_hmac(method, host, path, params)
    headers['Authorization'] = hmac
    #print('Full request:', method, host, path, params, headers, sep='\n')

    try:
        if method == "GET":
            res = requests.get("https://api.ask.fm:443" + path, headers=headers, params=params)
        elif method == "PUT":
            res = requests.put("https://api.ask.fm:443" + path, headers=headers, data=params)
        elif method == "POST":
            res = requests.post("https://api.ask.fm:443" + path, headers=headers, data=params)

        # Check if the response is not successful
        if res.status_code != 200:
            print("Error: Received response with status code:", res.status_code)
            return {"error": f"Received response with status code: {res.status_code}", "details": res.json()}

        return res.json()
    
    except requests.RequestException as e:
        print("RequestException:", str(e))
        return {"error": str(e)}

def generate_random_md5():
    # Generate a random string
    characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(characters, k=20))

    # Generate an MD5 hash of the random string
    # But it seems hash is detected by the server so random string is used
    md5_hash = hashlib.md5(random_str.encode()).hexdigest()

    return random_str


def init(email):
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

    # Open session with the server
    open_ses = open_session(headers)
    if 'error' in open_ses:
        return open_ses

    # Register User to the server, creating account
    register_user = post_user(email, headers)
    if 'error' in register_user:
        return register_user

    # Get the token from last response
    headers["X-Access-Token"] = register_user['at']

    # Make the email request
    user = get_user(email, headers)
    if 'error' in user:
        return user

    return {"user": user}


# API functions
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
   
    method = "GET"
    host = "api.ask.fm:443"
    path = "/token"
    params = {
        'adid': '',
        'did': '3049e49e18cfdcb8',
        'rt': '1',
        'ts': timestamp
    }

    response = sendRequest(method, host, path, params, headers)
    print(response)
    return response['accessToken']

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)