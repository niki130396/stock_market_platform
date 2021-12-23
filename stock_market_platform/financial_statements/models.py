from django.db import models

# Create your models here.


class StatementsMetaData(models.Model):
    company_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    market_cap = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    ipo_year = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=False)
    is_income_statement_available = models.BooleanField(default=False)
    is_balance_sheet_statement_available = models.BooleanField(default=False)
    is_cash_flow_statement_available = models.BooleanField(default=False)
    is_processed = models.BooleanField(
        default=False,
        help_text="Signals if a symbol is currently being processed by a spider",
    )
    is_attempted = models.BooleanField(
        default=False,
        help_text="Signals if financial statements for a given symbol have been attempted to be downloaded",
    )
