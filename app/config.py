from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rudderstack_api_token: str
    notion_api_token: str
    rudderstack_base_url: str
    notion_parent_page_id: str

    class Config:
        env_file = ".env"


settings = Settings()
