SELECT normalized.name, line.field_id FROM crawling_financialstatementline line
JOIN crawling_normalizedfieldtree normalized
ON line.normalized_field_id = normalized.field_id
WHERE line.crawling_source_id IN (SELECT s.crawling_source_id FROM crawling_crawlingsourcedetails s
                                    WHERE s.name = '{{ source_name }}');
