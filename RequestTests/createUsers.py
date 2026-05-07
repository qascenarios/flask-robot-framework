import requests
import pprint
import json
from pathlib import Path
from datetime import datetime
from random import randint

BASE_URL = "http://127.0.0.1:8080"
LATEST_USERS_FILE = Path(__file__).with_name(".latest_users.json")


def unique_username(prefix):
    suffix = datetime.now().strftime("%Y%m%d%H%M%S") + str(randint(100, 999))
    return f"{prefix}_{suffix}"


data = [
    {
        "username": unique_username("foden"),
        "password": "Tester@@4040",
        "firstname": "Folly",
        "lastname": "Fella",
        "phone": "000000000",
    },
    {
        "username": unique_username("goodies"),
        "password": "Tester@@4040",
        "firstname": "Plaza",
        "lastname": "Sun",
        "phone": "000000000",
    },
    {
        "username": unique_username("jandon"),
        "password": "Tester@@4040",
        "firstname": "Victor",
        "lastname": "Malu",
        "phone": "000000000",
    },
]

for x in data:
    response = requests.post(
        f"{BASE_URL}/api/users", json=x, headers={"Content-Type": "application/json"}
    )
    print(response.headers)
    pprint.pprint(response.json())
    statusCode = response.status_code
    print(statusCode)

LATEST_USERS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Saved latest users to: {LATEST_USERS_FILE}")
