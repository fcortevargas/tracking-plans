import unittest
from app.services.notion_service import NotionService
from app.config import settings


class TestNotionServiceIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize the NotionService with real credentials
        self.service = NotionService()

        # The ID of the parent page where the database will be created
        self.parent_page_id = (
            settings.notion_parent_page_id
        )  # Replace with actual Notion parent page ID

    def test_create_and_add_event_to_database(self):
        # Step 1: Check if the database exists
        database_name = "Test Tracking Plan"
        found_database = self.service.find_database_by_name(database_name)

        if not found_database:
            # Step 2: Create the database if not found
            print(f"Database '{database_name}' not found. Creating a new one...")
            database = self.service.create_database(database_name)
        else:
            print(f"Database '{database_name}' found. Using the existing one.")
            database = found_database

        # Step 3: Add an event to the database
        database_id = database["id"]
        event_name = "Test Event"
        event_description = "This is a test event."
        event_properties = "Test properties"

        # Step 4: Add event to the database
        response = self.service.add_event_to_database(
            database_id=database_id,
            event_name=event_name,
            event_description=event_description,
            event_properties=event_properties,
        )

        # Step 5: Verify the response
        print(f"Response from adding event: {response}")

        self.assertIsInstance(
            response, dict, "Expected a dictionary response from Notion API"
        )
        self.assertIn("id", response, "Response does not contain an 'id'")
        self.assertIn("properties", response, "Response does not contain 'properties'")

        # Verify the added event's name in Notion
        self.assertEqual(
            response["properties"]["Event Name"]["title"][0]["text"]["content"],
            event_name,
            "Event name does not match",
        )


if __name__ == "__main__":
    unittest.main()
