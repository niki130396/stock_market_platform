import re

from django.db import models

# Create your models here.


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


class FinancialStatement(models.Model):
    crawling_source = models.ForeignKey(CrawlingSourceDetails, on_delete=models.CASCADE)
    normalized_field = models.ForeignKey(
        NormalizedField, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return str(self.crawling_source)

    @classmethod
    def get_statement_type(cls):
        class_name = cls._meta.object_name
        camel_case_split = re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", class_name)[
            :-1
        ]
        return "_".join(camel_case_split).lower()

    class Meta:
        abstract = True


class IncomeStatementField(FinancialStatement):
    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)


class BalanceSheetField(FinancialStatement):
    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)


class CashFlowField(FinancialStatement):
    field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
