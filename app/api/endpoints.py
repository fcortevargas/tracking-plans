from fastapi import APIRouter, HTTPException
from app.services.sync_service import SyncService

router = APIRouter()

@router.get("/sync-tracking-plans")
def sync_tracking_plans():
    sync_service = SyncService()

    try:
        sync_service.sync_to_notion()
        return {"status": "success", "message": "Tracking plans synced successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))