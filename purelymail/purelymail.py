import requests

from dataclasses import asdict
from .models import User, RoutingRule, PurelymailAPIError


class PurelymailAPI:
    def __init__(self, api_token: str, version="v0"):

        self.base_url = f"https://purelymail.com/api/{version}"
        self.headers = {
            "accept": "application/json",
            "Purelymail-Api-Token": api_token,
            "Content-Type": "application/json"
        }

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle the API response, raise an exception if not successful."""
        if response.status_code != 200:
            raise PurelymailAPIError(f"API request failed with status code {
                                     response.status_code}: {response.text}")

        response_data = response.json()

        # Ensure that the response type matches
        if response_data.get("type") == "error":
            print(response_data)
            raise PurelymailAPIError(f"API returned an error: {
                                     response_data.get('message', 'Unknown error')}")  # noqa: E501
        return response_data['result'] if response_data.get('result') else response_data  # noqa: E501

    def create_user(self, user: User):
        """Create a new user."""
        url = f"{self.base_url}/createUser"
        response = requests.post(url, headers=self.headers, json=asdict(user))
        self._handle_response(response)

    def delete_user(self, username: str):
        """Delete a user."""
        url = f"{self.base_url}/deleteUser"
        response = requests.post(url, headers=self.headers, json={
            "userName": username
        })
        self._handle_response(response)

    def list_users(self):
        """List all users under the account."""
        url = f"{self.base_url}/listUser"
        response = requests.post(url, headers=self.headers, json={})
        data = self._handle_response(response)
        return data['users']

    def list_routing_rules(self) -> list[RoutingRule]:
        """List all routing rules under the account."""
        url = f"{self.base_url}/listRoutingRules"
        response = requests.post(url, headers=self.headers, json={})
        data = self._handle_response(response)
        return [RoutingRule(**item) for item in data['rules']]

    def check_account_credit(self) -> float:
        """Get the current account credit."""
        url = f"{self.base_url}/checkAccountCredit"
        response = requests.post(url, headers=self.headers, json={})
        data = self._handle_response(response)
        # TODO: fix long floating points returned from api
        # like '9.01254597919837645865043125317098'
        return float(data['credit'])
