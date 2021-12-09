from django.contrib import admin
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from stock_market_platform.crawling import models

# Register your models here.

admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)


class FinancialStatementGenericInline:
    fields = ["name", "crawling_source", "normalized_field"]
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "normalized_field":
            statement_type = db_field.model.get_statement_type()
            field.queryset = field.queryset.filter(
                statement_type__in=(statement_type, "other")
            )
        return field


class IncomeStatementFieldsInline(FinancialStatementGenericInline, admin.TabularInline):
    model = models.IncomeStatementField


class BalanceSheetFieldsInline(FinancialStatementGenericInline, admin.TabularInline):
    model = models.BalanceSheetField


class CashFlowFieldsInline(FinancialStatementGenericInline, admin.TabularInline):
    model = models.CashFlowField


class StatementTypeSourceDefinitionInline(admin.TabularInline):
    model = models.StatementTypeSourceDefinition
    extra = 0


@admin.register(models.CrawlingSourceDetails)
class CrawlingSourceDetailsAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementFieldsInline,
        BalanceSheetFieldsInline,
        CashFlowFieldsInline,
        StatementTypeSourceDefinitionInline,
    ]


@admin.register(models.NormalizedField)
class NormalizedFieldsAdmin(admin.ModelAdmin):
    list_display = ["name", "humanized_name", "statement_type"]
    ordering = ("statement_type", "name")
    search_fields = ("name",)
    list_filter = ("statement_type", )
