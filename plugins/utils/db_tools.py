from collections import defaultdict

import psycopg2
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


def update_ticker_status():
    pass


def get_unfetched_objects():
    SQL = """
        SELECT * FROM financial_statements_statementsmetadata
         WHERE is_available = False
         ORDER BY company_id
    """
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
    SQL = """
        SELECT
            statement_type_name_from_source,
            statement_type_local_name
        FROM crawling_statementtypesourcedefinition source

        JOIN crawling_statementtypelocaldefinition local
        ON local.statement_type_definition_id = source.local_statement_type_id

        JOIN crawling_crawlingsourcedetails details
        ON details.crawling_source_id = source.crawling_source_id
    """
    statements_map = {}

    cursor.execute(SQL)
    for row in cursor.fetchall():
        statements_map[row[1]] = row[0]
    return statements_map


class NormalizedFieldsProcessor:
    SQL = """
        SELECT
            field.name,
            normalized.name,
            normalized.statement_type
        FROM crawling_crawlingsourcedetails source

        JOIN %s field
        ON field.crawling_source_id = source.crawling_source_id
        JOIN crawling_normalizedfield normalized
        ON normalized.field_id = field.normalized_field_id
        WHERE source.name = '%s'
    """

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
            cursor.execute(self.SQL % (table, self.__source_name))
            output.update(self.fetch_fields())
        return output

    @property
    def mapped_source_fields(self):
        return self.__mapped_fields
