"""This is the main file for the shortener API."""
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import APP_PORT, HEALTHZ_PREFIX
from src.routers import readiness


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = '0.0.0.0'   # noqa: F401, S104
    app_port: int = APP_PORT


app = FastAPI()

app.include_router(readiness.router, prefix=HEALTHZ_PREFIX, tags=['shortener'])


if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
