{{
  config(
    materialized='view',
    schema='stg'
  )
}}

SELECT
  "Creationtime" AS creationtime,
  "Einddatum" AS einddatum,
  "Einddatumgepland" AS einddatumgepland,
  "Hoofdzaak_id" AS hoofdzaak_id,
  "Zaak_id" AS zaak_id,
  "Zaaknummer" AS zaaknummer,
  "Omschrijving" AS omschrijving,
  "Registratiedatum" AS registratiedatum,
  "Startdatum" AS startdatum,
  "Toelichting" AS toelichting,
  "UiterlijkeEinddatumAfdoening" AS uiterlijkeeinddatumafdoening,
  "VerantwoordelijkeOrganisatie" AS verantwoordelijkeorganisatie,
  "VertrouwelijkheidAanduiding" AS vertrouwelijkheidaanduiding,
  "Zaaktype_id" AS zaaktype_id,
  "When" AS when,
  "Change" AS change
FROM {{ ref('raw_rxm_zaken') }}
