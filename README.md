# RudderStack Tracking Plans Integration into Notion

This project integrates RudderStack's tracking plans and event properties into Notion databases, providing a seamless way to sync and track events and properties across both platforms.

## Getting Started

### 1. Set Up the Environment

Make sure you create a `.env` file in the project root with the following variables:

```bash
NOTION_API_TOKEN=your_notion_api_token
NOTION_PARENT_PAGE_ID=your_notion_parent_page_id
RUDDERSTACK_API_TOKEN=your_rudderstack_api_token
RUDDERSTACK_BASE_URL=https://api.rudderstack.com/v2
```

### 2. Install Dependencies

Make sure you have Python installed. Then, install the required dependencies:

```bash
python -m venv tracking-plans
source tracking-plans/bin/activate
pip install -r requirements.txt
```

### 3. Run the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

This will start the API at `http://127.0.0.1:8000`.

### 4. Sync Event Properties and Tracking Plans

#### Sync Event Properties

To sync all event properties from RudderStack into Notion, run the following `curl` command:

```bash
curl http://127.0.0.1:8000/api/sync-event-properties
```

#### Sync Tracking Plans

To sync tracking plans from RudderStack into Notion, use this `curl` command:

```bash
curl http://127.0.0.1:8000/api/sync-tracking-plans
```

### 5. Cache

The project uses caching to store database IDs. You can find this in the `cache/databases.json` file, which keeps track of the Notion databases that have been created.

---

### Additional Information

- Make sure the Notion API integration is properly shared with the pages and databases it needs access to.
- The sync services are designed to avoid duplication and archive old databases when creating new ones.
