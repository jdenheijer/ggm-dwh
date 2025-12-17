{{
  config(
    materialized='view',
    schema='stg'
  )
}}

SELECT
  "Organization_id" AS organization_id,
  "VerantwoordelijkeTeam_id" AS verantwoordelijketeam_id,
  "Verantwoordelijke_id" AS verantwoordelijke_id,
  "Process_id" AS process_id,
  "Processmodel_id" AS processmodel_id,
  "Procedure" AS procedure,
  "BehandelendTeam_id" AS behandelendteam_id,
  "Behandelaar_id" AS behandelaar_id,
  "Zaak_id" AS zaak_id,
  "Zaaktype_id" AS zaaktype_id,
  "When" AS when,
  "Change" AS change,
  "Is_heropend" AS is_heropend
FROM {{ ref('raw_rxm_processes') }}
