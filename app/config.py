import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    rudderstack_api_key: str = os.getenv("RUDDERSTACK_API_KEY")
    notion_api_key: str = os.getenv("NOTION_API_KEY")
    catalog_id: str = os.getenv("RUDDERSTACK_CATALOG_ID")
    parent_page_id: str = os.getenv("NOTION_PARENT_PAGE_ID")

    class Config:
        env_file = ".env"


settings = Settings()
