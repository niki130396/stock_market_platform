UPDATE "public".financial_statements_statementsmetadata
SET is_available = true
WHERE symbol = '{{ symbol }}';
