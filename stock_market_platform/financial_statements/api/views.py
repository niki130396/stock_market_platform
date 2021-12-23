from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from stock_market_platform.utils.mongodb import get_gross_margin


class BalanceSheetMetricsViewSet(ViewSet):
    @action(
        detail=False,
        methods=["GET"],
        url_path="gross-profit-margin",
        url_name="gross_profit_margin",
    )
    def get_gross_profit_margin(self, request):
        gross_margins = get_gross_margin()
        return Response(gross_margins)
