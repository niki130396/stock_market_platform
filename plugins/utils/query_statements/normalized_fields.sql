SELECT
    field.name,
    normalized.name,
    normalized.statement_type
FROM "public".crawling_crawlingsourcedetails source
JOIN {{ field_table }} field
    ON field.crawling_source_id = source.crawling_source_id
JOIN "public".crawling_normalizedfield normalized
    ON normalized.field_id = field.normalized_field_id
WHERE source."name" = '{{ source_name }}'
