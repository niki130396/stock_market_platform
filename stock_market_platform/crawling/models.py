from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from stock_market_platform.financial_statements.models import StatementsMetaData


class NormalizedFieldTree(MPTTModel):
    STATEMENT_TYPE_CHOICES = [
        ("income_statement", "Income Statement"),
        ("balance_sheet", "Balance Sheet"),
        ("cash_flow", "Cash Flow"),
        ("other", "Other"),
    ]

    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    humanized_name = models.CharField(max_length=256, null=True, blank=True)
    statement_type = models.CharField(
        max_length=256, choices=STATEMENT_TYPE_CHOICES, default="income_statement"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", blank=True, null=True
    )

    def __str__(self):
        return f"{self.humanized_name} - {self.statement_type}"

    class Meta:
        unique_together = ("name", "statement_type")


class CrawlingSourceDetails(models.Model):
    SOURCE_TYPE_CHOICES = [("API", "API"), ("HTML", "HTML")]
    crawling_source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    source_type = models.CharField(
        max_length=256, choices=SOURCE_TYPE_CHOICES, default="API"
    )

    def __str__(self):
        return self.name


class StatementTypeLocalDefinition(models.Model):
    statement_type_definition_id = models.AutoField(primary_key=True)
    statement_type_local_name = models.CharField(max_length=256)

    def __str__(self):
        return self.statement_type_local_name


class FinancialStatementLine(models.Model):
    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank=True)
    statement_type = models.ForeignKey(
        StatementTypeLocalDefinition, on_delete=models.DO_NOTHING, default=1
    )
    crawling_source = models.ForeignKey(CrawlingSourceDetails, on_delete=models.CASCADE)
    normalized_field = TreeForeignKey(NormalizedFieldTree, on_delete=models.PROTECT)


class FinancialStatementFact(models.Model):
    fact_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(StatementsMetaData, on_delete=models.PROTECT)
    financial_statement_line = models.ForeignKey(
        FinancialStatementLine, on_delete=models.PROTECT
    )
    fiscal_year = models.PositiveIntegerField(null=True, blank=True)
    fiscal_period = models.CharField(max_length=30, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    value = models.IntegerField()
