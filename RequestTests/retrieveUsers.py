import requests
import pprint
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8080"

token_response = requests.get(
    f"{BASE_URL}/api/auth/token",
    auth=HTTPBasicAuth("tester2022", "Tester@@4040"),
)
token = token_response.json().get("token")

response = requests.get(
    f"{BASE_URL}/api/users",
    headers={"Content-Type": "application/json", "Token": token},
)
pprint.pprint(response.json())
print(response.status_code)
