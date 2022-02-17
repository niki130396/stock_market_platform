from django.contrib import admin
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from mptt.admin import MPTTModelAdmin

from stock_market_platform.crawling import models
from stock_market_platform.crawling.forms import (
    FinancialStatementFieldInlineFormset,
    NormalizedFieldTreeForm,
)

# Register your models here.

admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)


class FinancialStatementFieldGenericInline:
    statement_type = None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "normalized_field":
            field.queryset = field.queryset.filter(
                statement_type__in=(self.statement_type, "other")
            )
        if db_field.name == "statement_type":
            field.queryset = field.queryset.filter(
                statement_type_local_name=self.statement_type
            )
        return field

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(
            statement_type__statement_type_local_name=self.statement_type
        )


class IncomeStatementFieldAdminInline(
    FinancialStatementFieldGenericInline, admin.TabularInline
):
    model = models.FinancialStatementLine
    extra = 0
    formset = FinancialStatementFieldInlineFormset
    statement_type = "income_statement"
    verbose_name = "income statement line"
    verbose_name_plural = "Income Statement"


class BalanceSheetFieldAdminInline(
    FinancialStatementFieldGenericInline, admin.TabularInline
):
    model = models.FinancialStatementLine
    extra = 0
    formset = FinancialStatementFieldInlineFormset
    statement_type = "balance_sheet"
    verbose_name = "balance sheet line"
    verbose_name_plural = "Balance Sheet"


class CashFlowFieldAdminInline(
    FinancialStatementFieldGenericInline, admin.TabularInline
):
    model = models.FinancialStatementLine
    extra = 0
    formset = FinancialStatementFieldInlineFormset
    statement_type = "cash_flow"
    verbose_name = "cash flow line"
    verbose_name_plural = "Cash Flow"


@admin.register(models.CrawlingSourceDetails)
class CrawlingSourceDetailsAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementFieldAdminInline,
        BalanceSheetFieldAdminInline,
        CashFlowFieldAdminInline,
    ]


@admin.register(models.NormalizedFieldTree)
class NormalizedFieldTreeAdmin(MPTTModelAdmin):
    list_display = ("name", "humanized_name", "statement_type")
    search_fields = ("humanized_name",)
    list_filter = ("statement_type",)
    form = NormalizedFieldTreeForm
