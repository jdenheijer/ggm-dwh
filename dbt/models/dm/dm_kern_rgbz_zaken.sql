{{ 
  config(
    materialized='view',
    schema='dm'
  ) 
}}

-- Expose all columns from the ggm model
SELECT
  *
FROM {{ ref('ggm_kern_rgbz_zaken') }}