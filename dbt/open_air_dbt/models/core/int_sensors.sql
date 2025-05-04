{{ config(materialized='table') }}

/*
  AirNow Sensors:
  One row per pollutant measured by AirNow, with its fixed lat/lon.
*/

SELECT DISTINCT
  'airnow'                 AS provider,
  parameter,
  lat,
  lon
FROM {{ ref('stg_airnow_measurements') }}

