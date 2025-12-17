{{
  config(
    materialized='incremental',
    unique_key='zaak_id',
    schema='ggm',
    incremental_strategy='merge',
    merge_update_columns=[
      'omschrijving',
      'toelichting',
      'einddatum',
      'einddatumgepland',
      'uiterlijkeeinddatumafdoening',
      'vertrouwelijkheidaanduiding',
      'status',
      'duurverlenging',
      'redenverlenging',
      'indicatie_deelzaken',
      'zaakniveau'
    ]
  )
}}
WITH process_map AS (
    SELECT
        zaak_id,
        process_id
    FROM {{ ref('stg_rxm_processes') }}
),

verlengingen_agg AS (
    SELECT
        process_id,
        SUM(duur) AS duurverlenging,
        STRING_AGG(reden, ', ') AS redenverlenging
    FROM {{ ref('stg_rxm_zaakverlengingen') }}
    GROUP BY process_id
),

zaak_base AS (
  SELECT
    z.zaak_id AS zaak_id,
    'N' AS archiefnominatie,
    z.einddatum AS einddatum,
    z.einddatumgepland AS einddatumgepland,
    z.uiterlijkeeinddatumafdoening AS uiterlijkeeinddatumafdoening,
    NULL AS datumlaatstebetaling,
    z.registratiedatum AS registratiedatum,
    z.registratiedatum AS datumpublicatie,
    z.startdatum AS startdatum,
    z.einddatum + interval '7 year' AS datumvernietigingdossier,
    COALESCE(vg.duurverlenging, 0) AS duurverlenging,
    'N' AS indicatie_betaling,
    CASE WHEN z.hoofdzaak_id IS NOT NULL THEN 'J' ELSE 'N' END AS indicatie_deelzaken,
    'N' AS indicatie_opschorting,
    NULL AS leges,
    z.omschrijving AS omschrijving,
    NULL AS omschrijving_resultaat,
    NULL AS reden_opschorting,
    vg.redenverlenging AS redenverlenging,
    CASE WHEN z.einddatum IS NULL THEN 'open' ELSE 'closed' END AS status,
    z.toelichting AS toelichting,
    NULL AS toelichting_resultaat,
    z.vertrouwelijkheidaanduiding AS vertrouwelijkheidaanduiding,
    z.zaaktype_id AS zaaktype_id,
    CASE WHEN z.hoofdzaak_id IS NULL THEN 1 ELSE 2 END AS zaakniveau,
    z.creationtime AS creationtime,
    current_timestamp AS dbt_updated_at
  FROM {{ ref('stg_rxm_zaken') }} z
  LEFT JOIN process_map pm ON z.zaak_id = pm.zaak_id
  LEFT JOIN verlengingen_agg vg ON pm.process_id = vg.process_id
)
SELECT
  *
FROM zaak_base
{% if is_incremental() %}
  WHERE creationtime > (SELECT MAX(creationtime) FROM {{ this }})
{% endif %}