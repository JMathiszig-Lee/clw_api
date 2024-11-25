import json
import os
from datetime import date, datetime, timedelta
from typing import Literal

import requests

clw_root = os.environ.get("CLW_ROOT", "rmh")
clw_pass = os.environ.get("CLW_PASS")
clw_user = os.environ.get("CLW_USER")


url = f"https://{clw_root}.clwrota.com"

# File to store access token
token_file = "access_token.json"



def authenticate(user, password):
    print(f"Authenticating with {user} and {password} at {url} ")
    auth_data = {"username": user, "password": password}
    headers = {
        "Accept": "application/json"
    }
    response = requests.post(f"{url}/publicapi/login/", data=auth_data, headers=headers)
    if response.status_code == 200:
        print("Authentication successful"
              )
        print(response.json())
        return response.json()["token"]
    else:
        print("Authentication failed:", response.text)
        return None


# Save access token to file
def save_access_token(token):
    with open(token_file, "w") as file:
        json.dump({"access_token": token, "time": datetime.now().isoformat() }, file)


# Load access token from file
def load_access_token():
    try:
        with open(token_file, "r") as file:
            data = json.load(file)
            if datetime.now() - datetime.fromisoformat(data["time"]) > timedelta(minutes=20):
                access_token = authenticate(clw_user, clw_pass)
                save_access_token(access_token)
                return access_token
            else:
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
    # headers = {
    #     "Accept": "application/json"
    # }
    response = requests.get(f"{url}/publicapi/{access_token}/people/list/")
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to get people:", response.text)
        return None
    
def get_groups(group_type: Literal['person', 'location']):
    access_token = refresh_access_token()
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(f"{url}/publicapi/{access_token}/groups/?group_type={group_type}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get groups:", response.text)
        return None

def get_person_rota(from_date: date, to_date: date, group_id: int = None):
    access_token = refresh_access_token()
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(
        f"{url}/publicapi/{access_token}/person_rota/?from_date={from_date}&to_date={to_date}", headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get rota:", response.text)
        return None