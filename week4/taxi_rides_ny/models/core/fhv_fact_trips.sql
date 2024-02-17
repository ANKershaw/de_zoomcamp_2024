{{
    config(
        materialized='table'
    )
}}

with fhv_trips as (
    select *, 
        'Fhv' as service_type
    from {{ ref('stg_fhv_tripdata') }}
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select
        dispatching_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        sr_flag,
        affiliated_base_number
from fhv_trips
inner join dim_zones as pickup_zone
on fhv_trips.pickup_location_id = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_trips.dropoff_location_id = dropoff_zone.locationid
