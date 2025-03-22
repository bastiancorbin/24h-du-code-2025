import requests

class ApiClient:
    def __init__(self):
        self.base_url = "https://app-584240518682.europe-west9.run.app/api"
        self.api_key = "85cwg64DcyTq9Uu7asCJ5Pzply87wXZo"

    def call_api(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"

        headers = {}

        if self.api_key:
            headers["Authorization"] = f"Token {self.api_key}"

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        return response.json()