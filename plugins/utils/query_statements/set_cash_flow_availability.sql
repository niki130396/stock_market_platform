UPDATE "public".financial_statements_statementsmetadata
SET is_cash_flow_statement_available = true
WHERE symbol = '{{ symbol }}';
