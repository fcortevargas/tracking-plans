import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


class TestAPIEndpoints(unittest.TestCase):
    client = TestClient(app)

    @patch("app.services.sync_service.SyncService.sync_to_notion")
    def test_sync_tracking_plans(self, mock_sync):
        # Mock the sync service to simulate a successful sync
        mock_sync.return_value = None

        response = self.client.get("/api/sync-tracking-plans")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "success", "message": "Tracking plans synced successfully"},
        )


if __name__ == "__main__":
    unittest.main()
