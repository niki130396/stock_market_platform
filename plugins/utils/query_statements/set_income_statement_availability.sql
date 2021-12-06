UPDATE "public".financial_statements_statementsmetadata
SET is_income_statement_available = true
WHERE symbol = '{{ symbol }}';
