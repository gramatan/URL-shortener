"""Мидлвари с метриками для приложения."""
from fastapi import Request, Response
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)
from prometheus_client import Counter

requests_num = Counter(
    'gran_url_request_number',
    'Count number of requests',
    ['endpoint'],
)
http_requests_total = Counter(
    'gran_url_http_requests_total',
    'Total HTTP Requests',
)


async def metrics_middleware(request: Request, call_next):
    """
    Middleware для реализации логгирования времени выполнения запроса.

    Args:
        request: Запрос.
        call_next: Следующий обработчик запроса.

    Returns:
        Ответ.
    """
    http_requests_total.inc()
    requests_num.labels(request.url.path).inc()
    response: Response = await call_next(request)

    return response  # noqa: WPS331


async def tracing_middleware(request: Request, call_next):
    """
    Middleware для реализации трейсинга.

    Args:
        request: Запрос.
        call_next: Следующий обработчик запроса.

    Returns:
        Ответ.
    """
    path = request.url.path
    if (
        path.startswith('/up')
        or path.startswith('/ready')
        or path.startswith('/metrics')
    ):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS,
            request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None

    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: request.url,
    }
    with global_tracer().start_active_span(
        str(request.url.path), child_of=span_ctx, tags=span_tags,
    ):
        return await call_next(request)
