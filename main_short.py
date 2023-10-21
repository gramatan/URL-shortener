"""This is the main file for the shortener API."""
from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI
from jaeger_client import Config
from prometheus_client import make_asgi_app
from pydantic_settings import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from config.config import APP_PORT, HEALTHZ_PREFIX, JAEGER_HOST
from src.middlewares import metrics_middleware, tracing_middleware
from src.routers import readiness, shortener


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = '0.0.0.0'   # noqa: F401, S104
    app_port: int = APP_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст для работы приложения.

    В нашем случае используется для Егеря.

    Args:
        app: Приложение.

    Yields:
        Контекст приложения.
    """
    session = ClientSession()
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': JAEGER_HOST,
                'reporting_port': 6831,
            },
            'logging': True,
        },
        service_name='gran_url',
        validate=True,
    )
    tracer = config.initialize_tracer()
    yield {'client_session': session, 'jaeger_tracer': tracer}
    await session.close()

app = FastAPI(lifespan=lifespan)

app.include_router(readiness.router, prefix=HEALTHZ_PREFIX, tags=['readiness'])
app.include_router(shortener.router, prefix='/api', tags=['shortener'])

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)
app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=tracing_middleware,
)

if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
