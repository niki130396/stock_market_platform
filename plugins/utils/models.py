from dataclasses import dataclass


class FinancialStatementDefinition:
    statement_type = None

    def __init__(self, mapped_fields):
        self.mapped_fields = mapped_fields[self.statement_type]

    def __map_source_fields_to_local_fields(self, data):
        output = []
        for report in data:
            remapped_report = {}
            for field, value in self.mapped_fields.items():
                remapped_report[value] = report[field]
            output.append(remapped_report)
        return output

    def set_data(self, data):
        output = self.__map_source_fields_to_local_fields(data)
        self.data = output


class IncomeStatementModel(FinancialStatementDefinition):
    statement_type = "income_statement"


class BalanceSheetModel(FinancialStatementDefinition):
    statement_type = "balance_sheet"


class CashFlowModel(FinancialStatementDefinition):
    statement_type = "cash_flow"


@dataclass
class DocumentModel:
    id: int
    symbol: str
    name: str
    sector: str
    industry: str
