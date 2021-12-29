WITH income_statements AS (
    SELECT
    {% for field in fields %}
    {% if not loop.last %}
    {{ field }},
    {% else %}
    {{ field }}
    {% endif %}
    {% endfor %}
    FROM crawling_financialstatementfact fact

    JOIN financial_statements_statementsmetadata meta
    ON fact.company_id = meta.company_id
    JOIN crawling_financialstatementline line
    ON fact.financial_statement_line_id = line.field_id
    JOIN crawling_normalizedfield normalized
    ON line.normalized_field_id = normalized.field_id
    JOIN crawling_statementtypesourcedefinition statement_type
    ON line.source_statement_type_id = statement_type.statement_type_definition_id
    JOIN crawling_statementtypelocaldefinition local_type
    ON statement_type.local_statement_type_id = local_type.statement_type_definition_id
    WHERE local_type.statement_type_local_name = '{{ statement_type }}'
)
