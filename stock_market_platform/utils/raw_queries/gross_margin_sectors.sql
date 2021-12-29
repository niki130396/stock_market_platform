SELECT gross_profit.sector,
       gross_profit.fiscal_period,
       ROUND(CAST(gross_profit.value AS DECIMAL) / CAST(total_revenue.value AS DECIMAL), 2) AS gross_margin
FROM
    (   SELECT i.sector, i.fiscal_period, AVG(i.value) AS value from income_statements i
        WHERE i.name = 'gross_profit'
        AND NOT i.sector = ''
        GROUP BY i.sector, i.fiscal_period
        ORDER BY i.sector
    ) gross_profit

    JOIN

    (   SELECT i.sector, i.fiscal_period, AVG(i.value) AS value from income_statements i
        WHERE i.name = 'total_revenue'
        AND NOT i.sector = ''
        GROUP BY i.sector, i.fiscal_period
        ORDER BY i.sector
    ) total_revenue

    ON gross_profit.sector = total_revenue.sector
    AND gross_profit.fiscal_period = total_revenue.fiscal_period
WHERE gross_profit.value > 0
AND total_revenue.value > 0;
