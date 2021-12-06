UPDATE "public".financial_statements_statementsmetadata
SET is_available = true
WHERE symbol = '{{ symbol }}'
AND is_income_statement_available = true
AND is_balance_sheet_statement_available = true
AND is_cash_flow_statement_available = true;
