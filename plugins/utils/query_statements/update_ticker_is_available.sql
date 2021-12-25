UPDATE "public".financial_statements_statementsmetadata meta
SET is_available =
    CASE
        WHEN meta.is_income_statement_available = true
            AND meta.is_balance_sheet_statement_available = true
            AND meta.is_cash_flow_statement_available = true
            THEN true
        ELSE false
    END,
    is_processed = false
WHERE meta.symbol = '{{ symbol }}';
