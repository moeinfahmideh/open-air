-- models/staging/stg_airnow_measurements.sql
{{ config(materialized='view') }}

SELECT
    -- timestamp in UTC
    (
      (payload->>'DateObserved')::date
        + ((payload->>'HourObserved')::int || ' hours')::interval
    ) AT TIME ZONE 'UTC'                  AS observed_at,

    -- geo
    (payload->>'Latitude')::numeric       AS lat,
    (payload->>'Longitude')::numeric      AS lon,
    payload->>'ReportingArea'             AS location_name,
    payload->>'StateCode'                 AS state_code,

    -- pollutant info
    payload->>'ParameterName'             AS parameter,
    (payload->>'AQI')::int                AS aqi,

    -- AirNow does not send concentration mass for “current” calls
    NULL::numeric                         AS value
FROM raw.measurements_raw
WHERE provider = 'airnow'
