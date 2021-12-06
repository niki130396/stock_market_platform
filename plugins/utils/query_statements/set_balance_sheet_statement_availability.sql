UPDATE "public".financial_statements_statementsmetadata
SET is_balance_sheet_statement_available = true
WHERE symbol = '{{ symbol }}';
