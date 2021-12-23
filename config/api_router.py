from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from stock_market_platform.financial_statements.api.views import (
    BalanceSheetMetricsViewSet,
)
from stock_market_platform.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "financial_statements", BalanceSheetMetricsViewSet, basename="financial-statements"
)


app_name = "api"
urlpatterns = router.urls
