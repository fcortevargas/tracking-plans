import os
import requests
import json
from app.config import settings


class NotionService:
    def __init__(self, cache_file="cache/properties.json"):
        self.api_key = settings.notion_api_token
        self.parent_page_id = settings.notion_parent_page_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.cache_file = cache_file
        self.properties = self.load_cache()

    def load_cache(self) -> dict:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self) -> None:
        with open(self.cache_file, "w") as f:
            json.dump(self.properties, f, indent=4)

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

    def create_tracking_plan_database(
        self,
        title: str,
        event_properties_db_id: str,
    ) -> dict:
        """Create a new tracking plan database with a relation to the Event Properties database."""
        url = "https://api.notion.com/v1/databases"
        headers = self.headers
        payload = {
            "parent": {"type": "page_id", "page_id": self.parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": {
                "Event Name": {"title": {}},
                "Event Description": {"rich_text": {}},
                "Event Properties": {
                    "relation": {
                        "database_id": event_properties_db_id,
                        "type": "single_property",
                        "single_property": {},
                    }
                },
            },
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
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
            property_page = response.json()
            self.properties[name] = property_page["id"]
            self.save_cache()
            return property_page
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()

    def add_event_to_tracking_plan_database(
        self,
        database_id: str,
        event_name: str,
        event_description: str,
        related_property_page_ids: list,
    ) -> dict:
        """Add an event to the Notion database with relations to Event Properties."""
        url = "https://api.notion.com/v1/pages"
        headers = self.headers

        # Structure the payload for the Notion API
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Event Name": {"title": [{"text": {"content": event_name}}]},
                "Event Description": {
                    "rich_text": [{"text": {"content": event_description}}]
                },
                "Event Properties": {
                    "relation": [
                        {"id": page_id} for page_id in related_property_page_ids
                    ]  # List of related property page IDs
                },
            },
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()

    def get_database(self, database_id: str) -> dict:
        """Get a Notion database by its ID."""
        url = f"https://api.notion.com/v1/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()
