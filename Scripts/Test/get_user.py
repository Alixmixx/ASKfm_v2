import requests
import json
from get_token import get_access_token

def get_user():
    # API endpoint
    url = "https://api.ask.fm/search"

    # Query parameters
    params = {
        'bio': 'miaooo',
        'limit': '25',
        'name': 'miaooo',
        'offset': '0',
        'rt': '29',
        'ts': 1709016214
    }

    # Headers
    headers = {
        'Accept': '*/*',
        'X-Access-Token': '',  # Update as needed
        'X-Api-Version': '1.18',
        'User-Agent': 'askfm/4535 CFNetwork/1492.0.1 Darwin/23.3.0',
        'X-Client-Type': 'ios_4.89.5',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'HMAC FAC9BF579D474290AF2C67F6732688B805FD1897',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api.ask.fm'
    }

    # Sending GET request
    headers.update({'X-Access-Token': get_access_token()})
    #print("Header:", json.dumps(headers, indent=4))

    response = requests.get(url, headers=headers, params=params, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        print(response.text)
        return None

# Usage
user = get_user()
if user:
    print("User found:", user)
else:
    print("No user found or failed to retrieve data.")
