from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"

    llm_provider: str = "openai"
    llm_model: str = "gpt-5.5"

    database_url: str = "sqlite:///./data/emodiary.db"
    chroma_persist_dir: str = "./data/chroma"

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
