import unittest
from unittest.mock import patch
from app.services.notion_service import NotionService


class TestNotionService(unittest.TestCase):

    @patch("app.services.notion_service.requests.post")
    def test_create_database(self, mock_post):
        # Mock the response of the Notion API for creating a database
        mock_response = {
            "object": "database",
            "id": "db_123",
            "title": [{"type": "text", "text": {"content": "Test Tracking Plan"}}],
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        service = NotionService()
        database = service.create_database("Test Tracking Plan")

        self.assertEqual(database["object"], "database")
        self.assertEqual(database["id"], "db_123")
        self.assertEqual(database["title"][0]["text"]["content"], "Test Tracking Plan")

    @patch("app.services.notion_service.requests.post")
    def test_find_database_by_name(self, mock_post):
        # Mock the response of the Notion API for finding a database by name
        mock_response = {
            "results": [
                {
                    "object": "database",
                    "id": "816cce8c-9b5c-4d2a-a14c-818eb41b7d97",
                    "title": [
                        {"type": "text", "text": {"content": "Test Tracking Plan"}}
                    ],
                    "parent": {"page_id": "parent_page_id"},
                }
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        service = NotionService()

        # Run the method to trigger the print statements
        found_database = service.find_database_by_name("Test Tracking Plan")

        self.assertIsNotNone(found_database)
        self.assertEqual(found_database["object"], "database")
        self.assertEqual(found_database["id"], "816cce8c-9b5c-4d2a-a14c-818eb41b7d97")

    @patch("app.services.notion_service.requests.patch")
    def test_archive_database(self, mock_patch):
        # Mock the response of the Notion API for archiving a database
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = {
            "object": "database",
            "archived": True,
        }

        service = NotionService()
        response = service.archive_database("816cce8c-9b5c-4d2a-a14c-818eb41b7d97")

        self.assertEqual(response["archived"], True)


if __name__ == "__main__":
    unittest.main()
