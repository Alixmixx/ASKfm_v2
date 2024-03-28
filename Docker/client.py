import requests
import json

def send_email_request(email):
    url = "http://localhost:5001/run"
    headers = {"Content-Type": "application/json"}
    data = {"email": email}

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    while True:
        email = input("Enter email (or type 'exit' to quit): ")
        if email.lower() == 'exit':
            break
        try:
            response = send_email_request(email)
            format_response = json.dumps(response, indent=4, sort_keys=True)
            print("Response:\n", format_response)        
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
