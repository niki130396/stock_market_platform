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
from stock_market_platform.crawling.forms import NormalizedFieldTreeForm

# Register your models here.

admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)


class FinancialStatementFieldAdminInline(admin.TabularInline):
    model = models.FinancialStatementLine
    extra = 0


@admin.register(models.CrawlingSourceDetails)
class CrawlingSourceDetailsAdmin(admin.ModelAdmin):
    inlines = [
        FinancialStatementFieldAdminInline,
    ]


@admin.register(models.NormalizedFieldTree)
class NormalizedFieldTreeAdmin(MPTTModelAdmin):
    list_display = ("name", "humanized_name", "statement_type")
    search_fields = ("humanized_name",)
    list_filter = ("statement_type",)
    form = NormalizedFieldTreeForm
