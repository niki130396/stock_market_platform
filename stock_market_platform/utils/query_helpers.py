import os

from django.db import connection
from jinja2 import Template


def get_from_sql(rel_file_path: str, **kwargs):
    name, extension = rel_file_path.split(".")
    if extension != "sql":
        raise ValueError("Only .sql extension files supported")
    current_file_path = os.path.dirname(__file__)
    abs_file_path = os.path.join(current_file_path, rel_file_path)
    with open(abs_file_path, "r") as sql_file:
        SQL = Template(sql_file.read()).render(**kwargs)
        return SQL


def get_fields_by_statement_type_cte(fields, statement_type):
    CTE = get_from_sql(
        "raw_queries/select_by_statement_type_cte.sql",
        fields=fields,
        statement_type=statement_type,
    )
    return CTE


def get_gross_margins_by_sector():
    with connection.cursor() as cursor:
        CTE = get_fields_by_statement_type_cte(
            fields=[
                "meta.sector",
                "local_type.statement_type_local_name",
                "fact.fiscal_period",
                "normalized.name",
                "fact.value",
            ],
            statement_type="income_statement",
        )
        SELECT = get_from_sql("raw_queries/gross_margin_sectors.sql")
        SQL = CTE + "\n" + SELECT
        cursor.execute(SQL)
        response = list(cursor.fetchall())
    return response


def get_gross_margins_by_company():
    with connection.cursor() as cursor:
        CTE = get_fields_by_statement_type_cte(
            fields=[
                "meta.symbol",
                "local_type.statement_type_local_name",
                "fact.fiscal_period",
                "normalized.name",
                "fact.value",
            ],
            statement_type="income_statement",
        )
        SELECT = get_from_sql("raw_queries/gross_margin_company.sql")
        SQL = CTE + "\n" + SELECT
        cursor.execute(SQL)
        response = list(cursor.fetchall())
    return response
