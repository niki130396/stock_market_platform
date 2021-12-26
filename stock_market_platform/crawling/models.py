from django.db import models

from stock_market_platform.financial_statements.models import StatementsMetaData


class NormalizedField(models.Model):
    STATEMENT_TYPE_CHOICES = [
        ("income_statement", "Income Statement"),
        ("balance_sheet", "Balance Sheet"),
        ("cash_flow", "Cash Flow"),
        ("other", "Other"),
    ]

    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    humanized_name = models.CharField(max_length=256, null=True, blank=True)
    statement_type = models.CharField(
        max_length=256, choices=STATEMENT_TYPE_CHOICES, default="income_statement"
    )

    def __str__(self):
        return self.humanized_name


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


class StatementTypeSourceDefinition(models.Model):
    statement_type_definition_id = models.AutoField(primary_key=True)
    statement_type_name_from_source = models.CharField(max_length=256)
    local_statement_type = models.ForeignKey(
        StatementTypeLocalDefinition, on_delete=models.PROTECT, null=True, blank=True
    )
    crawling_source = models.ForeignKey(
        CrawlingSourceDetails, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.statement_type_name_from_source


class FinancialStatementLine(models.Model):
    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank=True)
    source_statement_type = models.ForeignKey(
        StatementTypeSourceDefinition, on_delete=models.PROTECT
    )
    crawling_source = models.ForeignKey(CrawlingSourceDetails, on_delete=models.CASCADE)
    normalized_field = models.ForeignKey(NormalizedField, on_delete=models.PROTECT)


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
