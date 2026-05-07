import requests
import pprint
import json
from pathlib import Path
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8080"
LATEST_USERS_FILE = Path(__file__).with_name(".latest_users.json")

target_username = "tester2022"
if LATEST_USERS_FILE.exists():
    latest_users = json.loads(LATEST_USERS_FILE.read_text(encoding="utf-8"))
    if latest_users:
        target_username = latest_users[0]["username"]

response = requests.get(
    f"{BASE_URL}/api/auth/token", auth=HTTPBasicAuth(target_username, "Tester@@4040")
)
token = response.json().get("token")
pprint.pprint(token)
