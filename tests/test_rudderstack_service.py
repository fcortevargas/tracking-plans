import unittest
from unittest.mock import patch
from app.services.rudderstack_service import RudderStackService


class TestRudderStackService(unittest.TestCase):

    @patch("app.services.rudderstack_service.requests.get")
    def test_get_all_tracking_plans(self, mock_get):
        # Mock response for all tracking plans
        mock_response = {
            "trackingPlans": [
                {"id": "tp_2karqrN7gjPl7VTLX6KFNsm3EMq", "name": "Test Tracking Plan"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        service = RudderStackService()
        tracking_plans = service.get_all_tracking_plans()

        with self.subTest("Response is a dictionary"):
            self.assertIsInstance(
                tracking_plans, dict, "Expected a dictionary response"
            )

        with self.subTest("Response contains 'trackingPlans' key"):
            self.assertIn(
                "trackingPlans",
                tracking_plans,
                "Key 'trackingPlans' not found in response",
            )

        with self.subTest("Tracking plans are not empty"):
            self.assertGreater(
                len(tracking_plans["trackingPlans"]),
                0,
                "No tracking plans found in response",
            )

    @patch("app.services.rudderstack_service.requests.get")
    def test_get_tracking_plan(self, mock_get):
        # Mock response for a single tracking plan
        mock_response = {
            "id": "tp_2karqrN7gjPl7VTLX6KFNsm3EMq",
            "name": "Test Tracking Plan",
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        service = RudderStackService()
        tracking_plan_id = "tp_2karqrN7gjPl7VTLX6KFNsm3EMq"
        tracking_plan = service.get_tracking_plan(tracking_plan_id)

        with self.subTest("Response is a dictionary"):
            self.assertIsInstance(tracking_plan, dict, "Expected a dictionary response")

        with self.subTest("Tracking plan contains 'id' key"):
            self.assertIn(
                "id", tracking_plan, "Key 'id' not found in tracking plan response"
            )

    @patch("app.services.rudderstack_service.requests.get")
    def test_get_all_tracking_plan_events(self, mock_get):
        # Mock response for tracking plan events
        mock_response = {
            "data": [{"id": "ev_2kNerk3CTsz2MRyffp469FifuDT", "name": "Test Event"}]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        service = RudderStackService()
        tracking_plan_id = "tp_2karqrN7gjPl7VTLX6KFNsm3EMq"
        events = service.get_all_tracking_plan_events(tracking_plan_id)

        with self.subTest("Response is a dictionary"):
            self.assertIsInstance(events, dict, "Expected a dictionary response")

        with self.subTest("Response contains 'data' key"):
            self.assertIn("data", events, "Key 'data' not found in response")

        with self.subTest("Events are not empty"):
            self.assertGreater(
                len(events["data"]), 0, "No events found for the tracking plan"
            )

    @patch("app.services.rudderstack_service.requests.get")
    def test_get_tracking_plan_event(self, mock_get):
        # Mock response for a specific event in the tracking plan
        mock_response = {
            "id": "ev_2kNerk3CTsz2MRyffp469FifuDT",
            "rules": {"properties": {}},
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        service = RudderStackService()
        tracking_plan_id = "tp_2karqrN7gjPl7VTLX6KFNsm3EMq"
        event_id = "ev_2kNerk3CTsz2MRyffp469FifuDT"
        event = service.get_tracking_plan_event(tracking_plan_id, event_id)

        with self.subTest("Response is a dictionary"):
            self.assertIsInstance(event, dict, "Expected a dictionary response")

        with self.subTest("Event contains 'id' key"):
            self.assertIn("id", event, "Key 'id' not found in event response")

        with self.subTest("Event contains 'properties' key under 'rules'"):
            self.assertIn(
                "properties",
                event["rules"],
                "Event does not contain properties under 'rules'",
            )


if __name__ == "__main__":
    unittest.main()
