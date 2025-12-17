{{
  config(
    materialized='view',
    schema='stg'
  )
}}

SELECT
  "Duur" AS duur,
  "Reden" AS reden,
  "Process_id" AS process_id,
  "When" AS when,
  "Change" AS change,
  "Verlengd_op" AS verlengd_op
FROM {{ ref('raw_rxm_zaakverlengingen') }}
