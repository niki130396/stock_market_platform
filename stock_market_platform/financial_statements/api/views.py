from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from stock_market_platform.utils.query_helpers import (
    get_gross_margins_by_company,
    get_gross_margins_by_sector,
)


class BalanceSheetMetricsViewSet(ViewSet):
    @action(
        detail=False,
        methods=["GET"],
        url_path="gross-margin-company-wise",
        url_name="gross_margin_company_wise",
    )
    def get_gross_margin_by_company(self, request):
        gross_margins = get_gross_margins_by_company()
        return Response(gross_margins)

    @action(
        detail=False,
        methods=["GET"],
        url_path="gross-margin-sector-wise",
        url_name="gross_margin_sector_wise",
    )
    def get_gross_margin_by_sector(self, request):
        response = get_gross_margins_by_sector()
        return Response(response)
