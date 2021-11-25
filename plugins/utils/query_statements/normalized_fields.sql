WITH source_name AS (
    SELECT source.crawling_source_id
    FROM "public".crawling_crawlingsourcedetails source
    WHERE source.name = '{{ source_name }}'
)

SELECT * FROM (
    SELECT
        field.name,
        normalized.name,
        normalized.statement_type
    FROM "public".crawling_incomestatementfield field
    JOIN "public".crawling_normalizedfield normalized
        ON normalized.field_id = field.normalized_field_id
    WHERE field.crawling_source_id IN (SELECT * FROM source_name)

    UNION

    SELECT
        field.name,
        normalized.name,
        normalized.statement_type
    FROM "public".crawling_balancesheetfield field
    JOIN "public".crawling_normalizedfield normalized
        ON normalized.field_id = field.normalized_field_id
    WHERE field.crawling_source_id IN (SELECT * FROM source_name)

    UNION

    SELECT
        field.name,
        normalized.name,
        normalized.statement_type
    FROM "public".crawling_cashflowfield field
    JOIN "public".crawling_normalizedfield normalized
        ON normalized.field_id = field.normalized_field_id
    WHERE field.crawling_source_id IN (SELECT * FROM source_name)
) statement_fields
ORDER BY statement_fields.statement_type
