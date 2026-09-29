from fastapi import FastAPI
from backend.routes import router
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(title="LegalEase")

app.include_router(router)
class Settings(BaseSettings):
    app_name: str = "LegalEase"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    backend_url: str = "http://127.0.0.1:8000"

    cors_origins: str = (
        "http://localhost:8501,"
        "http://127.0.0.1:8501"
    )

    max_output_tokens: int = 8192
    temperature: float = 0.25

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()