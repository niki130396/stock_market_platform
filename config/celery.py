from celery import Celery

celery_app = Celery(
    "stock_market_platform",
    backend="redis://localhost",
    broker="redis://localhost",
    include=["stock_market_platform.statements_crawling.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Sofia",
    enable_utc=True,
)
