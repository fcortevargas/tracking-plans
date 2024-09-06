import requests
import json
from app.config import settings


class NotionService:
    def __init__(self):
        self.api_key = settings.notion_api_token
        self.parent_page_id = settings.notion_parent_page_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_event_properties_database(self):
        """Create a Notion database to store event properties."""
        url = "https://api.notion.com/v1/databases"
        headers = self.headers

        payload = {
            "parent": {"page_id": self.parent_page_id},
            "title": [{"text": {"content": "Event Properties"}}],
            "properties": {
                "Name": {"title": {}},
                "Type": {
                    "select": {
                        "options": [
                            {"name": "string", "color": "blue"},
                            {"name": "number", "color": "green"},
                            {"name": "boolean", "color": "yellow"},
                            {"name": "array", "color": "red"},
                            {"name": "object", "color": "purple"},
                        ]
                    }
                },
                "Description": {"rich_text": {}},
            },
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()

    def create_tracking_plan_database(self, title: str) -> dict:
        """Create a new tracking plan database with multi-select for properties."""
        url = "https://api.notion.com/v1/databases"
        headers = self.headers
        payload = {
            "parent": {"type": "page_id", "page_id": self.parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": {
                "Event Name": {"title": {}},
                "Event Description": {"rich_text": {}},
                "Properties": {
                    "multi_select": {
                        "options": []  # Add property options dynamically later
                    }
                },
            },
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def archive_database(self, database_id: str) -> dict:
        """Archive an existing Notion database."""
        url = f"https://api.notion.com/v1/databases/{database_id}"
        payload = {"archived": True}
        response = requests.patch(url, headers=self.headers, data=json.dumps(payload))
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def add_property_to_event_properties_database(
        self,
        database_id: str,
        property_id: str,
        name: str,
        description: str,
        prop_type: str,
    ) -> dict:
        """Add an event property to the Event Properties Notion database."""
        url = "https://api.notion.com/v1/pages"
        headers = self.headers

        if not description:
            description = ""

        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "Type": {"select": {"name": prop_type}},
                "Description": {"rich_text": [{"text": {"content": description}}]},
            },
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()

    def add_event_to_tracking_plan_database(
        self,
        database_id: str,
        event_name: str,
        event_description: str,
        multiselect_options: list,
    ) -> dict:
        """Add an event to the Notion database with multi-select options."""
        url = f"https://api.notion.com/v1/pages"
        headers = self.headers

        if not event_description:
            event_description = ""

        # Structure the payload for the Notion API
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Event Name": {"title": [{"text": {"content": event_name}}]},
                "Properties": {"multi_select": multiselect_options},
                "Event Description": {
                    "rich_text": [{"text": {"content": event_description}}]
                },
            },
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()
