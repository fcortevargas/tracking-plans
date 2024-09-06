import json
import os
from app.services.rudderstack_service import RudderStackService
from app.services.notion_service import NotionService


class SyncService:
    def __init__(self, cache_file="cache/databases.json"):
        self.rudderstack_service = RudderStackService()
        self.notion_service = NotionService()
        self.cache_file = cache_file
        self.databases = self.load_cache()

    def load_cache(self) -> dict:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self) -> None:
        with open(self.cache_file, "w") as f:
            json.dump(self.databases, f, indent=4)
        print(f"Cache saved to {self.cache_file}")

    def find_database_by_name_in_cache(self, name: str) -> str:
        """Find the database ID by name in the cache."""
        return self.databases.get(name)

    def sync_event_properties_to_notion(self):
        """Sync all event properties from RudderStack to Notion's Event Properties database."""
        database_name = "Event Properties"

        # Step 1: Check if the database is already in the cache
        database_id = self.find_database_by_name_in_cache(database_name)

        if database_id:
            # Step 2: Archive the existing database and update the cache
            try:
                self.notion_service.archive_database(database_id)
                self.databases[database_name] = None  # Mark as archived
                self.save_cache()
            except Exception as e:
                print(f"Failed to archive database {database_name}: {e}")

        # Step 3: Create a new database and update the cache
        notion_db = self.notion_service.create_event_properties_database()
        database_id = notion_db["id"]

        # Update cache with new database ID
        self.databases[database_name] = database_id
        print(f"Created database {database_name} with ID {database_id}")
        self.save_cache()

        # Step 4: Get all event properties in data catalog
        event_properties = self.rudderstack_service.get_all_properties()

        for prop in event_properties.get("data", []):
            property_id = prop["id"]
            name = prop["name"]
            description = prop.get("description", "")
            prop_type = prop["type"]

            self.notion_service.add_property_to_event_properties_database(
                database_id=database_id,
                property_id=property_id,
                name=name,
                prop_type=prop_type,
                description=description,
            )

    def sync_tracking_plans_to_notion(self):
        # Step 1: Get all tracking plans from RudderStack
        tracking_plans = self.rudderstack_service.get_all_tracking_plans()

        for plan in tracking_plans.get("trackingPlans", []):
            tracking_plan_id = plan["id"]
            tracking_plan_name = plan["name"]

            # Step 2: Check if the database is already in the cache
            database_id = self.find_database_by_name_in_cache(tracking_plan_name)

            if database_id:
                # Step 3: Archive the existing database and update the cache
                try:
                    self.notion_service.archive_database(database_id)
                    self.databases[tracking_plan_name] = None  # Mark as archived
                    self.save_cache()
                except Exception as e:
                    print(f"Failed to archive database {tracking_plan_name}: {e}")
                    continue

            # Step 4: Create a new database and update the cache
            notion_db = self.notion_service.create_tracking_plan_database(
                tracking_plan_name
            )
            database_id = notion_db["id"]

            # Update cache with new database ID
            self.databases[tracking_plan_name] = database_id
            print(f"Created database {tracking_plan_name} with ID {database_id}")
            self.save_cache()

            # Step 5: Get all events for this tracking plan
            events = self.rudderstack_service.get_all_tracking_plan_events(
                tracking_plan_id
            )

            for event in events.get("data", []):
                event_id = event["id"]
                event_name = event["name"]

                # Step 6: Get event details
                event_details = self.rudderstack_service.get_tracking_plan_event(
                    tracking_plan_id, event_id
                )

                # Step 7: Extract the properties you want to add to Notion
                event_description = event.get("description", "No description available")
                properties = (
                    event_details.get("rules", {})
                    .get("properties", {})
                    .get("properties", {})
                    .get("properties", {})
                )

                if not properties:
                    print(f"No properties found for event {event_name}")
                    continue

                multiselect_options = [{"name": key} for key in properties.keys()]

                if not multiselect_options:
                    print(f"No properties to add for event {event_name}")
                    continue  # Skip this event if there are no properties

                # Step 8: Insert the event into the Notion database
                self.notion_service.add_event_to_tracking_plan_database(
                    database_id, event_name, event_description, multiselect_options
                )
