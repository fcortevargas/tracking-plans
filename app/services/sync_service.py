from app.services.rudderstack_service import RudderStackService
from app.services.notion_service import NotionService


class SyncService:
    def __init__(self):
        self.rudderstack_service = RudderStackService()
        self.notion_service = NotionService()

    def sync_to_notion(self):
        # Step 1: Get all tracking plans
        tracking_plans = self.rudderstack_service.get_all_tracking_plans()

        for plan in tracking_plans.get("trackingPlans", []):
            tracking_plan_id = plan["id"]
            tracking_plan_name = plan["name"]

            # Step 2: Find or create a Notion database for this tracking plan
            found_database = self.notion_service.find_database_by_name(
                tracking_plan_name
            )
            if found_database:
                self.notion_service.archive_database(found_database["id"])
            notion_db = self.notion_service.create_database(tracking_plan_name)
            database_id = notion_db["id"]

            # Step 3: Get all events for this tracking plan
            events = self.rudderstack_service.get_all_tracking_plan_events(
                tracking_plan_id
            )

            for event in events.get("data", []):
                event_id = event["id"]
                event_name = event["name"]

                # Step 4: Get event details
                event_details = self.rudderstack_service.get_tracking_plan_event(
                    tracking_plan_id, event_id
                )

                # Extract the properties you want to add to Notion
                event_description = event.get("description", "")
                additional_properties = event_details.get("data", [{}])[0].get(
                    "identitySection", ""
                )

                # Step 5: Insert the event into the Notion database
                self.notion_service.add_event_to_database(
                    database_id, event_name, event_description, additional_properties
                )
