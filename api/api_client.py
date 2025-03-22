import requests

class ApiClient:
    def __init__(self):
        self.base_url = "https://app-584240518682.europe-west9.run.app/api"
        self.headers = {"Authorization": "Token 85cwg64DcyTq9Uu7asCJ5Pzply87wXZo"}

    def _request(self, method, endpoint, params=None, json=None):
        url = f"{self.base_url}/{endpoint}"

        response = requests.request(method, url, headers=self.headers, params=params, json=json)

        if method == "DELETE" and response.status_code == 204:
            return {"message": "Resource deleted successfully"}

        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None, json=None):
        return self._request("GET", endpoint, params, json)

    def post(self, endpoint, params=None, json=None):
        return self._request("POST", endpoint, params, json)

    def put(self, endpoint, params=None, json=None):
        return self._request("PUT", endpoint, params, json)

    def patch(self, endpoint, params=None, json=None):
        return self._request("PATCH", endpoint, params, json)

    def delete(self, endpoint, params=None, json=None):
        return self._request("DELETE", endpoint, params, json)