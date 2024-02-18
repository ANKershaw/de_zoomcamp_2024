{{
    config(
        materialized='table'
    )
}}

with green_tripdata as (
    select 
        pickup_datetime,
        dropoff_datetime, 
        pickup_location_id,
        dropoff_location_id,
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
), 
yellow_tripdata as (
    select 
        pickup_datetime,
        dropoff_datetime, 
        pickup_location_id,
        dropoff_location_id,
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
), 
fhv_tripdata as (
    select
        pickup_datetime,
        dropoff_datetime, 
        pickup_location_id,
        dropoff_location_id,
        'Fhv' as service_type
    from {{ ref('stg_fhv_tripdata') }}
), 
trips_unioned as (
    select * from green_tripdata
    union all 
    select * from yellow_tripdata
    union all
    select * from fhv_tripdata
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select
    trips_unioned.service_type,
    trips_unioned.pickup_location_id, 
    trips_unioned.dropoff_location_id,
    trips_unioned.pickup_datetime, 
    trips_unioned.dropoff_datetime
from trips_unioned
inner join dim_zones as pickup_zone
on trips_unioned.pickup_location_id = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trips_unioned.dropoff_location_id = dropoff_zone.locationid
