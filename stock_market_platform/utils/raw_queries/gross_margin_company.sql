SELECT gross_profit.symbol,
       gross_profit.fiscal_period,
       ROUND(CAST(gross_profit.value AS DECIMAL) / CAST(total_revenue.value AS DECIMAL), 2) AS gross_margin
FROM
    (   SELECT i.symbol, i.fiscal_period, i.value from income_statements i
        WHERE i.name = 'gross_profit'
        GROUP BY i.symbol, i.fiscal_period, i.value
        ORDER BY i.symbol
    ) gross_profit

    JOIN

    (   SELECT i.symbol, i.fiscal_period, i.value from income_statements i
        WHERE i.name = 'total_revenue'
        GROUP BY i.symbol, i.fiscal_period, i.value
        ORDER BY i.symbol
    ) total_revenue

    ON gross_profit.symbol = total_revenue.symbol
    AND gross_profit.fiscal_period = total_revenue.fiscal_period
WHERE gross_profit.value > 0
AND total_revenue.value > 0;
