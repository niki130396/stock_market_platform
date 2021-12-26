SELECT line.name,
       normalized.name,
       normalized.statement_type
FROM crawling_financialstatementline line
JOIN crawling_normalizedfield normalized
ON line.normalized_field_id = normalized.field_id
WHERE crawling_source_id IN (SELECT details.crawling_source_id FROM crawling_crawlingsourcedetails details
                             WHERE details.name = '{{ source_name }}')
ORDER BY normalized.statement_type;
