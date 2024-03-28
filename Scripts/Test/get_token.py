import requests
import json

def get_access_token():
    # API endpoint
    url = "https://api.ask.fm/token"

    # Query parameters
    params = {
        'adid': '00000000-0000-0000-0000-000000000000',
        'did': 'CF2C2ED7-5994-55D1-B6EE-9F457A9B829D',
        'ts': '1708753024'
    }

    # Headers
    headers = {
        'Accept': '*/*',
        'X-Access-Token': '',  # Will be updated later
        'X-Api-Version': '1.18',
        'User-Agent': 'askfm/4535 CFNetwork/1492.0.1 Darwin/23.3.0',
        'X-Client-Type': 'ios_4.89.5',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'HMAC F3CC121A730D0A7D69DEECF9FB1816B446AA68B1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api.ask.fm'
    }

    # Sending GET request
    response = requests.get(url, headers=headers, params=params, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))

        # Return accessToken
        accessToken = data.get('accessToken')
        return accessToken
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        print(response.text)
        return None

# Usage
# token = get_access_token()
# if token:
#     print("Access Token:", token)
# else:
#     print("No token received or failed to retrieve data.")
