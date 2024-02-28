import requests
import os
import json

clw_root = os.environ.get("CLW_ROOT", "rmh")
clw_pass = os.environ.get("CLW_PASS")
clw_user = os.environ.get("CLW_USER")


url = f"https://{clw_root}.clwrota.com"

# File to store access token
token_file = "access_token.json"

def authenticate(user, password):
    auth_data = {
        "username": user,
        "password": password
    }
    response = requests.post(url + "/publicapi/login/", json=auth_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Authentication failed:", response.text)
        return None
    

# Save access token to file
def save_access_token(token):
    with open(token_file, 'w') as file:
        json.dump({"access_token": token}, file)

# Load access token from file
def load_access_token():
    try:
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data["access_token"]
    except FileNotFoundError:
        return None

# Refresh access token if needed
def refresh_access_token():
    access_token = load_access_token()
    if not access_token:
        print("No access token found, authenticating...")
        access_token = authenticate(clw_user, clw_pass)
        save_access_token(access_token)
    return access_token

# https://ex.clwrota.com/publicapi/<token>/people/list/ 

def get_people():
    access_token = refresh_access_token()
    headers = {
        "Accept": "application/json" 
    }
    response = requests.get(f"{url}/publicapi/{access_token}/people/list/", headers=headers)
    if response.status_code == 200:
        print(response.text)
        return response.json()
    else:
        print("Failed to get people:", response.text)
        return None