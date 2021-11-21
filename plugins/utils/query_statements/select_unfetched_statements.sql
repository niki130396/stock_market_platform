SELECT * FROM "public".financial_statements_statementsmetadata
    WHERE is_available = false
    ORDER BY company_id
