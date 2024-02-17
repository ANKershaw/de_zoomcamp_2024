-- Add an additional filter for keeping only records with pickup time in year 2019. 
-- Do not add a deduplication step. Run this models without limits (is_test_run: false)

{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
  select *,
    row_number() over(partition by dispatching_base_num, pickup_datetime) as rn
  from {{ source('staging','fhv_tripdata') }}
  where dispatching_base_num is not null 
)
select
    -- identifiers
    dispatching_base_num,
    affiliated_base_number,
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as trip_id,
    {{ dbt.safe_cast("pickup_location_id", api.Column.translate_type("integer")) }} as pickup_location_id,
    {{ dbt.safe_cast("dropoff_location_id", api.Column.translate_type("integer")) }} as dropoff_location_id,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- flags
    {{ dbt.safe_cast("sr_flag", api.Column.translate_type("integer")) }} as sr_flag

from tripdata
where EXTRACT(YEAR FROM pickup_datetime) = 2019


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}