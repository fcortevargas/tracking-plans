import requests
from app.config import settings


class RudderStackService:
    def __init__(self):
        self.api_token = settings.rudderstack_api_token
        self.base_url = settings.rudderstack_base_url

    def get_all_tracking_plans(self) -> dict:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{self.base_url}/catalog/tracking-plans"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_tracking_plan(self, tracking_plan_id: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{self.base_url}/catalog/tracking-plans/{tracking_plan_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_all_tracking_plan_events(self, tracking_plan_id: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{self.base_url}/catalog/tracking-plans/{tracking_plan_id}/events"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_tracking_plan_event(self, tracking_plan_id: str, event_id: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{self.base_url}/catalog/tracking-plans/{tracking_plan_id}/events/{event_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
