UPDATE "public".financial_statements_statementsmetadata meta
SET is_processed = true,
    is_attempted = true
FROM (SELECT * FROM "public".financial_statements_statementsmetadata sub_meta
      WHERE sub_meta.is_available = false
      AND sub_meta.is_processed = false
      ORDER BY sub_meta.symbol, sub_meta.is_attempted DESC
      LIMIT 1) AS subquery
WHERE meta.symbol = subquery.symbol
RETURNING meta.*;
