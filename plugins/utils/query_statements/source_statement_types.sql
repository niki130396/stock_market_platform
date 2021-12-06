SELECT
    source.statement_type_name_from_source,
    local.statement_type_local_name
FROM "public".crawling_statementtypesourcedefinition source
JOIN "public".crawling_statementtypelocaldefinition local
    ON local.statement_type_definition_id = source.local_statement_type_id;
