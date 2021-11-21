import os
from collections import defaultdict

import psycopg2
from jinja2 import Template
from utils.models import DocumentModel

connection_kwargs = {
    "user": "vYFyCTEJOyYWibhYuVxlnvezFuDHwGXI",
    "password": "tD8Fpalp5GviRKn8zbBc0GdCIRWxynoqChkm4NaEG7g42lJgypqC1Iw8X7l6zAv5",
    "host": "postgres",
    "port": 5432,
    "database": "stock_market_platform",
}

connection = psycopg2.connect(**connection_kwargs)
cursor = connection.cursor()


def get_from_sql(rel_file_path: str, **kwargs):
    name, extension = rel_file_path.split(".")
    if extension != "sql":
        raise ValueError("Only .sql extension files supported")
    current_file_path = os.path.dirname(__file__)
    abs_file_path = os.path.join(current_file_path, rel_file_path)
    with open(abs_file_path, "r") as sql_file:
        SQL = Template(sql_file.read()).render(**kwargs)
        return SQL


def update_ticker_status():
    pass


def get_unfetched_objects():
    SQL = get_from_sql("query_statements/select_unfetched_statements.sql")
    cursor.execute(SQL)
    output = []
    for row in cursor.fetchall():
        output.append(
            DocumentModel(
                id=row[0], symbol=row[1], name=row[2], sector=row[7], industry=row[8]
            )
        )
    return output


def get_source_statement_types_map():
    SQL = get_from_sql("query_statements/source_statement_types.sql")
    statements_map = {}

    cursor.execute(SQL)
    for row in cursor.fetchall():
        statements_map[row[1]] = row[0]
    return statements_map


class NormalizedFieldsProcessor:
    def __init__(self, source_name):
        self.__source_name = source_name
        self.__statement_types_map = get_source_statement_types_map()
        self.__mapped_fields = self.fetch_source_and_normalized_field_names()

    def fetch_fields(self):
        output = defaultdict(dict)
        for fields in cursor.fetchall():
            source_field_name, local_field_name, local_statement_type_name = fields
            output[self.__statement_types_map[local_statement_type_name]][
                source_field_name
            ] = local_field_name
        return output

    def fetch_source_and_normalized_field_names(self):
        local_field_tables = [
            "crawling_incomestatementfield",
            "crawling_balancesheetfield",
            "crawling_cashflowfield",
        ]
        output = {}
        for table in local_field_tables:
            cursor.execute(
                get_from_sql(
                    "query_statements/normalized_fields.sql",
                    field_table=table,
                    source_name=self.__source_name,
                )
            )
            output.update(self.fetch_fields())
        return output

    @property
    def mapped_source_fields(self):
        return self.__mapped_fields
