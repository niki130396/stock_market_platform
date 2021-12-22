from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from stock_market_platform.financial_statements.api.serializers import (
    BalanceSheetMetricsSerializer,
)


class BalanceSheetMetricsViewSet(ViewSet):

    @action(detail=False, methods=["GET"], url_path="gross-profit-margin", url_name="gross_profit_margin")
    def get_gross_profit_margin(self, request):
        return Response({"this": 1})
