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

    def create_database(self, title: str) -> dict:
        """Create a new database."""
        database_data = {
            "parent": {"type": "page_id", "page_id": self.parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": {
                "Event Name": {"title": {}},
                "Event Description": {"rich_text": {}},
                "Properties": {"rich_text": {}},
            },
        }
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=self.headers,
            data=json.dumps(database_data),
        )
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def find_database_by_name(self, title: str) -> dict:
        """Search for a database by name in the parent page."""
        search_url = "https://api.notion.com/v1/search"
        payload = {
            "query": title,
            "filter": {"property": "object", "value": "database"},
        }
        response = requests.post(
            search_url, headers=self.headers, data=json.dumps(payload)
        )

        print(response.json())

        if response.status_code == 200:
            results = response.json().get("results", [])
            for result in results:
                if result["title"][0]["text"]["content"] == title:
                    return result
        else:
            response.raise_for_status()
        return None

    def archive_database(self, database_id: str) -> dict:
        """Archive an existing Notion database."""
        url = f"https://api.notion.com/v1/databases/{database_id}"
        update_data = {"archived": True}
        response = requests.patch(
            url, headers=self.headers, data=json.dumps(update_data)
        )
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def add_event_to_database(
        self,
        database_id: str,
        event_name: str,
        event_description: str,
        event_properties: str,
    ) -> dict:
        """Add an event to the Notion database."""
        new_page = {
            "parent": {"database_id": database_id},
            "properties": {
                "Event Name": {"title": [{"text": {"content": event_name}}]},
                "Event Description": {
                    "rich_text": [{"text": {"content": event_description}}]
                },
                "Properties": {"rich_text": [{"text": {"content": event_properties}}]},
            },
        }
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=self.headers,
            data=json.dumps(new_page),
        )
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()
